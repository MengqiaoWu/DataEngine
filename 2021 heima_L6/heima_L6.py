import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from itertools import product

# 读取源数据
data = pd.read_csv('jetrail/train.csv')
# 日期列转化成日期格式
data.Datetime = pd.to_datetime(data.Datetime, format="%d-%m-%Y %H:%M")
# 将源数据调整成ARIMA输入格式
data.index = data.Datetime
data.drop(columns=['ID', 'Datetime'], axis=1, inplace=True)
# 按照每天聚合数据
data_day = data.resample('D').sum()
# 检查数据是否有异常值
data_day['Count'].value_counts().sort_index()
# 可视化EDA
result = sm.tsa.seasonal_decompose(data_day.Count, period=7)
result.plot()
plt.show()
# 选取2013.10.1后的数据作为训练数据，与全数据差别不大
data_arima = data_day['2013-10-1':]
# 进行平稳性检验,得出需要一次差分
print(sm.tsa.stattools.adfuller(data_arima))
data_arima_d1 = data_arima.diff(1)
print(sm.tsa.stattools.adfuller(data_arima_d1[1:]))
# ARIMA建模
# 寻找最优ARMA模型参数，即best_aic最小,运用product来遍历
q = range(0, 10)
p = range(0, 10)
order_lists = list(product(q, p))
results = []
# 定义正无穷
best_aic = float("inf")
best_order = []
for order_list in order_lists:
    try:
        model = ARIMA(data_arima, order=(order_list[0], 1, order_list[1])).fit()
    except ValueError:
        print('参数错误:', order_list)
        continue
    aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
        best_order = order_list
    results.append([order_list, model.aic])
# 计算出，最佳（7，1，9）
model = ARIMA(data_arima, order=(7, 1, 9)).fit()
data_arima_predict = model.predict('2014-09-26', '2015-5-31', type='levels')
plt.figure(figsize=(40, 15))
plt.title('ARIMA Predict')
plt.plot(data_arima_predict)
plt.show()
data_arima_predict.to_csv('data_arima_predict.csv')

# 以下代码运用Prophet方法
# import fbprophet import Prophet
# data_prophet = data_day
# data_prophet.reset_index(inplace=True)
# data_prophet.rename(columns={'Count': 'y', 'Datetime': 'ds'}, inplace=True)
# print(data_prophet)
# model_prophet = Prophet()
# model_prophet.fit(data_prophet)
# future = model_prophet.make_future_dataframe(periods=213)
# data_prophet_predicht = model_prophet.predict(future)
# model_prophet.plot(data_prophet_predicht)
# plt.show()
# model_prophet.plot_components(data_prophet_predicht)
# plt.show()





