import cv2 as cv2
import numpy as np
import os
from PIL import Image
from PIL import ImageStat


def brightness(filename):
    im = Image.open(filename).convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]


def change_brightness(img):
    w = img.shape[1]
    h = img.shape[0]
    for xi in range(0, w):
        for xj in range(0, h):
            img[xj, xi, 0] = int(img[xj, xi, 0] * 2)
            img[xj, xi, 1] = int(img[xj, xi, 0] * 2)
            img[xj, xi, 2] = int(img[xj, xi, 0] * 2)
    return img


def template(fn_tpl, fn_target):
    tpl = cv2.imread(fn_tpl)
    target = cv2.imread(fn_target)
    cv2.namedWindow('template image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('target image', cv2.WINDOW_NORMAL)
    if brightness(fn_target) < 50:
        target = change_brightness(target)
    # tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    # target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    # tpl = cv2.Canny(tpl, 100, 200)
    # target = cv2.Canny(target, 100, 200)
    cv2.imshow("target image", target)
    cv2.imshow("template image", tpl)
    methods = [cv2.TM_CCOEFF]
    # methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
    th, tw = tpl.shape[:2]
    for md in methods:
        print(md)
        result = cv2.matchTemplate(target, tpl, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if md == cv2.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0] + tw, tl[1] + th)  # br是矩形右下角的点的坐标
        cv2.rectangle(target, tl, br, (0, 0, 255), 2)
        cv2.namedWindow("match-" + np.str(md), cv2.WINDOW_NORMAL)
        cv2.imshow("match-" + np.str(md), target)
        cv2.imwrite("match-" + np.str(md) + ".png", target)


def adjust(data_base_dir):
    def gamma_trans(img, gamma):  # gamma函数处理
        gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  # 建立映射表
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  # 颜色值为整数
        return cv2.LUT(img, gamma_table)  # 图片颜色查表。另外可以根据光强（颜色）均匀化原则设计自适应算法。

    def nothing(x):
        pass

    cv2.namedWindow("demo", 0)  # 将显示窗口的大小适应于显示器的分辨率
    cv2.createTrackbar('Value of Gamma', 'demo', 100, 1000, nothing)  # 使用滑动条动态调节参数gamma

    outfile_dir = "E:/imageload"  # 输出文件夹的路径
    processed_number = 0  # 统计处理图片的数量
    print("press enter to make sure your operation and process the next picture")

    for file in os.listdir(data_base_dir):  # 遍历目标文件夹图片
        read_img_name = data_base_dir + file.strip()  # 取图片完整路径
        image = cv2.imread(read_img_name)  # 读入图片
        while 1:
            value_of_gamma = cv2.getTrackbarPos('Value of Gamma', 'demo')  # gamma取值
            value_of_gamma = value_of_gamma * 0.01  # 压缩gamma范围，以进行精细调整
            image_gamma_correct = gamma_trans(image, value_of_gamma)  # 2.5为gamma函数的指数值，大于1曝光度下降，大于0小于1曝光度增强
            cv2.imshow("demo", image_gamma_correct)
            k = cv2.waitKey(1)
            if k == 13:  # 按回车键确认处理、保存图片到输出文件夹和读取下一张图片
                processed_number += 1
                out_img_name = outfile_dir + '/' + file.strip()
                cv2.imwrite(out_img_name+".png", image_gamma_correct)
                print("The number of photos which were processed is ", processed_number)
                break


if __name__ == '__main__':
    fn_tpl = "E:/imageload/sample3.png"
    fn_target = "E:/imageload/target1.jpg"
    # adjust(fn_target)
    template(fn_tpl, fn_target)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
