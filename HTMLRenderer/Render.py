import os
from selenium import webdriver

class WebDriver:
    def __init__(self, w=1200, h=1200):
        # self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(w, h)
        
    def saveScreenshot(self, filePath, fileName, savePath):
        self.driver.get(("file:///" + os.path.abspath(filePath + fileName + '.html')).replace("\\","/"))
        self.driver.save_screenshot(savePath + fileName + '.png')
        
    def setWindowSize(self, width, height):
        self.driver.set_window_size(width, height)