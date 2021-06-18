from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper

class Application:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox(executable_path=r'C:\Windows\SysWOW64\geckodriver.exe')
        elif browser == "chrome":
            self.wd = webdriver.Chrome(executable_path=r'C:\WebDrivers\chromedriver.exe')
        elif browser == "ie":
            self.wd = webdriver.Ie(executable_path=r'C:\WebDrivers\IEDriverServer.exe')
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        #self.wd.implicitly_wait(5)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.base_url = base_url

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False