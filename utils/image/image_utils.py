import numpy as np
import imageio
import cv2
from PIL import Image, ImageFilter, ImageEnhance
from scipy import misc


def read(path):
    return misc.imread(path)


def save(path, img):
    return imageio.imsave(path, img)


def save_batch(paths, imgs):
    for i in range(len(paths)):
        imageio.imsave(paths[i], imgs[i])


def resize(img, hw, more=False):
    if img.shape[0] == hw[0] and img.shape[1] == hw[1]:
        return img.copy()
    if more:
        if hw[0] + hw[1] < img.shape[0] + img.shape[1]:
            return cv2.resize(img, (hw[1], hw[0]), interpolation=cv2.INTER_AREA)
        else:
            return cv2.resize(img, (hw[1], hw[0]), interpolation=cv2.INTER_CUBIC)
    else:
        return cv2.resize(img, (hw[1], hw[0]), interpolation=cv2.INTER_LINEAR)


def resize_scale(img, scale, more=False):
    hw = (int(img.shape[0] * scale), int(img.shape[1] * scale))
    return resize(img, hw=hw, more=more)


def auto_binary(img, more=False):
    if more:
        _, img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    else:
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return img


def binary(img, threshold=220):
    ret = img.copy()
    ret[ret >= threshold] = 255
    ret[ret < threshold] = 0
    return ret


def is_gray(img):
    return img.ndim == 2


def gray(img):
    if img.ndim == 3:
        if img.shape[2] == 3:
            return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        elif img.shape[2] == 4:
            img = convert_3_channel(img)
            return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        elif img.shape[2] == 2:
            return img[:, :, 0]
        else:
            raise BaseException('unknown image shape: ' + str(img.shape))
    elif img.ndim == 2:
        return img.copy()
    else:
        raise BaseException('unknown image shape: ' + str(img.shape))


def is_3_channel(img):
    return img.ndim == 3 and img.shape[-1] == 3


def convert_3_channel(img):
    if img.ndim == 2:
        h, w = img.shape
        ret = np.empty((h, w, 3), dtype=np.uint8)
        ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
        return ret
    elif img.ndim == 3 and img.shape[-1] == 3:
        return img.copy()
    elif img.ndim == 3 and img.shape[-1] == 4:
        transparency = np.empty(img.shape[:2], np.float32)
        ret = np.empty((img.shape[0], img.shape[1], 3), np.float32)
        transparency[:, :] = img[:, :, 3] / 255.
        for i in range(3):
            ret[:, :, i] = 255 * (1 - transparency[:, :]) + img[:, :, i] * transparency[:, :]
        return ret.astype(np.uint8)
    elif img.ndim == 3 and img.shape[-1] == 2:
        ret = img[:, :, 0]
        return convert_3_channel(ret)
    else:
        raise BaseException('unknown image shape: ' + str(img.shape))


def copy_img(img):
    return img.copy()


def new_image(shape, fill=255):
    zero_img = np.zeros(shape, np.uint8)
    ret = np.add(zero_img, fill)
    return ret.astype(np.uint8)


def rotation(img, angle, fill=(255, 255, 255)):
    h, w = img.shape
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    return cv2.warpAffine(img, m, (w, h), borderValue=fill)


def translation(img, h_offset=0, w_offset=0, fill=(255, 255, 255)):
    h, w = img.shape
    m = np.float32([[1, 0, w_offset], [0, 1, h_offset]])
    return cv2.warpAffine(img, m, (w, h), borderValue=fill)


def joins(imgs, axis=0):
    """
    图片合并
    :param axis: 0 垂直合并, 1 水平合并
    """
    return np.concatenate(imgs, axis=axis)


def filters(img, code=0):
    """
    图像滤波
    :param code: 0~5 SmoothMore,Smooth,锐化,中值滤波,Blur,BoxBlur
    """
    ret = Image.fromarray(img)
    filter_list = [ImageFilter.SMOOTH_MORE, ImageFilter.SMOOTH, ImageFilter.SHARPEN,
                   ImageFilter.MedianFilter, ImageFilter.BLUR, ImageFilter.BoxBlur]
    ret = ret.filter(filter_list[code])
    return np.array(ret)


def bilateral_filter(img, d=40):
    """
    双边滤波
    :param d:
    """
    return cv2.bilateralFilter(img, d, 75, 75)


def contrast(img, contrast_val):
    img = Image.fromarray(img)
    enh_con = ImageEnhance.Contrast(img)
    return np.array(enh_con.enhance(contrast_val))


def flip_heigt(img, code=0):
    """
    图像翻转
    :param code: 0 垂直翻转, 1 水平翻转
    """
    return cv2.flip(img,flipCode=code)
