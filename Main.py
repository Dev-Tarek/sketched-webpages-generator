from Generator.Generator import *
from Compiler.WebCompiler import *
from HTMLRenderer.Render import *
from Sketcher.Screenshot2Sketch import *
from shutil import copyfile
from os.path import basename
from pathlib import Path

import argparse
import imagesize
import imutils
import hashlib
import zipfile
import cv2


## ON LOCAL MACHINE
GENERATOR_OUTPUT_PATH = './_Output_Pages/DSL/'
SKETCH_OUTPUT_PATH = './_Output_Sketches/'
RENDER_OUTPUT_PATH = './_Output_Pages/Render/'
DATASET_ZIP_PATH = './_Zipped/'
DATASET_ZIPPED_DIR = './_Zipped/Dataset_'

## ON COLAB
# GENERATOR_OUTPUT_PATH = '../drive/My Drive/Sketch-Dataset/DSL/'
# SKETCH_OUTPUT_PATH = '../drive/My Drive/Sketch-Dataset/Sketch/'
# RENDER_OUTPUT_PATH = '../drive/My Drive/Sketch-Dataset/Render/'
# DATASET_ZIP_PATH = '../drive/My Drive/_Zipped/'
# DATASET_ZIPPED_DIR = '../drive/My Drive/Dataset_'


def ZIP_SAVE_PATH(i): return DATASET_ZIPPED_DIR + \
    str((i + 1 % 100) - 1) + '.zip'


def initGeneration(generationPath, sketchPath, renderPath, zipPath, pageHeight, fresh, verbose):
    driver = WebDriver(1200, pageHeight)
    # Checking that directories exist.
    Path(generationPath).mkdir(exist_ok=True)
    Path(sketchPath).mkdir(exist_ok=True)
    Path(renderPath).mkdir(exist_ok=True)
    Path(zipPath).mkdir(exist_ok=True)
    if(fresh):
        cleanDirectories([sketchPath, renderPath, generationPath], verbose)
    fileNames = getGUIFilesName(generationPath)
    fileHashes = loadHashedExistingFiles(fileNames, generationPath)
    startIndex = findStartIndex(fileNames)
    return driver, fileHashes, startIndex


def cleanDirectories(paths, verbose):
    for path in paths:
        cleanDirectory(path, verbose)


def cleanDirectory(path, verbose=True):
    if(verbose):
        print("Cleaning:", path)
    for fileName in os.listdir(path):
        if not fileName == '.gitkeep':
            os.remove(os.path.join(path, fileName))
    if(verbose):
        print("Cleaning completed.")


def getGUIFilesName(outputPath):
    fileNames = []
    for fileName in os.listdir(outputPath):
        if fileName.split('.')[1] == 'gui':
            fileNames.append(fileName)
    return fileNames


def loadHashedExistingFiles(fileNames, outputPath):
    fileHashes = []
    for fileName in fileNames:
        with open(outputPath + fileName, 'rb') as afile:
            hasher = hashlib.md5()
            buf = afile.read()
            hasher.update(buf)
        fileHash = hasher.hexdigest()
        fileHashes.append(fileHash)
    return fileHashes


def findStartIndex(fileNames):
    lastFileIndex = 0
    for fileName in fileNames:
        lastFileIndex = max(lastFileIndex, int(fileName.split('_')[1]))
    return lastFileIndex


def deleteIntermediateOutputs(files):
    for fileName in files:
        os.remove(fileName)


def isFileUnique(fileName, fileHashes, verbose):
    with open(fileName, 'rb') as afile:
        hasher = hashlib.md5()
        buf = afile.read()
        hasher.update(buf)
    fileHash = hasher.hexdigest()

    if(not fileHash in fileHashes):
        fileHashes.append(fileHash)
        return True

    if(verbose):
        print('! retrying:', fileName, '- repeated..')
    return False


def generateDSL(path):
    with open(path, 'w+') as afile:
        tree = DSLNode('root', None)
        generate(tree, 0)
        tree.render(afile, -1)
        tokensCount[0] = 0


def isValidHeight(path, fileName, pageHeight, verbose):
    _, height = imagesize.get(path)
    if height > pageHeight:
        if(verbose):
            print('! retrying:', fileName, '- over height..')
        return False

    return True


def generateDataset(KEEP_INTERMEDIATE_OUTPUTS, GENERATOR_OUTPUT_SIZE, VARIATIONS_NUM, PAGE_HEIGHT, fresh, verbose, zipping, zipsize):

    global GENERATOR_OUTPUT_PATH
    global RENDER_OUTPUT_PATH

    driver, fileHashes, offsetIndex = initGeneration(GENERATOR_OUTPUT_PATH,
                                                     SKETCH_OUTPUT_PATH,
                                                     RENDER_OUTPUT_PATH,
                                                     DATASET_ZIP_PATH,
                                                     PAGE_HEIGHT,
                                                     fresh,
                                                     verbose)
    i = offsetIndex

    while i < offsetIndex + GENERATOR_OUTPUT_SIZE:
        pageIndex = str(i).zfill(5)
        fileName = 'page_' + pageIndex

        generateDSL(GENERATOR_OUTPUT_PATH + fileName + '_0.dsl')

        if not isFileUnique(GENERATOR_OUTPUT_PATH + fileName + '_0.dsl', fileHashes, verbose):
            continue

        compileDSL(GENERATOR_OUTPUT_PATH + fileName + '_0.dsl')
        driver.saveScreenshot(GENERATOR_OUTPUT_PATH,
                              fileName + '_0',
                              RENDER_OUTPUT_PATH)

        if not isValidHeight(RENDER_OUTPUT_PATH + fileName + '_0.png', fileName, PAGE_HEIGHT, verbose):
            continue

        for j in range(VARIATIONS_NUM):
            screenshot2Sketch(RENDER_OUTPUT_PATH + fileName + '_0.png',
                              SKETCH_OUTPUT_PATH,
                              fileName + '_' + str(j))

        if not KEEP_INTERMEDIATE_OUTPUTS:
            deleteIntermediateOutputs(
                [GENERATOR_OUTPUT_PATH + fileName + '_0.html', RENDER_OUTPUT_PATH + fileName + '_0.png'])

        i += 1
        
        if zipping and i % zipsize == False and i != 0:
            zipname = ZIP_SAVE_PATH(i)
            dataset = zipfile.ZipFile(zipname, 'w')
            start = ((i + 1 % 100) - 1) - zipsize
            end = (i + 1 % 100) - 1
            for j in range(start, end):
                pageIndex = str(j).zfill(5)
                fileName = 'page_' + pageIndex
                for k in range(VARIATIONS_NUM):
                    dataset.write(SKETCH_OUTPUT_PATH + fileName + '_' + str(k) + '.jpg', basename(
                        SKETCH_OUTPUT_PATH + fileName + '_' + str(k) + '.jpg'), compress_type=zipfile.ZIP_DEFLATED)
                dataset.write(GENERATOR_OUTPUT_PATH + fileName + '_0' + '.dsl', basename(
                    GENERATOR_OUTPUT_PATH + fileName + '_0' + '.dsl'), compress_type=zipfile.ZIP_DEFLATED)
            dataset.close()
            print("[BATCH " + str(int(i / zipsize)) + " SAVED: " + zipname + ']')
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", '-n',
                        help="Number of samples to be generated. Starts with n=0 if the output directory is empty.",
                        type=int,
                        required=True)
    parser.add_argument("--fresh", '-f',
                        help="Fresh start; removes any existing outputs.",
                        action="store_true")
    parser.add_argument("--variations", '-v',
                        help="Number of different sketches for each generated webpage.",
                        type=int,
                        default=1)
    parser.add_argument("--intermediate", '-i',
                        help="Save intermediate outputs from rendering during generation process.",
                        action="store_true")
    parser.add_argument("--height",
                        help="Specifiy page height in pixels. Note: page width is 1200px",
                        type=int,
                        default=1800)
    parser.add_argument("--zipping", '-z',
                        help="Store batches of output files as zipped files. Default batch size is 500.",
                        action="store_true")
    parser.add_argument("--batchsize", '-s',
                        help="Number of pages to be zipped together.",
                        type=int,
                        default=500)
    parser.add_argument("--verbose",
                        help="Printing in console during execution.",
                        action="store_true")

    args = parser.parse_args()
    generateDataset(KEEP_INTERMEDIATE_OUTPUTS=args.intermediate,
                    GENERATOR_OUTPUT_SIZE=args.number,
                    VARIATIONS_NUM=args.variations,
                    PAGE_HEIGHT=args.height,
                    fresh=args.fresh,
                    verbose=args.verbose,
                    zipping=args.zipping,
                    zipsize=args.batchsize
                    )
