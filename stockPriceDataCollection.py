from selenium import webdriver
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

browser = webdriver.Chrome()

def get_ETFTable():
    columnNames=[]

    ETFComparisonsTable=[]

    for num in range(0,48):
        browser.get("https://kabuoji3.com/stock/")
        stockSearch=browser.find_element_by_class_name("form_inputs")
        stockSearchForm=stockSearch.find_element_by_class_name("form_txt")
        stockSearchForm.send_keys("ETF")
        btnClick=browser.find_element_by_class_name("btn_submit")
        btnClick.click()

        stockClick=browser.find_elements_by_class_name("clickable")
        stockClick[num].find_element_by_tag_name("a").click()

        stockTable=browser.find_element_by_class_name("table_wrap")
        stockLine=stockTable.find_elements_by_tag_name("tr")

        if len(stockLine)==302:
            ETFComparisons=[]
            for i in range(2,152):
                stockETFPriceAfter=stockLine[i-1].find_elements_by_tag_name("td")
                stockETFPriceBefore=stockLine[i].find_elements_by_tag_name("td")
                ETFComparison=float(stockETFPriceAfter[6].text)-float(stockETFPriceBefore[6].text)
                ETFComparisons.append(ETFComparison)

            stockETFPriceAfter=stockLine[151].find_elements_by_tag_name("td")
            stockETFPriceBefore=stockLine[153].find_elements_by_tag_name("td")
            ETFComparison=float(stockETFPriceAfter[6].text)-float(stockETFPriceBefore[6].text)
            ETFComparisons.append(ETFComparison)

            for i in range(154,302):
                stockETFPriceAfter=stockLine[i-1].find_elements_by_tag_name("td")
                stockETFPriceBefore=stockLine[i].find_elements_by_tag_name("td")
                ETFComparison=float(stockETFPriceAfter[6].text)-float(stockETFPriceBefore[6].text)
                ETFComparisons.append(ETFComparison)

            ETFComparisonsTable.append( ETFComparisons )

            stockTitleBox=browser.find_element_by_class_name("base_box_ttl")
            stockTitle=stockTitleBox.find_element_by_class_name("jp").text
            columnNames.append( stockTitle )

    ETFTable=pd.DataFrame(ETFComparisonsTable)
    ETFTable=ETFTable.T
    ETFTable.columns=columnNames

    ETFTable.head()
    ETFTable.to_csv('./ETFTable.csv',encoding='utf-8')

def get_Dates():
    browser.get("https://babuoji3.com/stock/{}/").format(4307)
    stockTable=browser.find_element_by_class_name("table_wrap")
    stockLine=stockTable.find_elements_by_tag_name("tr")
    dates=[]
    for i in range(1,152):
        stockDate=stockLine[i].find_elements_by_tag_name("td")
        stockDate=stockDate[0].text
        dates.append(stockDate)
    for i in range(153,302):
        stockDate=stockLine[i].find_elements_by_tag_name("td")
        stockDate=stockDate[0].text
        dates.append(stockDate)
    df_date=pd.DateFrame()
    df_date["date"]=dates
    df_date["year"]=df_date["date"].apply(lambda x:int(x.split("-")[0]))
    df_date["month"]=df_date["date"].apply(lambda x:int(x.split("-")[1]))
    df_date["day"]=df_date["date"].apply(lambda x:int(x.split("-")[2]))
    df_date.head()
    df_date.to_csv('./df_date.csv',encoding='utf-8')

if __name__=='__main__':
    get_ETFTable()
    get_Dates()
