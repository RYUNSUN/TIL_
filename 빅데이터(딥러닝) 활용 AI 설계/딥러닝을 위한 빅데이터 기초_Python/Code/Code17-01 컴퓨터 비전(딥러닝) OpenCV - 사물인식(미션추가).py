from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from tkinter import messagebox
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import cv2

# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h,w,initValue=0) :
    retMemory = []
    for _ in range(h) :
        tmpList=[]
        for _ in range(w) :
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

# 파일을 메모리로 로딩하는 함수
def loadImageColor(fnameOrCvData) : # 파일명 or OpenCV 개체
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    global photo, cvPhoto # pillow 활용시 쓰기 위해
    inImage=[]
    ####################################
    ## PIL 개체 --> OpenCV 개체로 복사 ##
    ####################################
    if type(fnameOrCvData) == str : # 문자열 일때는 filename
        cvData = cv2.imread(fnameOrCvData) # 파일 --> CV 개체
    else :
        cvData = fnameOrCvData
    cvPhoto = cv2.cvtColor(cvData, cv2.COLOR_BGR2RGB) # 중요! CV 개체
    photo = Image.fromarray(cvPhoto)# 중요! PIL 객체
    inW = photo.width
    inH = photo.height
    ###################################
    ## 메모리 확보 ##
    for _ in range(3):
        inImage.append(malloc(inH,inW))

    photoRGB = photo.convert('RGB')
    for i in range(inH) :
        for k in range(inW) :
            r, g, b = photoRGB.getpixel((k,i))
            inImage[R][i][k] = r
            inImage[G][i][k] = g
            inImage[B][i][k] = b

# 파일을 선택해서 메모리로 로딩하는 함수
def openImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window,filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadImageColor(filename)
    equalImageColor()

    displayImageColor()

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    global VIEW_X, VIEW_Y
    # VIEW_X, VIEW_Y = 512, 512
    ## 고정된 화면 크기
    # 가로/세로 비율 계산
    ratio = outH / outW
    if ratio < 1:
        VIEW_X = int(1024 * ratio)
    else:
        VIEW_X = 1024
    if ratio > 1:
        VIEW_Y = int(1024 * ratio)
    else:
        VIEW_Y = 1024

    if outH <= VIEW_X :
        VIEW_X = outH; stepX = 1
    if outH > VIEW_X :
        if ratio < 1 :
            VIEW_X = int(1024 * ratio)
        else :
            VIEW_X = 1024
        stepX = outH / VIEW_X

    if outW <= VIEW_Y:
        VIEW_Y = outW; stepY = 1
    if outW > VIEW_Y:
        if ratio > 1 :
            VIEW_Y = int(1024 * ratio)
        else :
            VIEW_Y = 1024

        stepY = outW / VIEW_Y

    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_X, width=VIEW_Y)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, stepX) :
        tmpStr = ''
        for k in numpy.arange(0,outW, stepY) :
            i = int(i); k = int(k)
            r , g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

import numpy as np
def saveImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    if outImage == None :
        return
    outArray = []
    for i in range(outH) :
        tmpList=[]
        for k in range(outW) :
            tup = tuple([outImage[R][i][k],outImage[G][i][k],outImage[B][i][k]])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8),'RGB') # fromarry :  NumPy 배열을 Image 객체로 바꿀 때

    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension='.'
                               , filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    savePhoto.save(saveFp.name)
    print('Save~')

# 동일영상 알고리즘
def equalImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ## 메모리 할당 ##
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH,outW))
    ##############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    ##############################
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = inImage[RGB][i][k]
    ######################################

    displayImageColor()


def addImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ## 메모리 할당 ##
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH,outW))
    ##############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    ##############################
    value = askinteger("밝게/어둡게","값( -->",minvalue=-255,maxvalue=255)
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] + value > 255:
                    outImage[RGB][i][k] = 255
                elif inImage[RGB][i][k] + value < 0:
                    outImage[RGB][i][k] = 0
                else :
                    outImage[RGB][i][k] = inImage[RGB][i][k] + value
    ######################################

    displayImageColor()

def revImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ## 메모리 할당 ##
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH,outW))
    ##############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    ##############################
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255-inImage[RGB][i][k]
    ######################################

    displayImageColor()

def paraImageColor():
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ## 메모리 할당 ##
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH,outW))
    ##############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    ##############################
    LUT = [0 for _ in range(256)]
    for input in range(256) :
        LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]
    ######################################

    displayImageColor()


def morphImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    inImage2 = []
    photo2 = Image.open(filename2)  # PIL 객체
    inW2 = photo2.width;
    inH2 = photo2.height
    ## 메모리 확보
    for _ in range(3):
        inImage2.append(malloc(inH2, inW2))

    photoRGB2 = photo2.convert('RGB')
    for i in range(inH2):
        for k in range(inW2):
            r, g, b = photoRGB2.getpixel((k, i))
            inImage2[R][i][k] = r
            inImage2[G][i][k] = g
            inImage2[B][i][k] = b

    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for RGB in range(3):
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[RGB][i][k] = newValue
            displayImageColor()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()

# 상하반전 알고리즘
def upDownImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][inH-i-1][k] = inImage[RGB][i][k]

    displayImageColor()

# 영상 축소 알고리즘
def zoomOutImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    scale = askinteger("축소","값 -->",minvalue=2,maxvalue=16)
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH//scale
    outW = inW//scale
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i*scale][k*scale]

    displayImageColor()

# 영상 확대 알고리즘
def zoomInImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    scale = askinteger("확대","값 -->",minvalue=2,maxvalue=4)
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH*scale
    outW = inW*scale
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i//scale][k//scale]

    displayImageColor()

## 마우스 화면이동 알고리즘
def moveImageColor() :
    global panYN
    panYN = True
    canvas.configure(cursor = 'mouse')

def mouseClick(event) :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH,sx,sy,ex,ey,panYN
    if panYN == False :
        return
    sx = event.x
    sy = event.y

def mouseDrop(event) :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH,sx,sy,ex,ey,panYN
    if panYN == False :
        return
    ex = event.x
    ey = event.y
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    mx = sx - ex
    my = sy - ey
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                if 0 <= i-my < outH and 0 <= k-mx < outW :
                    outImage[RGB][i-my][k-mx] = inImage[RGB][i][k]
    panYN = False
    ## 출력
    displayImageColor()

# 화소점 처리 알고리즘(이진화)
def binaryImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    ##영상의 평균 구하기
    grayImage = []
    tmp = []
    sum = 0

    for i in range(inH) :
        tmp = []
        for k in range(inW) :
            gray = int((inImage[R][i][k]+inImage[G][i][k]+inImage[B][i][k])//3)
            if gray > 255 :
                gray = 255
            elif gray < 0 :
                gray = 0
            else :
                gray = gray
            sum += gray
            tmp.append(gray)
        grayImage.append(tmp)
    avg = sum // (inW * inH)

    for RGB in range(3) :
        outImage[RGB] = grayImage

    for GRB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                if outImage[RGB][i][k] > avg :
                    outImage[RGB][i][k] = 255
                else :
                    outImage[RGB][i][k] = 0

    displayImageColor()

# 오른쪽 90도 회전 알고리즘
def rotationImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][k][inW-i-1] = inImage[RGB][i][k]
    ## 출력
    displayImageColor()

# 영상 회전 알고리즘
def rotateImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    angle = askinteger("회전","값 -->",minvalue=1,maxvalue=360)
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180 # radian degree 수식
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                xs = i
                ys = k
                xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
                yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
                if 0<= xd < inH and 0 <= yd < inW :
                    outImage[RGB][xd][yd] = inImage[RGB][i][k]

    displayImageColor()

# 영상 회전 알고리즘
def rotateImageColor2() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    angle = askinteger("회전","값 -->",minvalue=1,maxvalue=360)
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW // 2;
    cy = inH // 2
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                xs = i;
                ys = k;
                xd = int(math.cos(radian) * (xs - cx) - math.sin(radian) * (ys - cy)) + cx
                yd = int(math.sin(radian) * (xs - cx) + math.cos(radian) * (ys - cy)) + cy
                if 0 <= xd < outH and 0 <= yd < outW:
                    outImage[RGB][xs][ys] = inImage[RGB][xd][yd]
                else:
                    outImage[RGB][xs][ys] = 255

    displayImageColor()

# 엠보싱 처리(RGB)
def embossImageRGB() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage, tmpOutImage = [],[] #[]*2 하면 메모리를 공유하므로 버그 발생
    for _ in range(3):
        tmpInImage.append(malloc(inH + MSIZE -1, inW + MSIZE -1, 127))
    for _ in range(3):
        tmpOutImage .append(malloc(outH, outW))

    ## 원 입력 ---> 임시 입력
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
    ## 회선연산 : (1,1)이 중심
    for RGB in range(3):
        for i in range(MSIZE//2,inH+MSIZE//2) :
            for k in range(MSIZE//2,inW+MSIZE//2) :
                # 각 점을 처리
                s = 0.0
                for m in range(0 ,MSIZE) :
                    for n in range(0,MSIZE) :
                        s += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2] # 마스크와 영상과 자리 맞추기
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = s

    ## 127 더하기 (선택)
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                tmpOutImage[RGB][i][k] += 127

    ## 임시 출력 --> 원 출력
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                value = tmpOutImage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()

# 엠보싱 처리(Pillow)
def embossImagePillow() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    global photo
    ## 중요! 코드, 출력영상 크기 결정##
    photo2 = photo.copy()
    photo2 = photo.filter(ImageFilter.EMBOSS)
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 임시 출력 --> 원 출력
    for i in range(outH) :
        for k in range(outW) :
            r, g, b = photo2.getpixel((k,i))
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b

    displayImageColor()

import colorsys
sx, sy, ex, ey = [0] * 4
# 엠보싱 처리(HSV)
def embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey
    ## 이벤트 바인드
    canvas.bind('<Button-3>', rightMouseClick_embossImageHSV)
    canvas.bind('<Button-1>', leftMouseClick)
    canvas.bind('<B1-Motion>', leftMouseMove) # 움직이는 거
    canvas.bind('<ButtonRelease-1>', leftMouseDrop_embossImageHSV)
    canvas.configure(cursor = 'mouse')

def rightMouseClick_embossImageHSV(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey
    sx = 0 ; sy = 0;
    ex = inW-1 # 그림의 마지막 점까지 인정해주기 위해
    ey = inH-1
    ###################
    __embossImageHSV()
    ###################
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind('<ButtonRelease-1>')

def leftMouseClick(event):
    global sx, sy, ex, ey
    sx = event.x # 그림의 마지막 점까지 인정해주기 위해
    sy = event.y

boxLine = None
def leftMouseMove(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, boxLine
    ex = event.x; ey = event.y
    if not boxLine :
        pass
    else :
        canvas.delete(boxLine)
    boxLine = canvas.create_rectangle(sx, sy, ex, ey,fill=None)

def leftMouseDrop_embossImageHSV(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    ex = event.x;    ey = event.y
    ##################
    __embossImageHSV()
    ##################
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind('<ButtonRelease-1>')

def __embossImageHSV():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 입력 RGB --> 입력 HSV (원 영상의 RGB 모델을 HSV모델로 변환)
    # 메모리 확보
    inImageHSV = []
    for _ in range(3):
        inImageHSV.append(malloc(inH,inW))
    #RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r,g,b = inImage[R][i][k],inImage[G][i][k],inImage[B][i][k]
            h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
            inImageHSV[0][i][k],inImageHSV[1][i][k],inImageHSV[2][i][k] = h, s, v

    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [[-1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]]
    ## 임시 입력영상 메모리 확보
    tmpInImageV, tmpOutImageV = [], []  # []*2 하면 메모리를 공유하므로 버그 발생
    tmpInImageV=malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127)#h,s,v 에서 v만 가져오기
    tmpOutImageV=malloc(outH, outW)
    ## 원 입력 ---> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImageV[i + MSIZE // 2][k + MSIZE // 2] = inImageHSV[2][i][k]
    ## 회선연산 : (1,1)이 중심
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점을 처리
            s = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    s += mask[m][n] * tmpInImageV[i + m - MSIZE // 2][k + n - MSIZE // 2]  # 마스크와 영상과 자리 맞추기
            tmpOutImageV[i - MSIZE // 2][k - MSIZE // 2] = s*255

    ## 127 더하기 (선택)
    for i in range(outH):
        for k in range(outW) :
            tmpOutImageV[i][k] += 127
            if tmpOutImageV[i][k] > 255 :
                tmpOutImageV[i][k] = 255
            elif tmpOutImageV[i][k] < 0:
                tmpOutImageV[i][k] = 0


    ## HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            if sx <= k <= ex and sy <= i <= ey : # 범위에 포함되면
                h, s, v = inImageHSV[0][i][k],inImageHSV[1][i][k],tmpOutImageV[i][k]
                r, g, v = colorsys.hsv_to_rgb(h, s, v)
                outImage[R][i][k],outImage[G][i][k],outImage[B][i][k] = int(r), int(g), int(b)
            else :
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = inImage[R][i][k],inImage[G][i][k],inImage[B][i][k]

    displayImageColor()

def sharpImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [[0., -1, 0],
            [-1, 5, -1],
            [0, -1, 0]]  # 뒤에 . 붙이는 걸 권장
    ## 임시 입력영상 메모리 확보
    tmpInImage, tmpOutImage = [], []  # []*2 하면 메모리를 공유하므로 버그 발생
    for _ in range(3):
        tmpInImage.append(malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127))
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))

    ## 원 입력 ---> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[RGB][i + MSIZE // 2][k + MSIZE // 2] = inImage[RGB][i][k]
    ## 회선연산 : (1,1)이 중심
    for RGB in range(3):
        for i in range(MSIZE // 2, inH + MSIZE // 2):
            for k in range(MSIZE // 2, inW + MSIZE // 2):
                # 각 점을 처리
                s = 0.0
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        s += mask[m][n] * tmpInImage[RGB][i + m - MSIZE // 2][k + n - MSIZE // 2]  # 마스크와 영상과 자리 맞추기
                tmpOutImage[RGB][i - MSIZE // 2][k - MSIZE // 2] = s

    ## 임시 출력 --> 원 출력
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImage[RGB][i][k] = int(value)

    ## 출력
    displayImageColor()


# 블러링 처리(RGB)
def blurImageRGB() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [ 1/9., 1/9., 1/9.],
             [ 1/9., 1/9., 1/9.],
             [ 1/9., 1/9., 1/9.] ] # 뒤에 . 붙이는 걸 권장
    ## 임시 입력영상 메모리 확보
    tmpInImage, tmpOutImage = [],[] #[]*2 하면 메모리를 공유하므로 버그 발생
    for _ in range(3):
        tmpInImage.append(malloc(inH + MSIZE -1, inW + MSIZE -1, 127))
    for _ in range(3):
        tmpOutImage .append(malloc(outH, outW))

    ## 원 입력 ---> 임시 입력
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
    ## 회선연산 : (1,1)이 중심
    for RGB in range(3):
        for i in range(MSIZE//2,inH+MSIZE//2) :
            for k in range(MSIZE//2,inW+MSIZE//2) :
                # 각 점을 처리
                s = 0.0
                for m in range(0 ,MSIZE) :
                    for n in range(0,MSIZE) :
                        s += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2] # 마스크와 영상과 자리 맞추기
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = s

    ## 임시 출력 --> 원 출력
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                value = tmpOutImage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)


    ## 출력
    displayImageColor()


def addSValuePillow() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    global photo
    ## 중요! 코드, 출력영상 크기 결정##
    value = askfloat("","0~1~10") # 1보다 커지면 채도가 진해짐
    photo2 = photo.copy()
    photo2 = ImageEnhance.Color(photo2)
    photo2 = photo2.enhance((value))
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 임시 출력 --> 원 출력
    for i in range(outH) :
        for k in range(outW) :
            r, g, b = photo2.getpixel((k,i))
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b

    displayImageColor()


def addSValueHSV():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 입력 RGB --> 입력 HSV (원 영상의 RGB 모델을 HSV모델로 변환)
    # 메모리 확보
    inImageHSV = []
    for _ in range(3):
        inImageHSV.append(malloc(inH, inW))
    # RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v

    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH
    outW = inW
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    value = askfloat("","-255~255") # -255 ~ 255
    value /= 255
    ## 임시 입력영상 메모리 확보
    ## HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            newS = inImageHSV[1][i][k] + value
            if newS < 0 :
                newS = 0
            elif newS > 1.0 :
                newS = 1.0
            h, s, v = inImageHSV[0][i][k], newS, inImageHSV[2][i][k]*255
            r, g, v = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(v)

    displayImageColor()

# 히스토그램
import matplotlib.pyplot as plt
def histoImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    rCountList = [0] * 256
    gCountList =[0] * 256
    bCountList = [0] * 256

    for i in range(inH) :
        for k in range(inW) :
            rCountList[inImage[R][i][k]] += 1

    for i in range(outH) :
        for k in range(outW) :
            gCountList[inImage[G][i][k]] += 1

    for i in range(outH) :
        for k in range(outW) :
            bCountList[inImage[B][i][k]] += 1

    plt.plot(rCountList)
    plt.plot(gCountList)
    plt.plot(bCountList)
    plt.show()

# 파일을 메모리로 로딩하는 함수
def loadCSVColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = 0
    fp = open(fname,'r')
    for _ in fp :
        fsize += 1
    inH = inW = int(math.sqrt(fsize/3)) # 핵심 코드
    fp.close()
    ## 입력영상 메모리 확보 ##
    inImage=[]
    for _ in range(3):
        inImage.append(malloc(inH, inW))
    # 파일 --> 메모리
    with open(fname, 'r') as rFp:
        for row_list in rFp :
            RGB, row, col, value = list(map(int,row_list.strip().split(',')))
            inImage[RGB][row][col] = value



# 파일을 선택해서 메모리로 로딩하는 함수
def openCSVColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return

    loadCSVColor(filename)
    equalImageColor()

# 파일을 선택해서 메모리로 로딩하는 함수
# p.353
import csv
def saveCSVColor() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension='*.csv'
                           , filetypes=(("CSV 파일", "*.csv"), ("모든파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    with open (saveFp.name,'w',newline='') as wFp :
        csvWriter = csv.writer(wFp)
        for RGB in range(3):
            for i in range(outH):
                for k in range(outW):
                   row_list = [RGB,i, k, outImage[RGB][i][k]]
                   csvWriter.writerow(row_list)

    print('csv.save ok~')

# 파일을 선택해서 메모리로 로딩하는 함수
import xlwt
def saveExcelColor() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension='*.xls'
                           , filetypes=(("XLS 파일", "*.xls"), ("모든파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)
    wb = xlwt.Workbook()
    ws_1 = wb.add_sheet(sheetName)
    ws = wb.add_sheet(sheetName)
    ws = wb.add_sheet(sheetName)

    for i in range(outH) :
        for k in range(outW) :
            ws.write(i, k, outImage[i][k])

    wb.save(xlsName)
    print('csv.save ok~')

import struct
## 임시 경로에 outImage를 저장하기.
import random
def saveTempImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + os.path.basename(filename)
    if saveFp == '' or saveFp == None:
        return
    # print(saveFp)
    saveFp = open(saveFp, mode='wb')
    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')

    savePhoto.save(saveFp.name)
    saveFp.close()
    return saveFp



# def findStat(fname):
#     # 파일 열고, 읽기.
#     fsize = os.path.getsize(fname)  # 파일의 크기(바이트)
#     inH = inW = int(math.sqrt(fsize))  # 핵심 코드
#     ## 입력영상 메모리 확보 ##
#     inImage = []
#     inImage = malloc(inH, inW)
#     # 파일 --> 메모리
#     with open(fname, 'rb') as rFp:
#         for i in range(inH):
#             for k in range(inW):
#                 inImage[i][k] = int(ord(rFp.read(1)))
#     sum = 0
#     for i in range(inH):
#         for k in range(inW):
#             sum += inImage[i][k]
#     avg = sum // (inW * inH)
#     maxVal = minVal = inImage[0][0]
#     for i in range(inH):
#         for k in range(inW):
#             if inImage[i][k] < minVal:
#                 minVal = inImage[i][k]
#             elif inImage[i][k] > maxVal:
#                 maxVal = inImage[i][k]
#     return avg, maxVal, minVal


import pymysql
IP_ADDR = '192.168.56.113';
USER_NAME = 'root';
USER_PASS = '1234'
DB_NAME = 'BigData_DB';
CHAR_SET = 'utf8'


def saveMysqlColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try:
        sql = '''
                CREATE TABLE colorimage_TBL(
                color_id INT AUTO_INCREMENT PRIMARY KEY,
                color_fname VARCHAR(30),
                color_extname CHAR(5),
                color_height SMALLINT, color_width SMALLINT,
                color_data LONGBLOB);
            '''
        cur.execute(sql)
    except:
        pass

    ## outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달.
    fullname = saveTempImage()
    fullname = fullname.name
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    print(height)
    sql = "INSERT INTO colorimage_TBL(color_id ,color_fname, color_extname, "
    sql += "color_height, color_width, color_data) "
    sql += " VALUES(NULL,'" + fname + "','" + extname + "',"
    sql += str(height) + "," + str(width)
    sql += ", %s )"
    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()
    os.remove(fullname)
    print("업로드 OK -->" + fullname)


def loadMysqlColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT color_id, color_fname, color_extname,  color_height, color_width "
    sql += "FROM colorimage_TBL"
    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [ ':'.join(map(str,row)) for row in queryList]
    import tempfile
    def selectRecord( ) :
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]
        subWindow.destroy()
        color_id = queryList[selIndex][0]
        sql = "SELECT color_fname, color_extname, color_data FROM colorImage_TBL "
        sql += "WHERE color_id = " + str(color_id)
        cur.execute(sql)
        fname, extname, binData = cur.fetchone()

        fullPath = tempfile.gettempdir() + '/' + fname + "." + extname
        with open(fullPath, 'wb') as wfp:
            wfp.write(binData)
        cur.close()
        con.close()

        loadImageColor(fullPath)
        equalImageColor()

    ## 서브 윈도에 목록 출력하기.
    subWindow = Toplevel(window)
    listbox = Listbox(subWindow)
    button = Button(subWindow, text='선택', command = selectRecord)

    for rowStr in rowList :
        listbox.insert(END, rowStr)

    listbox.pack(expand=1, anchor=CENTER)
    button.pack()
    subWindow.mainloop()

    cur.close()
    con.close()

######################################
##### OpenCV 용 컴퓨터 비전/딥러닝 ####
######################################
def toColorOutArray(pillowPhoto) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###### 메모리 할당 ################
    outH = pillowPhoto.height; outW = pillowPhoto.width
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    photoRGB = pillowPhoto.convert('RGB')
    for i in range(outH) :
        for k in range(outW) :
            r,g,b = photoRGB.getpixel((k,i))
            outImage[R][i][k],outImage[G][i][k],outImage[B][i][k]=r,g,b
    displayImageColor()

def embossOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None :
        return

    cvPhoto2 = cvPhoto[:]
    mask = np.zeros((3,3),np.float32)
    mask[0][0] = -1; mask[2][2] = 1;
    cvPhoto2 = cv2.filter2D(cvPhoto2,-1,mask)
    cvPhoto2 += 127
    photo2 = Image.fromarray(cvPhoto2) #PIL용 photo2로 보내서 출력
    toColorOutArray(photo2)

def greyscaleOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None :
        return
    ##이 부분이 OpenCV 처리 부분######################################
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    photo2 = Image.fromarray(cvPhoto2) #PIL용 photo2로 보내서 출력
    ################################################################
    toColorOutArray(photo2)

def blurOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None :
        return
    ##이 부분이 OpenCV 처리 부분######################################
    mSize = askinteger("블러링","마스크 크기:") # 마스크 크기는 홀수만 가능
    cvPhoto2 = cvPhoto[:]
    mask = np.ones((mSize, mSize), np.float32) / (mSize*mSize)
    cvPhoto2 = cv2.filter2D(cvPhoto2, -1, mask)
    photo2 = Image.fromarray(cvPhoto2) #PIL용 photo2로 보내서 출력
    ################################################################
    toColorOutArray(photo2)

def rotateOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None :
        return
    ##이 부분이 OpenCV 처리 부분######################################
    angle = askinteger("회전","각도: ")
    cvPhoto2 = cvPhoto[:]
    rotate_matrix = cv2.getRotationMatrix2D((outH//2, outW//2),angle,1) # 중앙점, 각도, 스케일(확대)
    cvPhoto2 = cv2.warpAffine(cvPhoto2, rotate_matrix, (outH, outW))
    photo2 = Image.fromarray(cvPhoto2) #PIL용 photo2로 보내서 출력
    ################################################################
    toColorOutArray(photo2)

def zoomInOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    scale = askfloat("확대/축소", "배수:")
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.resize(cvPhoto2, None, fx=scale, fy=scale)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def waveHorOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ##이 부분이 OpenCV 처리 부분######################################
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH) :
        for k in range(inW) :
            oy = int(15.0 * math.sin(2*3.14*k / 180))
            ox = 0
            if i+oy < inH :
                cvPhoto2[i][k] = cvPhoto [(i+oy) % inH][k]
            else :
                cvPhoto2[i][k] = 0
    photo2 = Image.fromarray(cvPhoto2)  # PIL용 photo2로 보내서 출력
    ################################################################
    toColorOutArray(photo2)

def waveVirOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            ox = int(25.0 * math.sin(2 * 3.14 * i / 180))
            oy = 0
            if k + ox < inW:
                cvPhoto2[i][k] = cvPhoto[i][(k + ox) % inW]
            else:
                cvPhoto2[i][k] = 0
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)


def cartoonOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ##이 부분이 OpenCV 처리 부분######################################
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    cyPhoto2 = cv2.medianBlur(cvPhoto2, 7)
    edges = cv2.Laplacian(cvPhoto2, cv2.CV_8U, ksize = 5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    cvPhoto2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    photo2 = Image.fromarray(cvPhoto2)  # PIL용 photo2로 보내서 출력
    ################################################################
    toColorOutArray(photo2)

def faceDetectOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        cv2.rectangle(cvPhoto2, (x, y), (x + w, y + w), (0, 255, 0), 3)

    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def hanibalOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    faceMask = cv2.imread("C:/images/images(ML)/mask_hannibal.png")
    h_mask, w_mask = faceMask.shape[:2]
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    for (x, y, w, h) in face_rects:
        if h> 0 and w > 0 :
            x = int(x + 0.1*w); y = int(y+0.4*h)
            w = int(0.8 *w) ; h = int(0.8*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w]
            faceMask_small = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA)
            grey_mask = cv2.cvtColor(faceMask_small, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(grey_mask, 50, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(faceMask_small, faceMask_small, mask=mask)
            maskedFrame = cv2.bitwise_and(cvPhoto2_2, cvPhoto2_2,mask_inv)
            cvPhoto2[y:y+h, x:x+w] = cv2.add(maskedFace, maskedFrame)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def catFaceDetectOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        cv2.rectangle(cvPhoto2, (x, y), (x + w, y + w), (0, 255, 0), 3)

    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def catHanibalOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
    faceMask = cv2.imread("C:/images/images(ML)/mask_hannibal.png")
    h_mask, w_mask = faceMask.shape[:2]
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    for (x, y, w, h) in face_rects:
        if h> 0 and w > 0 :
            x = int(x + 0.1*w); y = int(y+0.4*h)
            w = int(0.8 *w) ; h = int(0.8*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w]
            faceMask_small = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA)
            grey_mask = cv2.cvtColor(faceMask_small, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(grey_mask, 50, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(faceMask_small, faceMask_small, mask=mask)
            maskedFrame = cv2.bitwise_and(cvPhoto2_2, cvPhoto2_2,mask_inv)
            cvPhoto2[y:y+h, x:x+w] = cv2.add(maskedFace, maskedFrame)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def sunglassOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    sunglass = cv2.imread("C:/images/images(ML)/eye_sunglasses_1.jpg")
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    for (x, y, w, h) in face_rects:
        centers=[]
        roi_grey = grey[y:y+h, x:x+w]
        roi_color = cvPhoto2[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_grey)
        for (x_eye,y_eye,w_eye,h_eye)in eyes :
            # cv2.rectangle(roi_color, (x_eye,y_eye), (x_eye+w_eye,y_eye+h_eye), (0,255,0), 3)
            centers.append((x + int(x_eye + 0.5*w_eye), y + int(y_eye + 0.5*h_eye)))

        if len(centers) > 0:
            sunglass_width = 2.12*abs(centers[1][0]-centers[0][0])
            overlay_img =np.ones(cvPhoto2.shape, np.uint8) * 255
            h, w = sunglass.shape[:2]
            scaling_factor = sunglass_width / w
            overlay_sunglasses = cv2.resize(sunglass, None, fx=scaling_factor,
                                            fy=scaling_factor, interpolation=cv2.INTER_AREA)

            x = centers[0][0] if centers[0][0] < centers[1][0] else centers[1][0]
            x -= int(0.26 * overlay_sunglasses.shape[1])
            y += int(0.85 * overlay_sunglasses.shape[0])
            h, w = overlay_sunglasses.shape[:2]
            overlay_img[y:y + h, x:x + w] = overlay_sunglasses

            # create mask
            grey_sunglass = cv2.cvtColor(overlay_img, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(grey_sunglass, 110, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(cvPhoto2, cvPhoto2, mask=mask)
            maskedFrame = cv2.bitwise_and(overlay_img, overlay_img,mask = mask_inv)
            cvPhoto2 = cv2.add(maskedFace, maskedFrame)
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)

def moustacheOpenCV():
    import cv2
    import numpy as np
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    moustache_mask = cv2.imread("C:/images/images(ML)/moustache.png")
    h_mask, w_mask = moustache_mask.shape[:2]

    cvPhoto2 = cvPhoto[:]
    frame = cvPhoto2
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    mouth_rects = mouth_cascade.detectMultiScale(grey, 1.3, 5)
    for (x, y, w, h) in mouth_rects:
        if h> 0 and w > 0 :
            h, w = int(0.6 * h), int(1.2 * w)
            # x -= int(0.05*w)
            y -= int(0.45 * h)
            x = int(x + 0.2 * w);
            # y = int(y + 0.4 * h)
            # w = int(0.8 * w);
            # h = int(0.8 * h)
            frame_roi = frame[y:y + h, x:x + w]
            moustache_mask_small = cv2.resize(moustache_mask, (w, h), interpolation=cv2.INTER_AREA)

            gray_mask = cv2.cvtColor(moustache_mask_small, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray_mask, 50, 255, cv2.THRESH_BINARY_INV)
            mask_inv = cv2.bitwise_not(mask)
            masked_mouth = cv2.bitwise_and(moustache_mask_small, moustache_mask_small, mask=mask)
            masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask=mask_inv)
            frame[y:y + h, x:x + w] = cv2.add(masked_mouth, masked_frame)

    cvPhoto2 = frame
    photo2 = Image.fromarray(cvPhoto2)
    ###################################################
    toColorOutArray(photo2)



def deep1OpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    cvPhoto2 = cvPhoto[:] #OpenCV 개체
    ######### 고정해서 쓸 코드 ############
    CONF_VALUE= 0.2 # args["confidence"] : 샘플 돌렸을 때 기본 값이 0.2
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
    image = cvPhoto2
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    cvPhoto2 = image
#########################
    # 화면 출력
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArray(photo2)

def deep2OpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    global frame
    filename = askopenfilename(parent=window,
             filetypes=(("동영상 파일", "*.mp4"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    cap = cv2.VideoCapture(filename)
    s_factor = 0.5 # 화면 크기 비율

    frameCount = 0
    while True :
        ret, frame = cap.read() # 현재 한 장면
        if not ret :
            break
        frameCount += 1
        if frameCount % 8 == 0 :  # 8은 화면 속도 조절
            frame = cv2.resize(frame, None, fx =s_factor, fy=s_factor,
                               interpolation=cv2.INTER_AREA)
            ###########################
            CONF_VALUE = 0.2
            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                "sofa", "train", "tvmonitor"]
            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
            net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
            image = frame
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > CONF_VALUE:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(image, (startX, startY), (endX, endY),
                        COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            frame = image
            ############################
            cv2.imshow('Deep Learning', frame)
            c = cv2.waitKey(1)
            if c == 27 : # ESC키
                break
            elif c == ord('c') or c== ord('C') :
                captureVideo()
                window.update()

    cap.release()
    cv2.destroyAllWindows()

def captureVideo() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto, frame
    loadImageColor(frame)
    equalImageColor()

# 동영상 파일에서 입력한 사물이 가장 많이 출현한 화면 캡처 및 개수
def videoDeepMaxCountCV2() :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB
    global outImageR, outImageG, outImageB, filename, photo, cvPhoto

    global frame

    videoFilename = askopenfilename(parent=window, filetypes=(("동영상 파일", "*.mp4"), ("모든 파일", "*.*")))
    if videoFilename == "" or videoFilename == None :
        return

    targetClass = askstring('찾을 사물',
                            'background, aeroplane, bicycle, bird, boat, \nbottle, bus, car, cat, chair, cow, diningtable, \ndog, horse, motorbike, person, pottedplant, \nsheep, sofa, train, tvmonitor')

    cap = cv2.VideoCapture(videoFilename)
    ds_factor = 0.5

    frameCount = 0
    maxCount, maxConfidence = 0, 0 # 출현최대수, 사물인식확률

    while True:
        #time.sleep(0.1)

        ret, frame = cap.read()
        if not ret :
            break

        frameCount += 1
        if frameCount % 5 == 0 : # 화면출력 속도 조절
            frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)

            image = frame
            args = {'image': filename, 'prototxt': 'MobileNetSSD_deploy.prototxt.txt',
                    'model': 'MobileNetSSD_deploy.caffemodel', 'confidence': 0.5}

            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                       "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                       "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                       "sofa", "train", "tvmonitor"]

            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

            net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

            net.setInput(blob)
            detections = net.forward()

            count, countConfidence = 0, 0
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > args["confidence"]:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    if CLASSES[idx] == targetClass.strip() :
                        count += 1
                        countConfidence += confidence

                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y), cv2.FONT_ITALIC, 0.5, COLORS[idx], 2)

            frame = image
            cv2.imshow('DeepLearning', frame)

            # 센 개수가 최대면 화면 캡처
            if count > maxCount :
                maxCount = count; maxConfidence = countConfidence
                captureVideo()
                status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                window.update()
            elif count == maxCount :
                if countConfidence > maxConfidence :
                    maxCount = count; maxConfidence = countConfidence
                    captureVideo()
                    status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                    window.update()

            count = 0; countConfidence = 0

            c = cv2.waitKey(1)
            if c == 27 :
                break

    cap.release()
    cv2.destroyAllWindows()

# 동영상 파일에서 입력한 사물이 가장 많이 출현한 화면 캡처 및 개수 (히스토그램 평활화 추가)
def videoDeepMaxCountEqualCV2() :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB
    global outImageR, outImageG, outImageB, filename, photo, cvPhoto

    global frame

    videoFilename = askopenfilename(parent=window, filetypes=(("동영상 파일", "*.mp4"), ("모든 파일", "*.*")))
    if videoFilename == "" or videoFilename == None :
        return

    targetClass = askstring('찾을 사물',
                            'background, aeroplane, bicycle, bird, boat, \nbottle, bus, car, cat, chair, cow, diningtable, \ndog, horse, motorbike, person, pottedplant, \nsheep, sofa, train, tvmonitor')

    cap = cv2.VideoCapture(videoFilename)
    ds_factor = 0.5

    frameCount = 0
    maxCount, maxConfidence = 0, 0 # 출현최대수, 사물인식확률

    while True:
        #time.sleep(0.1)

        ret, frame = cap.read()
        if not ret :
            break

        frameCount += 1
        if frameCount % 5 == 0 : # 화면출력 속도 조절
            frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)

            ## 히스토그램 평활화를 통해서 처리
            hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsvimg)
            equalizedV = cv2.equalizeHist(v)
            # h,s,equalizedV를 합쳐서 새로운 hsv 이미지를 만듭니다.
            hsv2 = cv2.merge([h, s, equalizedV])
            # 마지막으로 hsv2를 다시 BGR 형태로 변경합니다.
            frame = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
            #########################################

            image = frame
            args = {'image': filename, 'prototxt': 'MobileNetSSD_deploy.prototxt.txt',
                    'model': 'MobileNetSSD_deploy.caffemodel', 'confidence': 0.5}

            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                       "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                       "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                       "sofa", "train", "tvmonitor"]

            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

            net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

            net.setInput(blob)
            detections = net.forward()

            count, countConfidence = 0, 0
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > args["confidence"]:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    if CLASSES[idx] == targetClass.strip() :
                        count += 1
                        countConfidence += confidence

                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y), cv2.FONT_ITALIC, 0.5, COLORS[idx], 2)

            frame = image
            cv2.imshow('DeepLearning', frame)

            # 센 개수가 최대면 화면 캡처
            if count > maxCount :
                maxCount = count; maxConfidence = countConfidence
                captureVideo()
                status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                window.update()
            elif count == maxCount :
                if countConfidence > maxConfidence :
                    maxCount = count; maxConfidence = countConfidence
                    captureVideo()
                    status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                    window.update()

            count = 0; countConfidence = 0

            c = cv2.waitKey(1)
            if c == 27 :
                break

    cap.release()
    cv2.destroyAllWindows()


# 동영상 파일에서 입력한 사물이 가장 많이 출현한 화면 캡처 및 개수 (히스토그램 평활화 추가)
# -->평활화 이전 화면을 보여줌 --> 결과를 사물별 저장
def videoDeepMaxCountEqualSaveObjectCV2() :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB
    global outImageR, outImageG, outImageB, filename, photo, cvPhoto

    global frame

    videoFilename = askopenfilename(parent=window, filetypes=(("동영상 파일", "*.mp4"), ("모든 파일", "*.*")))
    if videoFilename == "" or videoFilename == None :
        return

    targetClass = askstring('찾을 사물',
                            'background, aeroplane, bicycle, bird, boat, \nbottle, bus, car, cat, chair, cow, diningtable, \ndog, horse, motorbike, person, pottedplant, \nsheep, sofa, train, tvmonitor')

    cap = cv2.VideoCapture(videoFilename)
    ds_factor = 0.5

    frameCount = 0
    maxCount, maxConfidence = 0, 0 # 출현최대수, 사물인식확률
    findNameAndRect = [] # 찾은 사물 정보 : [ ['사물명', 신뢰도, [sx, sy, ex, ey]], ... ]
    findImage = None # 사각형 없는 최종 이미지
    while True:
        #time.sleep(0.1)

        ret, frame = cap.read()
        if not ret :
            break

        frameCount += 1
        tempfindNameAndRect = [] # 찾은 사물 정보 : [ ['사물명', 신뢰도, [sx, sy, ex, ey]], ... ]
        if frameCount % 10 == 0 : # 화면출력 속도 조절

            saveImage = frame[:]  # 사각형이 없는 평활화 이전 이미지 (원 크기영상)
            frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
            beforeImage = frame[:] # 평활화 이전의 이미지를 화면에 보여주기 위함 (1/2크기 영상)

            ## 히스토그램 평활화를 통해서 처리
            hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsvimg)
            equalizedV = cv2.equalizeHist(v)
            # h,s,equalizedV를 합쳐서 새로운 hsv 이미지를 만듭니다.
            hsv2 = cv2.merge([h, s, equalizedV])
            # 마지막으로 hsv2를 다시 BGR 형태로 변경합니다.
            frame = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
            #########################################
            image = frame # image는 평활화로 사용함
            args = {'image': filename, 'prototxt': 'MobileNetSSD_deploy.prototxt.txt',
                    'model': 'MobileNetSSD_deploy.caffemodel', 'confidence': 0.5}

            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                       "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                       "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                       "sofa", "train", "tvmonitor"]

            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

            net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

            net.setInput(blob)
            detections = net.forward()

            count, countConfidence = 0, 0
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > args["confidence"]:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    if CLASSES[idx] == targetClass.strip() :
                        count += 1
                        countConfidence += confidence
                        tempfindNameAndRect.append([CLASSES[idx], confidence, [startX, startY, endX, endY]])

                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(beforeImage, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(beforeImage, label, (startX, y), cv2.FONT_ITALIC, 0.5, COLORS[idx], 2)

            frame = beforeImage #화면에는 평활화 이전것을 보여줌
            cv2.imshow('DeepLearning', frame)

            # 센 개수가 최대면 화면 캡처
            if count > maxCount :
                maxCount = count; maxConfidence = countConfidence
                captureVideo()
                findNameAndRect = tempfindNameAndRect
                findImage = saveImage
                status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                window.update()
            elif count == maxCount :
                if countConfidence > maxConfidence :
                    maxCount = count; maxConfidence = countConfidence
                    captureVideo()
                    findNameAndRect = tempfindNameAndRect
                    findImage = saveImage
                    status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                    window.update()

            count = 0; countConfidence = 0

            c = cv2.waitKey(1)
            if c == 27 :
                break

    cap.release()
    cv2.destroyAllWindows()

    ###############################
    ## 최종 결과 화면에서 사물별로 저장한다.
    ###############################
    # findNameAndRect --> [['person', 0.9991334080696106, [366, 59, 459, 323]], ['person', 1.998100459575653, [68, 120, 206, 309]], ...
    findSubImages = [] # 잘라낸 사물 이미지 리스트
    import os.path
    index = 1
    for nameAndRect in findNameAndRect :
        x1, y1, x2, y2 = nameAndRect[2]

        x1 = 0 if x1 < 0 else x1 ; x2 = 0 if x2 < 0 else x2; y1 = 0 if y1 < 0 else y1; y2 = 0 if y2 < 0 else y2;
        sub = findImage[y1*2:y2*2, x1*2:x2*2] # resize를 1/2로 했으므로, 원영상 위치는 2배
        saveFname = os.path.basename(filename).split('.')[0]+ "_" +"{0:03d}".format(index) + "_" + nameAndRect[0] + "_" + "{0:03d}".format(int(nameAndRect[1]*100)) + ".png"
        cv2.imwrite('c:/temp/' + saveFname, sub)
        index += 1

    print('Save. OK!')
    # 해당 이미지를 저장한다.

# 동영상 파일에서 입력한 사물이 가장 많이 출현한 화면 캡처 및 개수 (히스토그램 평활화 추가)
# -->평활화 이전 화면을 보여줌 --> 결과를 사물별 저장 --> 저장하기 전에 얼굴만 추출(하르케스케이드)
def videoDeepMaxCountEqualSaveAndExtractFaceObjectCV2() :
    global window, canvas, paper, inW, inH, outW, outH, inImageR, inImageG, inImageB
    global outImageR, outImageG, outImageB, filename, photo, cvPhoto

    global frame

    videoFilename = askopenfilename(parent=window, filetypes=(("동영상 파일", "*.mp4"), ("모든 파일", "*.*")))
    if videoFilename == "" or videoFilename == None :
        return

    # targetClass = askstring('찾을 사물',
    #                         'background, aeroplane, bicycle, bird, boat, \nbottle, bus, car, cat, chair, cow, diningtable, \ndog, horse, motorbike, person, pottedplant, \nsheep, sofa, train, tvmonitor')
    targetClass = 'person'
    cap = cv2.VideoCapture(videoFilename)
    ds_factor = 0.5

    frameCount = 0
    maxCount, maxConfidence = 0, 0 # 출현최대수, 사물인식확률
    findNameAndRect = [] # 찾은 사물 정보 : [ ['사물명', 신뢰도, [sx, sy, ex, ey]], ... ]
    findImage = None # 사각형 없는 최종 이미지
    while True:
        #time.sleep(0.1)

        ret, frame = cap.read()
        if not ret :
            break

        frameCount += 1
        tempfindNameAndRect = [] # 찾은 사물 정보 : [ ['사물명', 신뢰도, [sx, sy, ex, ey]], ... ]
        if frameCount % 10 == 0 : # 화면출력 속도 조절

            saveImage = frame[:]  # 사각형이 없는 평활화 이전 이미지 (원 크기영상)
            frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
            beforeImage = frame[:] # 평활화 이전의 이미지를 화면에 보여주기 위함 (1/2크기 영상)

            ## 히스토그램 평활화를 통해서 처리
            hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsvimg)
            equalizedV = cv2.equalizeHist(v)
            # h,s,equalizedV를 합쳐서 새로운 hsv 이미지를 만듭니다.
            hsv2 = cv2.merge([h, s, equalizedV])
            # 마지막으로 hsv2를 다시 BGR 형태로 변경합니다.
            frame = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
            #########################################
            image = frame # image는 평활화로 사용함
            args = {'image': filename, 'prototxt': 'MobileNetSSD_deploy.prototxt.txt',
                    'model': 'MobileNetSSD_deploy.caffemodel', 'confidence': 0.5}

            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                       "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                       "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                       "sofa", "train", "tvmonitor"]

            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

            net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

            net.setInput(blob)
            detections = net.forward()

            count, countConfidence = 0, 0
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > args["confidence"]:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    if CLASSES[idx] == targetClass.strip() :
                        count += 1
                        countConfidence += confidence
                        tempfindNameAndRect.append([CLASSES[idx], confidence, [startX, startY, endX, endY]])

                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(beforeImage, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(beforeImage, label, (startX, y), cv2.FONT_ITALIC, 0.5, COLORS[idx], 2)

            frame = beforeImage #화면에는 평활화 이전것을 보여줌
            cv2.imshow('DeepLearning', frame)

            # 센 개수가 최대면 화면 캡처
            if count > maxCount :
                maxCount = count; maxConfidence = countConfidence
                captureVideo()
                findNameAndRect = tempfindNameAndRect
                findImage = saveImage
                status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                window.update()
            elif count == maxCount :
                if countConfidence > maxConfidence :
                    maxCount = count; maxConfidence = countConfidence
                    captureVideo()
                    findNameAndRect = tempfindNameAndRect
                    findImage = saveImage
                    status.configure(text=status.cget("text") + '\t' + targetClass + ':' + str(maxCount) + '\t 평균 신뢰도:' + str( round(maxConfidence/maxCount * 100)) )
                    window.update()

            count = 0; countConfidence = 0

            c = cv2.waitKey(1)
            if c == 27 :
                break

    cap.release()
    cv2.destroyAllWindows()

    ###############################
    ## 최종 결과 화면에서 사물별로 저장한다.
    ###############################
    # findNameAndRect --> [['person', 0.9991334080696106, [366, 59, 459, 323]], ['person', 1.998100459575653, [68, 120, 206, 309]], ...
    findSubImages = [] # 잘라낸 사물 이미지 리스트
    import os.path
    cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    index = 1
    for nameAndRect in findNameAndRect :
        x1, y1, x2, y2 = nameAndRect[2]
        x1 = 0 if x1 < 0 else x1 ; x2 = 0 if x2 < 0 else x2; y1 = 0 if y1 < 0 else y1; y2 = 0 if y2 < 0 else y2;
        sub = findImage[y1*2:y2*2, x1*2:x2*2] # resize를 1/2로 했으므로, 원영상 위치는 2배
        ###############################################
        # sub를 이용해서 얼굴 찾기 (하르케스케이드)
        ####### CV2 메소드로 구현하기 --> photo2로 넘기기 ####
        sub2 = sub[:]  # 복사
        cvGray = cv2.cvtColor(sub2, cv2.COLOR_BGR2GRAY)
        ##얼굴 인식하는 사각형을 추출
        face_rects = cascade.detectMultiScale(cvGray, 1.1, 5)
        if len(face_rects) == 0 :
            faceSub = sub2
        else :
            for (x, y, w, h) in face_rects:
                faceSub = sub2[y:y+h, x:x+w]
        sub = faceSub
        ###############################################
        saveFname = 'face_' + os.path.basename(filename).split('.')[0]+ "_" +"{0:03d}".format(index) + "_" + nameAndRect[0] + "_" + "{0:03d}".format(int(nameAndRect[1]*100)) + ".png"
        cv2.imwrite('c:/temp/' + saveFname, sub)
        index += 1

    print('Save. OK!')
    # 해당 이미지를 저장한다.


#######################
#### 전역변수 선언부 ####
#######################
R, G, B = 0,1,2
inImage,outImage = [],[] # 3차원 리스트(배열)
inW, inH, outW, outH = [0]*4
window, canvas, paper = None, None, None
filename = ""
VIEW_X, VIEW_Y = 512,512 #화면에 보일 크기 (출력용)


####################
#### 메인 코드부 ####
####################
window = Tk()
window.title('컴퓨터 비젼(OpenCV) ver 0.4')
window.geometry("500x500")

status = Label(window, text = '이미지 정보:',bd = 1 , relief = SUNKEN, anchor = W)
status.pack(side = BOTTOM,fill=X)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='파일 열기', command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label='파일 저장', command=saveImageColor)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label='화소점 처리', menu=comVisionMenu1)
comVisionMenu1.add_command(label='덧셈/뺄셈', command=addImageColor)
comVisionMenu1.add_command(label='화소값 반전', command=revImageColor)
comVisionMenu1.add_command(label='파라볼라', command=paraImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label='모핑', command=morphImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label='채도조절(Pillow)', command=addSValuePillow)
comVisionMenu1.add_command(label='채도조절(HSV)', command=addSValueHSV)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label='통계', menu=comVisionMenu2 )
comVisionMenu2.add_command(label='이진화', command=binaryImageColor)
# comVisionMenu2.add_command(label='축소(평균변환)', command=zoomOutImage2)
# comVisionMenu2.add_command(label='확대(양선형보간변환)', command=zoomInImage2)
# comVisionMenu2.add_separator()
comVisionMenu2.add_command(label='히스토그램', command=histoImageColor)
# comVisionMenu2.add_command(label='히스토그램(내꺼)', command=histoImageColor2)
# comVisionMenu2.add_command(label='명암대비', command=stretchImage)
# comVisionMenu2.add_command(label='End-In탐색', command=endinImage)
# comVisionMenu2.add_command(label='히스토그램 평활화', command=histoEqualImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label='기하학 처리', menu=comVisionMenu3)
comVisionMenu3.add_command(label='상하반전', command=upDownImageColor)
comVisionMenu3.add_command(label='오른쪽 90도 회전', command=rotationImageColor)
comVisionMenu3.add_command(label='축소', command=zoomOutImageColor)
comVisionMenu3.add_command(label='확대', command=zoomInImageColor)
comVisionMenu3.add_command(label='이동', command=moveImageColor)
comVisionMenu3.add_command(label='회전1', command=rotateImageColor)
comVisionMenu3.add_command(label='회전2(중심, 역방향)', command=rotateImageColor2)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label='화소영역 처리', menu=comVisionMenu4)
comVisionMenu4.add_command(label='엠보싱(RGB)', command=embossImageRGB)
comVisionMenu4.add_command(label='엠보싱(pillow제공)', command=embossImagePillow)
comVisionMenu4.add_command(label='엠보싱(HSV)', command=embossImageHSV)
comVisionMenu4.add_separator()
comVisionMenu4.add_command(label='블러링(RGB)', command=blurImageRGB)
comVisionMenu4.add_command(label='샤프닝', command=sharpImageRGB)
# comVisionMenu4.add_command(label='경계선 검출', command=boundaryImage)
# comVisionMenu4.add_command(label='가우시안 필터링', command=gaussianImage)
# comVisionMenu4.add_command(label='고주파', command=highFrequencyImage)
# comVisionMenu4.add_command(label='저주파', command=lowFrequencyImage)

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label='데이터베이스 입출력', menu=comVisionMenu5)
comVisionMenu5.add_command(label='MySQL에서 불러오기', command=loadMysqlColor)
comVisionMenu5.add_command(label='MySQL에 저장하기', command=saveMysqlColor)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label='CSV 열기', command=openCSVColor)
comVisionMenu5.add_command(label='CSV 형식으로 저장', command=saveCSVColor)
comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label='엑셀 열기', command=openExcel)
comVisionMenu5.add_command(label='엑셀 형식으로 저장', command=saveExcelColor)
# comVisionMenu5.add_command(label='엑셀 아트로 저장', command=saveExcelArt)

openCVMenu = Menu(mainMenu)
mainMenu.add_cascade(label='OpenCV 딥러닝', menu=openCVMenu)
openCVMenu.add_command(label='엠보싱(OpenCV)', command=embossOpenCV)
openCVMenu.add_command(label='그레이스케일(OpenCV)', command=greyscaleOpenCV)
openCVMenu.add_command(label='블러링(OpenCV)', command= blurOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label='회전', command=rotateOpenCV)
openCVMenu.add_command(label='확대', command= zoomInOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label='수평 웨이브', command = waveHorOpenCV)
openCVMenu.add_command(label='수직 웨이브', command = waveVirOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label='카툰화', command = cartoonOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label='얼굴인식(머신러닝)', command =faceDetectOpenCV)
openCVMenu.add_command(label='한니발 마스크(머신러닝)', command = hanibalOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label='냥이 얼굴(머신러닝)', command =catFaceDetectOpenCV)
openCVMenu.add_command(label='냥이 마스크(머신러닝)', command = catHanibalOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label='선글라스(머신러닝)', command =sunglassOpenCV)
openCVMenu.add_command(label='콧수염(머신러닝)', command =moustacheOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="동영상 인식(딥러닝)-최대 장면추출", command=videoDeepMaxCountCV2)
openCVMenu.add_command(label="동영상 인식(딥러닝)-최대 장면추출(평활화)", command=videoDeepMaxCountEqualCV2)
openCVMenu.add_command(label="동영상 인식(딥러닝)-최대 장면추출(평활화)-사물별 별도 저장", command=videoDeepMaxCountEqualSaveObjectCV2)
openCVMenu.add_command(label="동영상 인식(딥러닝)-최대 장면추출(평활화)-사물별 별도 저장-얼굴만 추출", command=videoDeepMaxCountEqualSaveAndExtractFaceObjectCV2)

window.mainloop()