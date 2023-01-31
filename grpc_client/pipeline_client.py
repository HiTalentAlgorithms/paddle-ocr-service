# copy from paddle_serving_server/pipeline/pipeline_client.py
import sys

import grpc
import numpy as np
from . import pipeline_service_pb2, pipeline_service_pb2_grpc
from io import BytesIO


class PipelineClient(object):
    """
    PipelineClient provides the basic capabilities of the pipeline SDK
    """

    def __init__(self):
        self._channel = None
        self._stub = None
        self._profile_key = "pipeline.profile"
        self._profile_value = "1"

    def connect(self, grpc_server):
        options = [('grpc.max_receive_message_length', 512 * 1024 * 1024),
                   ('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.lb_policy_name', 'round_robin')]
        self._channel = grpc.insecure_channel(grpc_server, options=options)
        self._stub = pipeline_service_pb2_grpc.PipelineServiceStub(self._channel)

    def _pack_request_package(self, feed_dict, pack_tensor_format,
                              use_tensor_bytes, profile):
        req = pipeline_service_pb2.Request()

        logid = feed_dict.get("logid")
        if logid is None:
            req.logid = 0
        else:
            if sys.version_info.major == 2:
                req.logid = np.long(logid)
            elif sys.version_info.major == 3:
                req.logid = int(logid)
            feed_dict.pop("logid")

        clientip = feed_dict.get("clientip")
        if clientip is None:
            req.clientip = '127.0.0.1'
        else:
            req.clientip = clientip
            feed_dict.pop("clientip")

        np.set_printoptions(threshold=sys.maxsize)
        if pack_tensor_format is False:
            # pack string key/val format
            for key, value in feed_dict.items():
                req.key.append(key)

                if (sys.version_info.major == 2 and
                        isinstance(value, (str, np.unicode)) or
                        ((sys.version_info.major == 3) and isinstance(value, str))):
                    req.value.append(value)
                    continue

                if isinstance(value, np.ndarray):
                    req.value.append(value.__repr__())
                elif isinstance(value, list):
                    req.value.append(np.array(value).__repr__())
                else:
                    raise TypeError(
                        "only str and np.ndarray type is supported: {}".format(
                            type(value)))

            if profile:
                req.key.append(self._profile_key)
                req.value.append(self._profile_value)
        else:
            # pack tensor format
            for key, value in feed_dict.items():

                # skipping the lod feed_var.
                # The declare of lod feed_var must be hebind the feed_var.
                if ".lod" in key:
                    continue

                one_tensor = req.tensors.add()
                one_tensor.name = key

                if isinstance(value, str):
                    one_tensor.str_data.append(value)
                    one_tensor.elem_type = 12  # 12 => string in proto
                    continue

                if isinstance(value, np.ndarray):
                    for one_dim in value.shape:
                        one_tensor.shape.append(one_dim)

                    # set lod info, must be list type.
                    lod_key = key + ".lod"
                    if lod_key in feed_dict:
                        lod_list = feed_dict.get(lod_key)
                        if lod_list is not None:
                            one_tensor.lod.extend(lod_list)

                    # packed into bytes
                    if use_tensor_bytes is True:
                        np_bytes = BytesIO()
                        np.save(np_bytes, value, allow_pickle=True)
                        one_tensor.byte_data = np_bytes.getvalue()
                        one_tensor.elem_type = 13  # 13 => bytes in proto
                        continue

                    flat_value = value.flatten().tolist()
                    # copy data
                    if value.dtype == "int64":
                        one_tensor.int64_data.extend(flat_value)
                        one_tensor.elem_type = 0
                    elif value.dtype == "float32":
                        one_tensor.float_data.extend(flat_value)
                        one_tensor.elem_type = 1
                    elif value.dtype == "int32":
                        one_tensor.int_data.extend(flat_value)
                        one_tensor.elem_type = 2
                    elif value.dtype == "float64":
                        one_tensor.float64_data.extend(flat_value)
                        one_tensor.elem_type = 3
                    elif value.dtype == "int16":
                        one_tensor.int_data.extend(flat_value)
                        one_tensor.elem_type = 4
                    elif value.dtype == "float16":
                        one_tensor.float_data.extend(flat_value)
                        one_tensor.elem_type = 5
                    elif value.dtype == "uint16":
                        one_tensor.uint32_data.extend(flat_value)
                        one_tensor.elem_type = 6
                    elif value.dtype == "uint8":
                        one_tensor.uint32_data.extend(flat_value)
                        one_tensor.elem_type = 7
                    elif value.dtype == "int8":
                        one_tensor.int_data.extend(flat_value)
                        one_tensor.elem_type = 8
                    elif value.dtype == "bool":
                        one_tensor.bool_data.extend(flat_value)
                        one_tensor.elem_type = 9
                    else:
                        raise TypeError(
                            "value type {} of tensor {} is not supported.".
                            format(value.dtype, key))

                else:
                    raise TypeError(
                        "only str and np.ndarray type is supported: {}".format(
                            type(value)))
        return req

    def predict(self,
                feed_dict,
                asyn=False,
                timeout=None,
                pack_tensor_format=False,
                use_tensor_bytes=False,
                profile=False,
                log_id=0):
        if not isinstance(feed_dict, dict):
            raise TypeError("feed must be dict type with format: {name: value}.")
        req = self._pack_request_package(feed_dict, pack_tensor_format,
                                         use_tensor_bytes, profile)
        req.logid = log_id
        if not asyn:
            return self._stub.inference(request=req, timeout=timeout)
        else:
            return self._stub.inference.future(request=req, timeout=timeout)
