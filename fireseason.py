import pandas as pd


df = pd.read_excel('C:/Users/ch/Documents/Tencent Files/646134029/FileRecv/赣防火期.xlsx')
df.columns = [x for x in range(len(df.columns))]
temp_list = [x for x in range(1, 367)]
data_dic = {}
for i in df.columns:
    data_dic[i] = []
for date in range(1, len(df.columns)+1, 2):
    date_list = list(df.loc[:, date])
    for each_day in temp_list:
        if each_day in date_list:
            # 原始数据中存在火点数量
            index1 = df[df.loc[:, date] == each_day].index[0]
            data_dic[date].append(df.loc[index1, date])
            # 追加日期
            data_dic[date - 1].append(df.loc[index1, date - 1])
            # 追加火点数量
            continue
        data_dic[date].append(each_day)
        data_dic[date - 1].append(0)
df_final = pd.DataFrame(data=data_dic)
df_final.loc[366] = [0 for i in range(len(df_final.columns))]
'''
数据框构建完成
'''
stock = [1000, 0, 0]
for temp in range(0, len(df.columns)-1, 2):
    cut_off = df_final.loc[:, temp].sum() * 0.9
    list_fire = list(df_final.loc[:, temp])
    list_date = list(df_final.loc[:, temp+1])
    dictionary = dict(zip(list_date, list_fire))
    for eachhead in range(1, 366):
        sum1 = 0
        days = 0
        start = eachhead
        for sum2 in dictionary:
            if sum1 < cut_off:
                sum1 += dictionary[sum2]
                days += 1
                continue
            end = sum2
            stock_temp = [days, start, end]
            if stock_temp[0] < stock[0]:
                stock = stock_temp
            break
        # 更新字典
        start_value = dictionary[start]
        del dictionary[start]
        dictionary[start] = start_value
    else:
        df_final.loc[366, temp + 1] = str(stock[0]+1) + '-' + str(stock[1]) + '-' + str(stock[2])
        stock = [1000, 0, 0]
df_final.to_excel('C:/Users/ch/Documents/Tencent Files/646134029/FileRecv/jx123456.xlsx')
