import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import matplotlib
import streamlit as st
matplotlib.rc('font',family='YouYuan')
import seaborn as sns
import os
st.set_option('deprecation.showPyplotGlobalUse', False)

script_dir = os.path.dirname(os.path.abspath(__file__))

# 回到上一级目录
parent_dir = os.path.dirname(script_dir)
print(parent_dir)
# 导入数据
relative_path = '2019-12.csv'
data_dir = os.path.join(parent_dir, relative_path)

data = pd.read_csv(data_dir, encoding='gbk')

# 数据处理和处理后的代码
data['text'] = (data['title'] + data['abstract']).replace('\n', ' ').str.lower()

#显示数据前五行
print(data.head())

data = pd.DataFrame(data)
data = data.drop(['abstract', 'title'], axis=1)


# 多个类别，包含子分类
data['categories'] = data['categories'].apply(lambda x: x.split(' '))

# 单个类别，不包含子分类
data['categories_big'] = data['categories'].apply(lambda x: [xx.split('.')[0] for xx in x])


# 多标签数据处理，将类别列表转换为二进制矩阵
mlb = MultiLabelBinarizer()
data_label = mlb.fit_transform(data['categories_big'])

# 使用 TF-IDF 对文本数据进行特征提取
vectorizer = TfidfVectorizer(max_features=4000)
data_tfidf = vectorizer.fit_transform(data['text'])


x_train, x_test, y_train, y_test = train_test_split(data_tfidf, data_label,
                                                    test_size=0.3, random_state=1)

# 将训练集的标签转换为 DataFrame
train_labels = pd.DataFrame(y_train, columns=mlb.classes_)

# 计算标签之间的相关性
correlation_matrix_train = train_labels.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix_train, cmap="YlGnBu", annot=True, fmt=".2f", linewidths=.5)
plt.title("Correlation Heatmap - Training Set")
# plt.show()
st.pyplot()

# 构建多标签分类模型
model = MultiOutputClassifier(MultinomialNB()).fit(x_train, y_train)


# 预测测试集的分类结果
y_pred = model.predict(x_test)


# 创建一个包含分类的DataFrame
categories_df = pd.DataFrame(data=mlb.classes_, columns=["分类"])

# 得到分类的预测结果
predicted_categories = mlb.inverse_transform(y_pred)
actual_categories = mlb.inverse_transform(y_test)
# 创建一个包含预测结果的DataFrame
results_df = pd.DataFrame({'实际': actual_categories, '预测': predicted_categories})

# 统计每个分类的数量
category_counts_actual = results_df['实际'].apply(pd.Series).stack().value_counts()
category_counts_predicted = results_df['预测'].apply(pd.Series).stack().value_counts()

# 查找系统中的中文字体路径
font_path = fm.findfont(fm.FontProperties(family='SimHei'))
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=category_counts_actual.index, y=category_counts_actual.values, color='blue', ci=None)

plt.xlabel('分类', fontproperties=fm.FontProperties(fname=font_path))
plt.ylabel('文章数量', fontproperties=fm.FontProperties(fname=font_path))
plt.title('实际分类文章数量', fontproperties=fm.FontProperties(fname=font_path))
# 在每个柱形上显示数量标签
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10, color='black')

plt.xticks(rotation=45, ha='right')
# plt.show()
st.pyplot()

# 绘制预测分类文章数量的柱状图
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=category_counts_predicted.index, y=category_counts_predicted.values, color='green', ci=None)

plt.xlabel('分类',fontproperties=fm.FontProperties(fname=font_path))
plt.ylabel('文章数量',fontproperties=fm.FontProperties(fname=font_path))
plt.title('预测分类文章数量',fontproperties=fm.FontProperties(fname=font_path))
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10, color='black')

plt.xticks(rotation=45, ha='right')
# plt.show()
st.pyplot()

# 输出分类预测结果报告
print(classification_report(y_test, y_pred, target_names=mlb.classes_))

print("测试集准确率：", accuracy_score(y_test, model.predict(x_test)))