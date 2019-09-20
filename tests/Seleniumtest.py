import os
import sys
import time
from datetime import datetime
import unittest2
import xmlrunner
from selenium import webdriver

print "hello selenium"


class Seleniumtest(unittest2.TestCase):

    def setUp(self):
        options=webdriver.ChromeOptions()
        options.headless=True
        self.driver=webdriver.Chrome(options=options)
        self.driver.implicitly_wait(7)
        #self.longMessage=True


    def test_edureka_webapp_homepage(self):
        driver=self.driver
        #driver.get("http:mavixk1c.mylabserver.com:3000")
        driver.get("http:localhost:3000")
        self.assertGreater(len(driver.page_source),0,"\n\n Test : home page load failed")
        #self.assertNotIn("404",driver.page_source,"home page not found..test failed")
        self.assertIn("PHP",driver.title,"\n\nhome page load error..test failed")
        driver.save_screenshot("apphome.png")
        navmenu=driver.find_element_by_xpath("//nav[@class='menu']")
        self.assertIsNotNone(navmenu,"\n\n Test : navigation menu load error..test failed")

    def test_edureka_webapp_menu(self):
        driver=self.driver
        driver.get("http:localhost:3000")
        navmenu = driver.find_element_by_xpath("//nav[@class='menu']")
        self.assertIsNotNone(navmenu, "\n\n Test : navigation menu load error..test failed")
        navlinks = navmenu.find_elements_by_tag_name("a")
        totalinks = len(navlinks)

        for index in range(totalinks):
            pngname = str(navlinks[index].text) + ".png"
            linktext=str(navlinks[index].text)
            linkfailmsg="\n\n Test : navigation onclick.." + linktext + " page load failed"
            navlinks[index].click()

            time.sleep(5)
            self.assertNotIn("404",driver.page_source,linkfailmsg)
            self.assertGreater(len(driver.page_source),0,"\n\n Test : webpage content null..page load failed")
            driver.save_screenshot(pngname)
            driver.back()
            time.sleep(5)
            if index == 0:
                driver.forward()
            self.assertNotIn("404",driver.page_source,"\n\n Test: home page navigation failed")
            self.assertGreater(len(driver.page_source),0)
            self.assertIn("PHP",driver.title,"\n\nhome page navigation failed")
            navmenu = driver.find_element_by_xpath("//nav[@class='menu']")
            navlinks = navmenu.find_elements_by_tag_name("a")
            totalinks=len(navlinks)



    def tearDown(self):
        self.driver.quit()



if __name__ == "__main__":
    with open("seleniumresults.xml","wb") as output:
        unittest2.main(testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)

