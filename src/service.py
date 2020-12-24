import os
import subprocess
import uuid

from settings import TESSERACT_CMD, TEMPDIR


def image_to_pdf(image_file_path):
    out_file_name = str(uuid.uuid4())
    out_file_path = os.path.join(TEMPDIR, out_file_name)
    cmd_args = [TESSERACT_CMD,  image_file_path, out_file_path,"-l", "chi_sim", "pdf"]
    try:
        # proc = subprocess.Popen(cmd_args)
        subprocess.run(cmd_args)
    except OSError as e:
        return f"tesseract run error: {str(e)}", None

    out_file_path = os.path.join(TEMPDIR, out_file_name+".pdf")
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
