# 部署 paddleocr v5

## 1.准备好 PaddleOCR.yaml

```yaml
pipeline_name: OCR

text_type: general

use_doc_preprocessor: True
use_textline_orientation: False

Serving:
  visualize: False

SubPipelines:
  DocPreprocessor:
    pipeline_name: doc_preprocessor
    use_doc_orientation_classify: True
    use_doc_unwarping: False
    SubModules:
      DocOrientationClassify:
        module_name: doc_text_orientation
        model_name: PP-LCNet_x1_0_doc_ori
        model_dir: null

SubModules:
  TextDetection:
    module_name: text_detection
    model_name: PP-OCRv5_server_det
    model_dir: null
    limit_side_len: 64
    limit_type: min
    max_side_limit: 1280
    thresh: 0.3
    box_thresh: 0.6
    batch_size: 1
    unclip_ratio: 1.5
  TextRecognition:
    module_name: text_recognition
    model_name: PP-OCRv5_server_rec
    model_dir: null
    batch_size: 2
    score_thresh: 0.0

```

## 2.部署文件参考 (compose.yaml)
```yaml
services:
  gpu-service:
    image: minghealtomni/paddle-ocr:v5-paddlex3.0.1-cuda11.8-cudnn8.9-trt8.6
    pull_policy: never
    container_name: paddle-ocr-v5
    ports:
    - "18091:8080"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: always
    volumes:
        # PaddleOCR.yaml 不挂载的话就会用默认的配置
        - /{my_path}/PaddleOCR.yaml:/root/PaddleX/PaddleOCR.yaml
        - /{my_local_cache_path}:/root/.paddlex
    command: ["paddlex", "--serve", "--pipeline", "PaddleOCR.yaml"]
```


### 测试结果数据参考(61张简历图片)

| 模型 | gpu men 占用 | batch_size(v5) | 串行处理图片耗时 | 并发处理图片耗时 |
| ------------- |--|----|--|----|
| v4 | ~4G | det:1 rec:1 | 26.51s | 25.47s |
| v5 | 2259 Mb | TextDetection:1 TextRecognition:2 | 35.62s | 33s |
| v5 | 3265 Mb | TextDetection:10 TextRecognition:10 | 36.54s | 35.84s |
| v5-tensortrt | 10825 Mb | TextDetection:1 TextRecognition:2 | 33.28s | 32s |
