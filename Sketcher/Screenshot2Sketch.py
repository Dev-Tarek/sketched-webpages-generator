import random
if __package__ is None or __package__ == '':
    from Functions import *
    from COMPONENT_LEVELS import COMPONENT_LEVELS
    
else:
    from .Functions import *
    from .COMPONENT_LEVELS import COMPONENT_LEVELS

def screenshot2Sketch(imagePath, outputPath, fileName):
    
    objects, lvl = [], 0
    image = openImageRGB(imagePath)

    for level in COMPONENT_LEVELS:
        objects.append([])
        elements = level.keys()
        for element in elements:
            color = level[element]
            binaryImage = binaryMaskedImage(image, color)
            contours = getContours(binaryImage)
            for contour in contours:
                x, y, w, h = getBoundingRectPoints(contour)
                objects[lvl].append({element: [x, y, x+w, y+h]})
        lvl += 1
    
    sketchImage = getBlankImage(image.shape)

    lvl = 1
    bold = False
    for level in objects:
        for element in level:
            key = list(element.keys())[0]
            x, y, w, h = element[key]
            insertSketch(sketchImage, key, (x, y, w, h), bold)
        lvl += 1
        
    cv2.imwrite(outputPath + fileName + '.jpg', sketchImage)
    print('done:', fileName)