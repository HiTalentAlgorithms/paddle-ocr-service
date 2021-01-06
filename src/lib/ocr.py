import os
import subprocess
import uuid

from settings import TEMPDIR, TESSERACT_CMD


# from tesserocr import PyTessBaseAPI

# tess_api = PyTessBaseAPI(lang="chi_sim")
def image_to_pdf(image_file_path):
    """
    图片ocr识别，使用Tesseract-OCR
    :param image_file_path: 图片路径
    :return: pdf 文本内容
    """
    out_file_name = str(uuid.uuid4())
    out_file_path = os.path.join(TEMPDIR, out_file_name)
    cmd_args = [TESSERACT_CMD, image_file_path, out_file_path, "-l", "chi_sim", "-c", "tessedit_create_pdf=1"]
    try:
        subprocess.run(cmd_args)
        # tess_api.SetVariable('tessedit_create_pdf', 'True')
        # tess_api.ProcessPages(outputbase=out_file_path,filename=image_file_path)
    except Exception as e:
        return f"tesseract run error: {str(e)}", None
    # finally:
    #     tess_api.End()
    out_file_path = os.path.join(TEMPDIR, out_file_name + ".pdf")
    if not os.path.exists(out_file_path):
        return f"tesseract run error: No output file", None
    with open(out_file_path, "rb") as file:
        buffer = file.read()
    try:
        os.remove(image_file_path)
        os.remove(out_file_path)
    except NotImplementedError:
        pass
    return None, buffer
