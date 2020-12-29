import io
import os
import uuid
import fitz
from PIL import Image

from lib.util import delete_dir
from settings import TEMPDIR


def recoverpix(doc, item):
    """
    from https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/extract-imga.py
    判断Smask是否存在
    :param doc: pdf doc对象
    :param item: pdf 中的image 对象
    :return: 图片数据
    """
    xref = item[0]  # xref of PDF image
    smask = item[1]  # xref of its /SMask

    # special case: /SMask exists
    # use Pillow to recover original image
    if smask > 0:
        fpx = io.BytesIO(  # BytesIO object from image binary
            doc.extractImage(xref)["image"],
        )
        fps = io.BytesIO(  # BytesIO object from smask binary
            doc.extractImage(smask)["image"],
        )
        img0 = Image.open(fpx)  # Pillow Image
        mask = Image.open(fps)  # Pillow Image
        img = Image.new("RGBA", img0.size)  # prepare result Image
        img.paste(img0, None, mask)  # fill in base image and mask
        bf = io.BytesIO()
        img.save(bf, "png")  # save to BytesIO
        return {  # create dictionary expected by caller
            "ext": "png",
            "colorspace": 3,
            "image": bf.getvalue(),
        }

    # special case: /ColorSpace definition exists
    # to be sure, we convert these cases to RGB PNG images
    if "/ColorSpace" in doc.xrefObject(xref, compressed=True):
        pix1 = fitz.Pixmap(doc, xref)
        pix2 = fitz.Pixmap(fitz.csRGB, pix1)
        return {  # create dictionary expected by caller
            "ext": "png",
            "colorspace": 3,
            "image": pix2.getImageData("png"),
        }
    return doc.extractImage(xref)


def ext_pdf_images(file_path):
    """
    提取pdf中嵌入的图片
    :param file_path: pdf文件路径
    :return:  输出的图片文件夹
    """
    doc = fitz.open(file_path)
    i = 0
    dir_name = str(uuid.uuid4())
    out_path = os.path.join(TEMPDIR, dir_name)
    xreflist = []
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for page in doc:
        images = page.get_images()
        for image in images:
            xref = image[0]
            if xref in xreflist:
                continue
            im = recoverpix(doc, image)
            with open(os.path.join(out_path, f"image_{str(i)}.{im['ext']}"), "wb") as imgout:
                imgout.write(im['image'])
                i += 1
            xreflist.append(xref)
    return out_path


def pdf_to_image(file_path):
    """
    将pdf 转成图片
    :param file_path: pdf文件路径
    :return:
    """
    doc = fitz.open(file_path)
    i = 0
    dir_name = str(uuid.uuid4())
    out_path = os.path.join(TEMPDIR, dir_name)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    images = []
    for page in doc:
        mat = fitz.Matrix(2, 2).preRotate(0)
        pix = page.getPixmap(matrix=mat, alpha=False)
        img_path = os.path.join(out_path, 'image_%s.png' % i)
        i += 1
        pix.writePNG(img_path)
        images.append(Image.open(img_path))

    sum_height = sum(im.size[1] for im in images)
    result = Image.new(images[0].mode, (images[0].size[0], sum_height))
    top = 0
    for index, image in enumerate(images):
        result.paste(image, box=(0, top))
        top += image.size[1]
    result_path = os.path.join(TEMPDIR, dir_name + ".png")
    result.save(result_path)
    delete_dir(out_path)
    return result_path
