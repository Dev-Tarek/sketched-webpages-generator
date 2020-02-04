import numpy as np
import cv2, random, imutils
from os import listdir
from os.path import isfile, join
import imagesize

ELEMENTS_PATH = './Assets/Sketched-Elements/'

def openImageRGB(path):
    img = cv2.imread(path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def binaryMaskedImage(image, color):
    mask = cv2.inRange(image, color, color)
    masked_img = cv2.bitwise_and(image, image, mask = mask)
    masked_img = cv2.cvtColor(masked_img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)[1]
    
def getContours(binaryImage):
    cnts = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return imutils.grab_contours(cnts)

def getContourCenter(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return cX, cY

def getBoundingRectPoints(contour):
    return np.array(np.array(cv2.boundingRect(contour)), dtype='int')

def getBlankImage(shape):
    blank = np.zeros(shape, dtype=np.uint8)
    blank = cv2.cvtColor(blank, cv2.COLOR_BGR2BGRA)
    blank.fill(255)
    return blank


def getBestFitImage(element, borderPoints, path, bold):
    best = ''
    difference = []
    x, y, w, h = borderPoints
    imageAspect = (w-x) / (h-y)
    for filename in listdir(path):
        if (bold and not filename.startswith('bold')) or (not bold and filename.startswith('bold')):
            continue
        width, height = imagesize.get(join(path, filename))
        aspect = width / height
        difference.append([abs(imageAspect - aspect), filename])
    difference.sort()
    limit = min(len(difference), 6)
    best = random.choice(difference[:limit])[1]
    return join(path, best)


def insertSketch(image, element, borderPoints, bold):
    if element.find('list-group-item_') > -1:
        element = 'list-group-item'
    try:
        elementImagePath = getBestFitImage(element, borderPoints, join(ELEMENTS_PATH, element), bold)
        iw, ih = imagesize.get(elementImagePath)
        x, y, w, h = borderPoints
        interp = cv2.INTER_CUBIC
        if (w-x)*(h-y) < iw*ih:
            interp = cv2.INTER_AREA
        elementImage = cv2.imread(elementImagePath, cv2.IMREAD_UNCHANGED)
        elementImage = cv2.cvtColor(elementImage, cv2.COLOR_BGR2BGRA)
        if element == 'img':
            if (ih > iw and h-y < w-x):
                elementImage = imutils.rotate_bound(elementImage, 90)
            elif (ih < iw and h-y > w-x):
                elementImage = imutils.rotate_bound(elementImage, -90)
        resizedElement = cv2.resize(elementImage , (w-x, h-y), interpolation = interp)
        # image[y:h, x:w] = resizedElement
        for i in range(resizedElement.shape[0]):
            for j in range(resizedElement.shape[1]):
                if resizedElement[i][j][3] > 0:
                    image[y+i][x+j] = resizedElement[i][j]
                
    except:
        return
    
def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, max(angle * 180 / np.pi, 1), 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_CUBIC, borderValue=(255,255,255))
    return result

def translateImage(image, x, y):
    M = np.float32([[1,0,x],[0,1,y]])
    return cv2.warpAffine(image, M, image.shape[1::-1], borderValue=(255,255,255))

def scaleImage(image, scale):
    scale_percent = scale # Percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    return cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
    
def skewImage(image, size):
    w, h = image.shape[1], image.shape[0]
    wr, hr = int(w * size), int(h * size)
    pts1 = np.float32([[0, 0],[w, 0],[0, h],[w, h]])
    pts2 = np.float32([[random.randrange(0, wr), random.randrange(0, hr)],
                       [random.randrange(w - wr, w), random.randrange(0, hr)],
                       [random.randrange(0, wr), random.randrange(h - hr, h)],
                       [random.randrange(w - wr, w), random.randrange(h - hr, h)]
                     ])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(image, M, (w, h), borderValue=(255,255,255))
    
def augment(points, strength, transformation):
    x, y, w, h = points
    s = strength * 0.008
    t = random.randrange(-7, 7) * strength
    if transformation == 2 or transformation == 3:
        dw = int(random.uniform(1-s, 1+s) * w) - w
        dh = int(random.uniform(1-s, 1+s) * h) - h
        w += dw
        h += dh
        x -= int(0.5 * dw)
        y -= int(0.5 * dh)
    if transformation == 1 or transformation == 3:
        x += t
        y += t
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return [x, y, w, h]
    