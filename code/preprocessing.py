import json
import os 
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
##Processing Data

l = []
for fi in os.listdir('./data/'):
    fn = f'./data/{fi}'
    with open (fn,'r',encoding = 'utf8') as f:
        tmp = json.load(f)
        l.extend(tmp)
df = pd.DataFrame(l)

replaced = {'悠遊pay、悠遊卡':['悠遊付','悠遊卡'],
          '悠遊付及PI錢包':['悠遊付','PI錢包'],
           '歐付寶、悠遊付':['歐付寶','悠遊付'],
           '拍錢包':['PI錢包'],
           '(線上刷卡)':['線上刷卡'],
           '(PG)':['PG'],
            '(信用卡)':['信用卡'],
            '(悠遊付、PI)':['悠遊付','PI錢包'],
            }
unknown_count = 0
for i in l[0:]:
    if 'pay_list' not in i:
        i['pay_list']=['None']
        unknown_count +=1
    if i['pay_list'] is None or i['pay_list'] =='':
        i['pay_list'] = ['None']
        unknown_count +=1
    if not isinstance(i['pay_list'],list):
        print(i['pay_list'],'not a list')
    '''
    for item in i['pay_list'] :
        if item in replaced:
            i['pay_list'].extend(replaced[item])
            i['pay_list'].remove(item)
    '''
pay_list = []
unique_pay_list = []
for i in l:
    pay_list.append(i['pay_list'])
    unique_pay_list.extend(i['pay_list'])
print( 'unknown count ', unknown_count)
print('unique pay_list', set(unique_pay_list))

 
renamed = {
    'category':'類別',
    'city':'縣市',
    'zone':'鄉鎮市',
    'market_address':'地址',
    'shop':'店名'}
    

te = TransactionEncoder().fit(pay_list)
pay_list_onehot = te.transform(pay_list)
columns  = te.columns_
for index,i in enumerate(l):
    for col,b in zip(columns,pay_list_onehot[index]):
        if b:
            i[col]='O'

df = pd.DataFrame(l)
#df = df.drop(columns=['id','index','pay_list','user','zone'])
df = df.drop(columns=['id','index','user','zone','行業代號', '行業代號1', '名稱1', '行業代號2', '名稱2', '行業代號3','名稱3','品牌名稱'])
df=  df.rename( columns=renamed)
print(df.columns)
df.to_excel('latest_foodlover.xlsx')

df = pd.DataFrame(l)
df.to_csv('latest_foodlover.csv',sep='|',index=False)