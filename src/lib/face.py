import dlib

detector = dlib.get_frontal_face_detector()


def check_face(image_path):
    """
    检查是否有人脸
    :param image_path: image path
    :return: 人脸数大于0为true
    """
    img = dlib.load_rgb_image(image_path)
    dets = detector(img, 1)
    return len(dets) > 0
