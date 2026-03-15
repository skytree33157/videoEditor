import cv2 as cv
import numpy as np
import os
import datetime
def on_trackbar(val):
    pass

video=cv.VideoCapture(0)
windowName='videoEditor'
target_format='avi'
target_fourcc='XVID'
up_pressed=False
left_pressed=False
brightTrack = 'bright'
contrastTrack='contrast'
negativeTrack='negative'
date= datetime.datetime.now().strftime('%y%m%d_%H%M%S')
saveURL=os.path.join(os.path.expanduser('~'),'Videos','videoEditor')
os.makedirs(saveURL, exist_ok=True)
filename='videoEditor'

cv.namedWindow(windowName)
cv.createTrackbar(negativeTrack,windowName,0,100,on_trackbar)
cv.createTrackbar(brightTrack,windowName,0,100,on_trackbar)
cv.createTrackbar(contrastTrack,windowName,0,100,on_trackbar)

if video.isOpened():
    target = cv.VideoWriter()
    img_record = None

    while True:
        valid, img = video.read()
        if not valid:
            break
        img_pre=img.copy()
        key=cv.waitKey(1)
        negativeColor = cv.getTrackbarPos(negativeTrack,windowName)/100
        bright=cv.getTrackbarPos(brightTrack,windowName)-50
        contrast=cv.getTrackbarPos(contrastTrack,windowName)/50
        img_cpy=img.astype(np.float32)
        img_cpy=contrast*img+bright
        img_cpy=(img_cpy*(1-negativeColor)+(255-img_cpy)*negativeColor)
        img_cpy=np.clip(img_cpy,0,255).astype(np.uint8)

        #스페이스바
        if key==32:
            #녹화 안 하고 있었다면
            if not target.isOpened():
                #트랙바 이동
                cv.setTrackbarPos(negativeTrack,windowName,0)
                cv.setTrackbarPos(brightTrack,windowName,50)
                cv.setTrackbarPos(contrastTrack,windowName,50)
                #녹화 파일
                target_file=saveURL+'/'+filename+'_'+date+'.'+target_format
                fps=video.get(cv.CAP_PROP_FPS)
                h,w,*_=img_pre.shape
                is_color=(img_pre.ndim>2)and (img_pre.shape[2]>1)
                target.open(target_file, cv.VideoWriter_fourcc(*target_fourcc),fps,(w,h),is_color)
            #녹화 중이었다면
            else:
                #초기화
                target.release()
                img_record=img.copy()
                up_pressed=False
                left_pressed=False
                cv.setTrackbarPos(negativeTrack,windowName,0)
        
        #상하좌우 반전 키
        if key==ord('w') or key==ord('s'):
            up_pressed = not up_pressed
        if key==ord('a') or key==ord('d'):
            left_pressed = not left_pressed

        #녹화 중이면
        if target.isOpened():
            cv.circle(img_pre, (195,23), 10,color=(0,0,255),thickness=-1)
            cv.putText(img_pre, 'Recording', (20,30), cv.FONT_HERSHEY_DUPLEX, 1, (0,0,0), thickness=2)
            cv.putText(img_pre, 'Recording', (20,30), cv.FONT_HERSHEY_DUPLEX, 1, (255,255,255))
            img_record=img_cpy.copy()
            if up_pressed == True:
                img_record=cv.flip(img_record,0)
            if left_pressed == True:
                img_record=cv.flip(img_record,1)
        else:
            cv.putText(img_pre, 'Preview', (20,30), cv.FONT_HERSHEY_DUPLEX, 1, (0,0,0), thickness = 2)
            cv.putText(img_pre, 'Preview', (20,30), cv.FONT_HERSHEY_DUPLEX, 1, (255,255,255))
            img_record=np.zeros_like(img)
        
        merge = np.hstack((img_pre,img_record))
        target.write(img_record)
        cv.imshow(windowName, merge)

        if key==27:
            break
        
        
    target.release()
    video.release()
    cv.destroyAllWindows()