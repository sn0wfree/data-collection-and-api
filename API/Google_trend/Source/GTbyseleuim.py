from selenium import webdriver


if __name__ == '__main__':

    driver = webdriver.PhantomJS()
    driver.get(
        'https://trends.google.com/trends/explore?date=2004-01-01%202004-06-30&q=FLWS,SRCE,FOXA,FOX,TWOU')
    data = driver.title
    print data
