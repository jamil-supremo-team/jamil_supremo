import cv2 as cv

Gray = cv.imread("1.jpg", 0) 
cv.imshow("Gray",Gray)

cv.waitKey(0)
cv.destroyAllWindows()

