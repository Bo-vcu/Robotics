import cv2 as cv

def draw_circle(event,x,y,flags,param):
 if event == cv.EVENT_LBUTTONDBLCLK:
    cv.circle(img,(x,y),100,(255,0,0),-1)


img = cv.imread("testimage.jpg")
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)

while(1):
    cv.imshow('image',img)       
    if cv.waitKey(5) & 0xFF == 27:
        cv.imwrite("output.png", img)
        break
cv.destroyAllWindows()