import pandas as pd
data = {'姓名': ['张飞', '关羽', '刘备', '典韦', '许诸'], '语文': [68, 95, 98, 90, 80], '数学': [65, 76, 86, 88, 90], '英语': [30, 98, 88, 77, 90]}
df = pd.DataFrame(data)
print(df)
df1 = df.describe()
print(df1)
df['total'] = df['语文']+df['数学']+df['英语']
df['rank'] = df['total'].rank(ascending=False)
df = df.sort_values('total', ascending=False)
print(df)
df.to_csv('成绩排名.csv', index=False)

