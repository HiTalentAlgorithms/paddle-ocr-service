import os
import uuid
import shutil
from settings import TEMPDIR


def save_file(content):
    """
    暂存文件到本地目录
    :param content: 文件内容
    :return: 存储目录
    """
    out_file_name = str(uuid.uuid4())
    out_file_path = os.path.join(TEMPDIR, out_file_name)
    with open(out_file_path, "wb") as file:
        file.write(content)
    return out_file_path


def delete_dir(root_dir):
    """
    delete dir
    :param root_dir: root dir
    :return:
    """
    file_list = os.listdir(root_dir)
    for f in file_list:
        file_path = os.path.join(root_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            delete_dir(file_path)
    shutil.rmtree(root_dir, True)
