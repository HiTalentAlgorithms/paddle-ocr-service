import os
import time

import fitz
import requests


def get_pdf_images(path):
    doc = fitz.open(path)
    images = []
    for page in doc:
        mat = fitz.Matrix(1.3, 1.3).preRotate(0)
        pix = page.getPixmap(matrix=mat, alpha=False)
        images.append(pix.getImageData())
    return images

def test_ocr(content):
    response = requests.post("http://13.229.18.220:31005/image2pdf", files={"file": content})
    return response.content


# root_path = "testpdf"
# result = open("result.csv","w",encoding="utf-8")
# result.write("file_path,pdf_page,time\n")
# for file in os.listdir(root_path):
#     path = os.path.join(root_path, file)
#     if os.path.isfile(path):
#         out_path = path+"_out"
#         if not os.path.exists(out_path):
#             os.makedirs(out_path)
#         images = get_pdf_images(path)
#         for i,image in enumerate(images):
#             start = time.time()
#             pdf_content = test_ocr(image)
#             end = time.time()
#             out_file_path = os.path.join(out_path, f"pdf{i}.pdf")
#             out_image_path = os.path.join(out_path, f"image{i}.png")
#             with open(out_file_path,"wb") as f :
#                 f.write(pdf_content)
#             with open(out_image_path,"wb") as f :
#                 f.write(image)
#             result.write(f"{path},{out_file_path},{end-start}\n")
#             result.flush()
# result.close()

path ="Zhewei_Wang_Resume.pdf"
if os.path.isfile(path):
    out_path = path+"_out"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    images = get_pdf_images(path)
    for i,image in enumerate(images):
        start = time.time()
        #pdf_content = test_ocr(image)
        end = time.time()
        out_file_path = os.path.join(out_path, f"pdf{i}.pdf")
        out_image_path = os.path.join(out_path, f"image{i}.png")
        # with open(out_file_path,"wb") as f :
        #     f.write(pdf_content)
        with open(out_image_path,"wb") as f :
            f.write(image)
