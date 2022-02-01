"""
Readme :
This is a code to crawl data from indonesia's ecommerce. 
Shopee marketplace is chosen to be crawled. 
The task is to get the name, category, and price for each product.
In this code, additional column such as number of sold
was added to the data. This columns was added because 
in the long run, this column could help to be the features
to detect suspicious transactions. 

Thank you
"""

#===================================================
# Dependencies
#===================================================

import re
import pandas as pd 
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium .webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#===================================================
# Scraping Class
#===================================================

class ShopeeScraping():
    """
    A class used to scrape product data from shopee

    ...

    Attributes
    ----------
    base_url : str
        a base link to shopee's website
    keyword : str
        the keyword to be searched
    category : str
        the category to be matched
    linklist : list
        a list contains the page url
    numOfPage : int
        the range of page number to be searched
    item_price = list
        a list contains the price for each product
    item_name = list
        a list contains the name of each product 
    starlist = list
        a list contains the rating of each product
    nofsold = list
        a list contains the number of product sold

    Methods
    -------
    startWebDriver()
        Initialize google chrome web driver
    getBaseUrl()
        Navigate to base url attributes
    quitWebDriver()
        Exit webdriver
    findSearchBar()
        Find shopee search bar 
    inputKeyword()
        enter the keyword to be searched
    scrollDown()
        scroll down the entire page to refresh the HTML content
    scrollUp()
        scroll up the entire page to refresh the HTML content
    getHTML()
        get HTML element from the current page
    getProductName()
        get product name from HTML content
    getProductPrice()
        get product price from HTML content
    getNumberOfSold()
        get number of sold from HTML content
    getRating()
        iterate through the product's detail page and get the rating
    clickCategories()
        click the nearest match of the categories to filter out the product
    checkLength()
        check the entire page product's number, if loaded correctly, the number of produccrt is 60
    navigateThorughPage()
        change the url to the next page
    exportDf()
        export the pandas dataframe to json and csv
    scrapePage()
        scrape the shopee's product
    
    """

    def __init__(self, keyword, category, numOfPage):
        """
        Parameters
        ----------
        base_url : str
            a base link to shopee's website
        keyword : str
            the keyword to be searched
        category : str
            the category to be matched
        linklist : list
            a list contains the page url
        numOfPage : int
            the range of page number to be searched
        item_price = list
            a list contains the price for each product
        item_name = list
            a list contains the name of each product 
        starlist = list
            a list contains the rating of each product
        nofsold = list
            a list contains the number of product sold
        """

        self.base_url = 'https://shopee.co.id'
        self.keyword = keyword
        self.category = category
        self.linklist = []
        self.linklist.append(self.base_url)
        self.numOfPage = numOfPage
        self.item_price = []
        self.item_name = []
        self.starlist = []
        self.nofsold = []
       
    def startWebDriver(self):
        """Initialize google chrome web driver"""
        self.chrome_options = Options()
        self.chrome_options.add_argument('start-maximized')
        self.chrome_options.add_argument("--disable-notifications")
        self.browser = webdriver.Chrome(executable_path = r"C:\Program Files (x86)\chromedriver.exe", options = self.chrome_options)
       
    def getBaseUrl(self):
        """Navigate to base url attributes"""
        self.browser.get(self.base_url)
   
    def quitWebDriver(self):
        """Exit webdriver"""
        self.browser.quit()
   
    def findSearchBar(self):
        """Find shopee search bar"""
        try:
            self.inputbox = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "shopee-searchbar-input__input"))
            )
        except:
            self.inputbox = None
            raise Exception("Class is not found!")
            
           
    def inputKeyword(self):
        """enter the keyword to be searched"""
        try :
            self.inputbox.send_keys(self.keyword)
            self.inputbox.send_keys(Keys.ENTER)
        except:
            self.browser.quit()
            raise Exception("Key input failed")
           
    def scrollDown(self):
        """scroll down the entire page to refresh the HTML content"""
        for h in range(0,10000,100):
            if h != 0 :
                self.browser.execute_script("window.scrollTo({0},{1});".format(h-100, h))
                sleep(0.05)  
               
    def scrollUp(self) :
        """scroll up the entire page to refresh the HTML content"""
        g = 10000-100
        for h in range(0,10000,100):
            if g-h != 10000 :
                cc.browser.execute_script("window.scrollTo({0},{1});".format(g-h+100, g-h))
                sleep(0.1)
       
    def getHTML(self):
        """get HTML element from the current page"""
        self.html = self.browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        self.soup = BeautifulSoup(self.html, "html.parser")
           
    def getProductName(self):
        """get product name from HTML content"""
        for item_n in self.soup.find_all('div', class_='_10Wbs- _5SSWfi UjjMrh'):
            self.item_name.append(item_n.text)
           
    def getProductPrice(self):
        """get product price from HTML content"""
        for item_n in self.soup.find_all('div', class_='zp9xm9 xSxKlK _1heB4J'):
            self.item_price.append(item_n.text)
           
    def getNumberOfSold(self):
        """get number of sold from HTML content"""
        for item_n in self.soup.find_all('div', class_='_2VIlt8'):
            self.nofsold.append(item_n.text)
           
    def getRating(self):
        """iterate through the product's detail page and get the rating"""
        for k in range(60):
            self.prodlist = self.browser.find_elements_by_class_name("_3QUP7l")
            if len(self.prodlist) != 60 :
                for i in range(100):
                    self.scrollDown()
                    self.prodlist = self.browser.find_elements_by_class_name("_3QUP7l")
                    if len(self.prodlist) == 60 :
                        break
            if len(self.prodlist) == 60 :
                self.prodlist = self.browser.find_elements_by_class_name("_3QUP7l")
                self.prodlist[k].click()
                sleep(0.5)
                self.html_detail = self.browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                self.soup_detail = BeautifulSoup(self.html_detail, "html.parser")
                for item_n in self.soup_detail.find_all('div', class_='OitLRu _1mYa1t'):
                    try :
                        self.starlist.append(item_n.text)
                    except:
                        self.starlist.append(None)
                self.browser.get(self.linklist[-1])

    def clickCategories(self):
        """click the nearest match of the categories to filter out the"""
        self.togg = None
        counter = 0
        while self.togg != "Done" :
            try:
                self.browser.find_elements_by_class_name("shopee-filter-group__toggle-btn")[1].click()
                self.togg = "Done"
            except :
                self.togg = "undone"
                pass
            counter = counter + 1
            if counter > 100 :
                raise Exception("filter button is not found")
            self.scrollDown()
        self.clicklist = self.browser.find_elements_by_class_name("shopee-checkbox__label")
        self.ctext = []
        self.cobj = []
        for c in self.clicklist:
            if self.category in c.text:
                self.ctext.append(c.text)
                self.cobj.append(c)
       
        for x in range(len(self.ctext)) :
            if len(self.ctext[x]) == min(map(len, self.ctext)) :
                self.category = self.ctext[x]
                self.cobj[x].click()

    def checkLength(self):
        """check the entire page product's number, if loaded correctly"""
        self.productLength = []
        for item_n in self.soup.find_all('div', class_='_10Wbs- _5SSWfi UjjMrh'):
            self.productLength.append(item_n.text)

    def navigateThorughPage(self):
        """change the url to the next page"""
        for page in range(self.numOfPage):
            self.linklist.append(cc.browser.current_url)
            self.scrollUp()
            self.getHTML()
            self.checkLength()
            while len(self.productLength) != 60 :
                self.scrollDown()
                self.getHTML()
                self.checkLength()
                print("length of product", len(self.productLength))
            self.getProductName()
            self.getProductPrice()
            self.getNumberOfSold()
            # self.getRating()
            nextpage = re.sub("page={}".format(page),  'page={}'.format(page+1), self.browser.current_url)
            self.browser.get(nextpage)
            sleep(1)
        self.quitWebDriver()

    def exportDf(self):
        """export the pandas dataframe to json and csv"""
        try :
            self.df = pd.DataFrame(self.item_name,columns =['Item Name'])
        except :
            pass

        try :
            self.df['price'] = self.item_price
        except :
            self.df['price'] = None
        
        try :
            self.df['number of sold'] = self.nofsold
        except :
            self.df['number of sold'] = None
        
        try :
            self.df['Categories'] = self.category
        except :
            self.df['Categories'] = None
        
        # try :
        #     self.df['Rating'] = self.starlist
        # except :
        #     self.df['Rating'] = None

        self.df.to_csv("scraping.csv")
        self.df.to_json("scraping.json")

    def scrapePage(self):
        """scrape the shopee's product"""
        self.startWebDriver()
        self.getBaseUrl()
        self.findSearchBar()
        self.inputKeyword()
        self.browser.refresh()
        self.clickCategories()
        self.navigateThorughPage()
        self.exportDf()
        self.quitWebDriver()

#===================================================
# Main Program
#===================================================

keyword = "samsung"
category = "Handphone"
numofpage = 2
cc = ShopeeScraping(keyword, category, numofpage)
cc.scrapePage()
print("Done")

