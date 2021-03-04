# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 15:11:45 2021

@author: WuMengqiao
"""

# 导入数据处理通用模块
import pandas as pd
import matplotlib.pyplot as plt
# 导入聚类方法前处理模块
from sklearn import preprocessing
# 导入两种聚类算法
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
# 导入分层聚类图像输出模块
from scipy.cluster.hierarchy import dendrogram, ward

# 读取聚类的源数据
data = pd.read_csv('car_data.csv', encoding='gbk')
# 摘取出需要处理的数据部分
train_x = data[['人均GDP', '城镇人口比重', '交通工具消费价格指数', '百户拥有汽车量']]
# 对源数据进行归一化处理
min_max_scaler = preprocessing.MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_x)
'''
若需要将特征转化为数值表达，可使用LabelEncoder类
le = preprocessing.LabelEncoder()
train_x['aa'] = le.fit_transform(train_x['aa'])
'''


def findnclusters(i=11) -> int:
    """ 运用KMeans手肘法，找到合理的聚类数目 """
    sse = []
    x = range(1, i)
    for k in x:
        # kmeans算法
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_x)
        # 计算inertia簇内误差平方和
        sse.append(kmeans.inertia_)
    # 图像输出
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(x, sse, 'o-')
    plt.show()    
    # 通过归一化X轴Y轴的数值，寻找与XY轴围成形状最接近正方形的点，即X坐标与Y坐标差值最小的点
    x_normal = [(j-min(x))/(max(x)-min(x)) for j in x]
    sse_normal = [(j-min(sse))/(max(sse)-min(sse)) for j in sse]
    diff = [abs(sse_normal[j]-x_normal[j]) for j in range(i-1)]
    return diff.index(min(diff)) + 1
    # 通过多次尝试，发现最优分组的数目会随着分组上限的增加而变多，比如i<=6时，2组；7<i<12时,3组


# 根据最优分组数目，进行KMeans聚类
nclusters = findnclusters(11)
kmeans = KMeans(n_clusters=nclusters)
predict_y = kmeans.fit_predict(train_x)
# 结果输出到文件
result_KMeans = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
result_KMeans.rename({0: u'聚类结果'}, axis=1, inplace=True)
result_KMeans.to_csv('result_KMeans.csv', index=False)

# 分层聚类
model = AgglomerativeClustering(linkage='ward', n_clusters=nclusters)
predict_y = model.fit_predict(train_x)
result_hierarchy = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
result_hierarchy.rename({0: u'聚类结果'}, axis=1, inplace=True)
result_hierarchy.to_csv('result_hierarchy.csv', index=False)
# 分层聚类层次图像
linkage_matrix = ward(train_x)
dendrogram(linkage_matrix)
plt.show()
