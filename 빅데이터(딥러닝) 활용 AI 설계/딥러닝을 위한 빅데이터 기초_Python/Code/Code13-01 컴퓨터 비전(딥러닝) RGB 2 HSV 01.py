from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from tkinter import messagebox
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

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
def loadImageColor(fname) :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    global photo # pillow 활용시 쓰기 위해
    inImage=[]
    photo = Image.open(fname) # PIL 객체
    inW = photo.width
    inH = photo.height
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
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()
    VIEW_X = outW;
    VIEW_Y = outH;
    step = 1

    window.geometry(str(int(VIEW_X * 1.2)) + 'x' + str(int(VIEW_Y * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_X // 2, VIEW_Y // 2), image=paper, state='normal')

    import numpy
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i);
            k = int(k)
            r, g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

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
    value = askinteger("밝게/어둡게","값 -->",minvalue=-255,maxvalue=255)
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
    photo2 = Image.open(filename2)  # PIL 객체, 이미지 바로 전달
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

# 영상 축소 알고리즘 (평균변환)
def zoomOutImage2Color() :
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
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i // scale][k // scale] += inImage[RGB][i][k]
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] //= (scale * scale)
    ## 출력
    displayImageColor()

# 영상 확대 알고리즘
def zoomInImageColor() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    scale = askinteger("확대","값 -->",minvalue=2,maxvalue=8)
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

# 영상 확대 알고리즘(양선형 보간)
# 깨끗하게 확대되기 때문에 추후에 딥러닝하면 좋은 결과가 나올 수 있음
def zoomInImage2Color() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    scale = askinteger("확대","값 -->",minvalue=2,maxvalue=8)
    ## 중요! 코드, 출력영상 크기 결정##
    outH = inH*scale
    outW = inW*scale
    ###### 메모리 할당 ###########################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH-1, outW-1))
    ###### 진짜 컴퓨터 비전 알고리즘 #####
    rH,rW,iH, iW = [0]*4 # 실수 위치(rH,rW) 및 실수 위치와 가까운 정수 위치(iH, iW)
    x,y = 0,0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for RGB in range(3):
        for i in range(outH-1) :
            for k in range(outW-1) :
                rH = i / scale
                rW = k / scale
                iH = int(rH)
                iW = int(rW)
                x = rW - iW
                y = rH - iH
                if 0 <= iH < inH-1 and 0 <= iW < inW-1 :
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW+1]
                    C3 = inImage[RGB][iH+1][iW+1]
                    C4 = inImage[RGB][iH+1][iW]
                    newValue = C1 * (1-y) * (1-x) + C2 * (1-y) * x + C3*y*x + C4 * y * (1-x)
                    outImage[RGB][i][k] = int(newValue)
    ## 출력
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
    gCountList = [0] * 256
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

    plt.plot(rCountList,color='r')
    plt.plot(gCountList,color='g')
    plt.plot(bCountList,color='b')
    plt.show()

# 히스토그램
import matplotlib.pyplot as plt
def histoImage2Color() :
    global window, canvas, paper, filename, inImage,outImage, inW, inH, outW, outH
    outCountList =[[0]*256 for _ in range(3)]
    normalCountList =[[0]*256 for _ in range(3)]
    maxVal = []
    minVal = []
    #빈도수 계산
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outCountList[RGB][outImage[RGB][i][k]] += 1
        maxVal.append(max(outCountList[RGB]))
        minVal.append(min(outCountList[RGB]))
    High = 256
    print("max: " + str(maxVal[0]))
    print("min :" + str(minVal[0]))
    print(len(outCountList[RGB]))
    # 정규화 = (카운트 값 - 최소값) * High / (최대값 - 최소값)
    for i in range(3) :
        for k in range(len(outCountList[RGB])) :
            normalCountList[i][k] = (outCountList[i][k] - minVal[i]) * High / (maxVal[i]-minVal[i])
    print(normalCountList)

    # 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window) # window의 하위 window 생성
    subWindow.geometry("768x256")
    subCanvas = Canvas(subWindow, width = 768, height = 256)
    subPaper = PhotoImage(width = 768, height = 256)
    subCanvas.create_image((256*3//2,256//2),image = subPaper, state = "normal")

    for RGB in range(3):
        for i in range(len(normalCountList[RGB])) :
            for k in range(int(normalCountList[RGB][i])) :
                if RGB==0:
                    subPaper.put('#d62719', (256*RGB + i, 255-k))
                elif RGB==1:
                    subPaper.put('#4fc34e', (256*RGB + i, 255-k))
                elif RGB==2:
                    subPaper.put('#1948b4', (256*RGB + i, 255-k))

    subCanvas.pack(expand = 1 , anchor = CENTER)
    subWindow.mainloop()


# 파일을 메모리로 로딩하는 함수
def loadCSVColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    row_list= []
    with open(fname, 'r') as rFp:
        for row_list in rFp :
            row, col = list(map(int, row_list.strip().split(',')))[0:2]
            inH = row+1
            inW = col+1

    ## 입력영상 메모리 확보 ##
    inImage=[]
    for _ in range(3):
        inImage.append(malloc(inH, inW))
    # 파일 --> 메모리
    with open(fname, 'r') as rFp:
        for row_list in rFp :
            row, col, r, g, b, = list(map(int,row_list.strip().split(',')))
            inImage[R][row][col] = r
            inImage[G][row][col] = g
            inImage[B][row][col] = b

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


        for i in range(outH):
            for k in range(outW):
               row_list = [i, k, outImage[R][i][k],outImage[G][i][k],outImage[B][i][k]]
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
    ws_r = wb.add_sheet('first_sheet')
    ws_g = wb.add_sheet('second_sheet')
    ws_b = wb.add_sheet('third_sheet')

    for i in range(outH) :
        for k in range(outW) :
            ws_r.write(i, k, outImage[R][i][k])
            ws_g.write(i, k, outImage[G][i][k])
            ws_b.write(i, k, outImage[B][i][k])

    wb.save(xlsName)
    print('excel.save ok~')


import xlrd
def openExcelColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("엑셀 파일","*.xls;*.xlsx"), ("모든파일", "*.*")))
    if filename == '' or filename == None :
        return
    workbook = xlrd.open_workbook(filename)
    wsList = workbook.sheets()
    # print(wsList.cell_value(0,1))
    inW = wsList[0].nrows
    inH = wsList[0].ncols
    ## 입력영상 메모리 확보 ##
    inImage=[]
    for _ in range(3):
        inImage.append(malloc(inH, inW))

    ## 입력영상 메모리 확보 ##
    for i in range(inH):
        for k in range(inW):
            inImage[R][i][k] = int(wsList[0].cell_value(i,k))
            inImage[G][i][k] = int(wsList[1].cell_value(i,k))
            inImage[B][i][k] = int(wsList[2].cell_value(i,k))
    equalImageColor()

import xlsxwriter
def saveExcelArtColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.xls', filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)

    wb = xlsxwriter.Workbook(xlsName)
    ws = wb.add_worksheet(sheetName)

    ws.set_column(0, outW-1, 1.0) # 약 0.34
    for i in range(outH) :
        ws.set_row(i, 9.5) # 약 0.35

    for i in range(outH) :
        for k in range(outW) :
            data_r = outImage[R][i][k]
            data_g = outImage[G][i][k]
            data_b = outImage[B][i][k]
            # data 값으로 셀의 배경색을 조절 #000000 ~ #FFFFFF
            if data_r > 15 and data_g > 15 and data_b > 15 :
                hexStr = '#' + hex(data_r)[2:] +hex(data_g)[2:] + hex(data_b)[2:]
            else :
                hexStr = '#' + '0' + hex(data_r)[2:] +'0' +hex(data_g)[2:] + '0' +hex(data_b)[2:]
            # 셀의 포맷을 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            ws.write(i, k, '', cell_format)

    wb.close()
    print('Excel Art. save OK~')


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
window.title('컴퓨터 비젼 (딥러닝-칼라) ver 0.1')
window.geometry("600x600")

status = Label(window, text = '이미지 정보:',bd = 1 , relief = SUNKEN, anchor = W, fg="black")
status.pack(side = BOTTOM,fill=X)

mainMenu = tkinter.Menu(window)
window.config(menu=mainMenu)

fileMenu = tkinter.Menu(mainMenu)
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
comVisionMenu2.add_command(label='축소(평균변환)', command=zoomOutImage2Color)
comVisionMenu2.add_command(label='확대(양선형보간변환)', command=zoomInImage2Color)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label='히스토그램', command=histoImageColor)
comVisionMenu2.add_command(label='히스토그램(내꺼)', command=histoImage2Color)
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
comVisionMenu5.add_command(label='엑셀 열기', command=openExcelColor)
comVisionMenu5.add_command(label='엑셀 형식으로 저장', command=saveExcelColor)
comVisionMenu5.add_command(label='엑셀 아트로 저장', command=saveExcelArtColor)

window.mainloop()