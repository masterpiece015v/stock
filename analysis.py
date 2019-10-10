import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics

if __name__ == '__main__':
    train1=pd.read_csv("file/東証ETF前日比.csv",sep=',',index_col='コード・名称')
    train2=pd.read_csv("file/東証ETF翌日比.csv",sep=',',index_col='コード・名称')
    #市場列を削除
    train1.drop(['市場'],axis=1,inplace=True)
    train2.drop(['市場'],axis=1,inplace=True)
    #最終日列の切り捨て
    train1 = train1.iloc[:,:train1.shape[1]-1]
    train2 = train2.iloc[:,:train2.shape[1]-1]

    #print( x_train.isnull().sum() )
    #最後の列名
    colname = train1.columns[train1.shape[1]-1]
    #最後の列がNaNの行を削除する
    train1.dropna( subset=[colname],axis=0,inplace=True)
    train2.dropna( subset=[colname],axis=0,inplace=True)
    #print( x_train )
    #print( x_train[x_train.isnull().any(axis=1)].head() )
    x =train1.T[1:train1.T.shape[0]-1]
    y =train2.T[1:train2.T.shape[0]-1]['1329 iシェアーズ・コア 日経225ETF']
    #x=train[1:].T[['1329 iシェアーズ・コア 日経225ETF']]
    #print( x )

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.27)

    model = RandomForestRegressor(n_estimators=1000)
    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)

    testUpDown=[]

    for test in y_test:
        if test > 0:
            testUpDown.append(1)
        else:
            testUpDown.append(-1)
    predUpDown=[]
    for pred in y_pred:
        if pred>0:
            predUpDown.append(1)
        else:
            predUpDown.append(-1)

    print("確率："+str(metrics.accuracy_score(testUpDown,predUpDown)*100)+"%")

    feature_imp = pd.Series(model.feature_importances_,index=[]).sort_values(ascending=False)
    print( feature_imp)