import cv2 as cv

img = cv.imread("1.jpg")
girar = 1

while girar <= 5:
    cv.imshow("final", img)
    cv.waitKey(0)
    
    if girar == 5:
        cv.destroyAllWindows()
        girar = 6
    else:
        img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
        girar = girar + 1