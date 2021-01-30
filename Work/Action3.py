import pandas as pd
table_ori = pd.read_csv('car_complain.csv')
# 导入数据表
table_problem_breakdown = table_ori.drop('problem', axis=1).join(table_ori.problem.str.get_dummies(','))
# 对problem列做关联分析并向左连接原始表格


def f(x):
    x = x.replace('一汽大众', '一汽-大众')
    return x


table_problem_breakdown['brand'] = table_problem_breakdown['brand'].apply(f)
result_1 = table_problem_breakdown.groupby(['brand'])['id'].agg(['count']).sort_values('count', ascending=False)
print(result_1)
result_1.to_csv('品牌投诉总数.csv', index=True)
# 品牌投诉总数
result_2 = table_problem_breakdown.groupby(['car_model'])['id'].agg(['count']).sort_values('count', ascending=False)
print(result_2)
result_2.to_csv('车型投诉总数.csv', index=True)
# 车型投诉总数
result_3 = table_problem_breakdown.groupby(['brand'])['car_model'].nunique()
# 各品牌车型总数
df4 = result_1.merge(result_3, left_index=True, right_index=True, how='left')
# df4 = result_1.join(result_3) 这个方法更方便！
df4['count'].astype(int)
df4['car_model'].astype(int)
df4['平均车型投诉'] = round(df4['count']/df4['car_model'], 2)
df4 = df4.sort_values('平均车型投诉', ascending=False)
# 如果不赋值的话，要加inplace=True参数
df4.to_csv('品牌平均车型投诉.csv', index=True)
print(df4)
# 投诉总数除以车型总数
