ROW, COL = 10, 10
image = []
temp = []
for i in range(ROW) :
    temp = []
    for k in range(COL) :
        temp.append(0)
    image.append(temp)
print(image)

# (2) 대입 --> 파일에서 로딩...
import random
for i in range(ROW) :
        for k in range(COL):
            image[i][k] = random.randint(0,255)

# (3) 데이터 처리/변환/분석.... --> 영상 밝게 하기 (100)
for i in range(ROW) :
        for k in range(COL) :
            image[i][k] += 100

# (4) 데이터 출력
for i in range(ROW) :
        for k in range(COL):
            if image[i][k] > 255 :
               image[i][k] = 255
            print("%3d " % (image[i][k]), end='')
        print()