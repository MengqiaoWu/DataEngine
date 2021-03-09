# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 11:14:13 2021

@author: WuMengqiao
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from efficient_apriori import apriori as ap

# 数据加载
data = pd.read_csv('Market_Basket_Optimisation.csv', header=None)
# 调整显示列数，也可用pd.options.display.max_columns = 50
pd.set_option('max_columns', None)
# 创建用于合并采购物品的列
combi = []
# 按照行数遍历
for i in range(0, data.shape[0]):
    string = ''
    # 按照列数遍历
    for j in range(0, data.shape[1]):
        if str(data.iloc[i, j]) != 'nan':
            string += str(data.iloc[i, j]) + '/'
    combi.append(string)
# 合成用于关联分析的数据表，维度在表头，0，1表示有无
data_combi = pd.DataFrame(combi, columns=["combi"])
data_hot_encoded = data_combi.drop('combi', 1).join(data_combi.combi.str.get_dummies(sep='/'))
# 挖掘频繁项集
Itemsets = apriori(data_hot_encoded, use_colnames=True, min_support=0.04)
Itemsets.sort_values(by=['support'], ascending=False, inplace=True)
print('频繁项集：\n', Itemsets)
# 计算关联规则，设置最小提升度0.3
Rules = association_rules(Itemsets, metric='lift', min_threshold=1)
Rules.sort_values(by='lift', ascending=False, inplace=True)
print(Rules.shape)
print('关联规则：\n', Rules)
# 运用efficient_apriori方法,数据源为列表的形式
transcation = []
# 按照行数遍历
for i in range(0, data.shape[0]):
    temp = []
    # 按照列数遍历
    for j in range(0, data.shape[1]):
        if str(data.iloc[i, j]) != 'nan':
            temp.append(str(data.iloc[i, j]))
    transcation.append(temp)
itemsets, rules = ap(transcation, min_support=0.04, min_confidence=0.2)
print('-'*100)
print('频繁项集：\n', itemsets)
print('关联规则：\n', rules)
