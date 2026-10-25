import cv2

def resize_img(img, width, height):
    up_points = (width, height)
    img_resize = cv2.resize(img, up_points)
    return img_resize

if __name__ == "__main__":
    img = cv2.imread("assets\img1.jpg")
    rimg = resize_img(img, 500, 500)
    cv2.imshow("resize image", rimg)
    cv2.waitKey(0)


