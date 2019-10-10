import requests
from bs4 import BeautifulSoup
import datetime
import csv

def get_all_stock_list(k_list):
    url = 'https://kabuoji3.com/stock/'
    rows = []
    rows_k = []
    header = []
    for i in range(1,34):
        params = {'page': i }
        res = requests.get( url,params=params )
        print("%sページ" % i)
        soup = BeautifulSoup( res.text , "lxml")
        table = soup.find("table",class_='stock_table')
        tr_all = table.find_all("tr")

        #見出
        th_all = tr_all[0].find_all("th")
        if i == 1:
            header.append( th_all[0].text )
            header.append( th_all[1].text )

        #内容
        stock_num = 0
        stock_k_num = 0
        for j in range(1,len( tr_all )):
        #for j in range(1,5):
            td_all = tr_all[ j ].find_all("td")
            #print( td_all )
            if td_all[1].text == '東証ETF':
            #if 'ETF' in td_all[0].text:
                # ETFの株価
                stock_num = stock_num + 1
                row = []
                row.append( td_all[0].text )
                row.append( td_all[1].text )

                url_sub = td_all[0].find("a").get("href")
                res_sub = requests.get( url_sub )
                print( "ETF:%s,%s回目"%(td_all[0].text,stock_num) )
                soup_sub = BeautifulSoup( res_sub.text , "lxml" )
                table_sub_all = soup_sub.find_all("table")
                for table in table_sub_all:
                    tr_sub_all = table.find_all("tr")
                    for k in range(1,len(tr_sub_all)):
                        #print( tr_sub_all[ k ] )
                        td_sub_all = tr_sub_all[ k ].find_all("td")
                        if i == 1 and stock_num == 1:
                            header.append( td_sub_all[0].text )
                        row.append( int( td_sub_all[4].text ) )
                #print( row )
                rows.append( row )
            else:
                for item in k_list:
                    if item in td_all[0].text:
                        #調べたい株のコード
                        stock_k_num = stock_k_num + 1
                        print("個別:%s,%s回目" % (td_all[0].text, stock_k_num))
                        rows_k.append( get_kobetsu_stock( item ) )

    newrows = []
    #東証ETF前日比を計算
    for row in rows:
        #print( row )
        newrow = []
        newrow.append( row[0])
        newrow.append( row[1])
        for i in range(3,len(row)):
            newrow.append( row[i-1] - row[i] )
        newrows.append( newrow )
    #東証ETF翌日比を計算
    newrows3 = []
    for row in rows:
        newrow3 = []
        newrow3.append( row[0])
        newrow3.append( row[1] )
        newrow3.append( 0 )
        for i in range( 3 , len(row)-1):
            newrow3.append( row[i-1] - row[i] )
        newrows3.append( newrow3 )
    #個別株の前日比を計算
    newrows_k = []
    for row in rows_k:
        newrow_k = []
        newrow_k.append( row[0])
        newrow_k.append( row[1] )
        for i in range( 3,len( row )):
            newrow_k.append( row[i-1] - row[i] )
        newrows_k.append( newrow_k )
    #個別株の翌日費を計算
    newrows3_k = []
    for row in rows_k:
        newrow3_k = []
        newrow3_k.append( row[0])
        newrow3_k.append( row[1] )
        newrow3_k.append( 0 )
        for i in range( 3,len(row)-1):
            newrow3_k.append( row[i-1] - row[i] )
        newrows3_k.append( newrow3_k )

    rows.insert( 0, header )
    newrows.insert( 0 , header )
    newrows3.insert( 0 , header )
    rows_k.insert( 0 , header )
    newrows_k.insert( 0 , header )
    newrows3_k.insert( 0 , header )

    csv_write('file/東証ETF.csv',rows )
    csv_write('file/東証ETF前日比.csv',newrows)
    csv_write('file/東証ETF翌日比.csv',newrows3)
    csv_write('file/個別.csv',rows_k)
    csv_write('file/個別前日比.csv',newrows_k )
    csv_write('file/個別翌日比.csv',newrows3_k)

#コードからリストを取得する
def get_kobetsu_stock( code ):
    # 調べたい株のコード
    stock_k_num = 1
    row_k = []
    url_k_sub = "https://kabuoji3.com/stock/%s/"%code
    res_k_sub = requests.get(url_k_sub)
    soup_k_sub = BeautifulSoup(res_k_sub.text, "lxml")
    k_name = soup_k_sub.find("span",class_="jp").text
    k_mark = soup_k_sub.find("p",class_="dread").text
    row_k.append( k_name )
    row_k.append( k_mark[0:k_mark.find('\n')] )
    table_k_sub_all = soup_k_sub.find_all("table")
    for table in table_k_sub_all:
        tr_k_sub_all = table.find_all("tr")
        for l in range(1, len(tr_k_sub_all)):
            td_k_sub_all = tr_k_sub_all[l].find_all("td")
            row_k.append(int(td_k_sub_all[4].text))
    return row_k

def csv_write(filename,list):
    with open( filename , 'w',encoding='UTF-8',newline='') as f:
        writer = csv.writer( f )
        writer.writerows( list )

def get_file_name(delta):
    now = datetime.date.today()
    filename = "file/%s%s%s_%s.csv"%(now.year,"0%s"%now.month if now.month < 10 else now.month,"0%s"%now.day if now.day < 10 else now.day,"0%s"%delta if delta < 10 else delta)
    return filename

if __name__=='__main__':
    get_all_stock_list([])
    #get_kobetsu_stock( "1429" )
    #print( get_file_name(1) )




