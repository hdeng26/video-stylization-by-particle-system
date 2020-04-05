import numpy as np
import cv2
import time
import algbp
import particle
import particleList

def processFrame(img, outputIntensity):

    #img = cv2.imread('test1.jpg', 0)

    canvas_height = img.shape[0]
    canvas_width = img.shape[1]
    cannyX = cv2.Canny(img, 30, 150)
    image_mean = img.mean()


    xList = particleList.particleList()
    x = img.shape[0]

    threshold_base = outputIntensity
    bearing = 0

    for i in range(0, x, threshold_base):
        curP = particle.particle(prev=None, nex=None, vector=(i, 0), bearing=0, threshold=threshold_base, direction=0)
        xList.insert2Last(curP)

    proceedFrameX = algbp.update(xList, img, cannyX, threshold_base)

    '''**************************************************second layer'''
    #print("foreground layer!")
    inputX = img
    _, inputX = cv2.threshold(inputX, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    inputY = np.rot90(inputX, 1)
    yList = particleList.particleList()

    inputY = np.uint8(inputY)
    cannyY = cv2.Canny(inputY, 30, 150)
    y = inputY.shape[0]
    for i in range(0, y, threshold_base):
        curP = particle.particle(prev=None, nex=None, vector=(i, 0), bearing=0, threshold=threshold_base, direction=0)
        yList.insert2Last(curP)

    proceedFrameY = algbp.update(yList, inputY, cannyY, threshold_base)
    rotationY = np.rot90(proceedFrameY, 3)

    for y in range(0, rotationY.shape[0]):
        for x in range(0, rotationY.shape[1]):
            # threshold the pixel
            if proceedFrameX[y, x] != 255:  
                rotationY[y, x] = 0
    return rotationY


outputIntensity = algbp.outputIntensity
time_start = time.time()

cap = cv2.VideoCapture('draft.mp4')
ret1, frame1 = cap.read()
prvs = cv2.GaussianBlur(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY),(5,5),0)
baseOutput = processFrame(prvs, outputIntensity)
time_base = time.time()
print('time cost', time_base-time_start, 's')
out = cv2.VideoWriter('output.avi', -1, 30, (int(cap.get(3)),int(cap.get(4))))
count = 0
width = int(cap.get(3))
height = int(cap.get(4))

while(cap.isOpened()):
    # Capture frame-by-frame
    ret2, frame2 = cap.read()
    if not ret1 or not ret2:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    next = cv2.GaussianBlur(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY),(5,5),0)
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    # mag[mag < (mag.mean()*1.8)] = 0
    # mag = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    mag = np.uint8(mag)

    _, mag = cv2.threshold(mag, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    if count % 2 == 0:
        prev_mag = mag
    else:
        mag[prev_mag > 0] = 255
        prev_mag = mag

    cv2.imshow('mag', mag)
    
    newFrame = np.zeros_like(baseOutput)
    for y in range(0, baseOutput.shape[0]):
        for x in range(0, baseOutput.shape[1]):
            if y+int(flow[y][x][1]) < baseOutput.shape[0] and x+int(flow[y][x][0]) < baseOutput.shape[1]:
                newFrame[y+int(flow[y][x][1])][x+int(flow[y][x][0])] = baseOutput[y][x]

    count += 1
    print(count)

    if count % 10 == 0:
        dynamic_style = processFrame(next, outputIntensity)
        for y in range(0, newFrame.shape[0]):
            for x in range(0, newFrame.shape[1]):
                if mag[y][x] > 0:
                    newFrame[y][x] = dynamic_style[y][x]
                    baseOutput[y][x] = dynamic_style[y][x]

    cv2.imshow('frameNew', newFrame)

    # output video
    out.write(np.uint8(newFrame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    prvs = next
time_end = time.time()
print('time cost', time_end-time_start, 's')


# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

