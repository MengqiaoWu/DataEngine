import pandas as pd
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt

# 读取文件
data = pd.read_csv('Market_Basket_Optimisation.csv', header=None)
# 将数据转化成列表形式，并按照物品统计累计数量
transactions = []
item_counts = {}
for i in range(data.shape[0]):
    temp = []
    for j in range(data.shape[1]):
        item = str(data.values[i, j])
        if item != 'nan':
            temp.append(item)
            if item not in item_counts.keys():
                item_counts[item] = 1
            else:
                item_counts[item] += 1
    transactions.append(temp)
# 将交易列表转化为长字符串，以便替换词语
transactions_string = ''
for transaction in transactions:
    transactions_string += ' '.join(transaction)


# 定义需要剔除的文字列表
def remove_stop_words(f):
    stop_words = ['fuck', 'damn']
    for stop_word in stop_words:
        f = f.replace(stop_word, '')
    return f


# 运用词云分析
def create_word_cloud(f):
    # 自定义去除非关键词语
    f = remove_stop_words(f)
    # 使用nltk.tokenize类中的word_tokenize的方法，根据不同语言的特点，重新分割词语，输出列表
    cut_text = word_tokenize(f)
    # 使用join方法，以空格作为标识符将列表转化为字符串
    cut_text = ' '.join(cut_text)
    # 定义词云分析的参数
    wc = WordCloud(max_words=100, width=2000, height=1200)
    # 运行词云分析
    wordcloud = wc.generate(cut_text)
    # 输出图片结果
    wordcloud.to_file('wordcloud.jpg')


create_word_cloud(transactions_string)


# 创建条形图表示函数
def bar_chart(data_list: list, max_num=10):
    keys = []
    values = []
    for index in range(max_num):
        keys.append(data_list[index][0])
        values.append(data_list[index][1])
    # 用Seaborn画条形图
    plt.figure(figsize=(50, 30))
    sns.barplot(keys, values)
    plt.show()


# 对商品的交易量进行排序，转化成list对象
item_counts_sorted = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
print(item_counts_sorted[:10])
bar_chart(item_counts_sorted, 10)
