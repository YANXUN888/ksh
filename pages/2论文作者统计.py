import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import ast
from wordcloud import WordCloud
import os

# 显示中文
# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建相对路径
relative_path = 'FZJZJW.TTF'  # 根据实际的相对路径修改
font_path = os.path.join(script_dir, relative_path)
font = FontProperties(fname=font_path, size=14)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置页面配置
st.set_page_config(page_title="Mapping Demo", page_icon="🌍", layout='wide')
st.markdown("# 论文作者统计")
st.sidebar.header("论文作者数据更新结果统计")
st.markdown("## 我们将从论文作者更新论文数来探讨学术前沿")
script_dir = os.path.dirname(os.path.abspath(__file__))

# 回到上一级目录
parent_dir = os.path.dirname(script_dir)
print(parent_dir)
# 导入数据
relative_path = '2019-12.csv'
data_fir = os.path.join(parent_dir, relative_path)
data = pd.read_csv(data_fir, encoding='ISO-8859-1')
data['authors_parsed'] = data['authors_parsed'].apply(ast.literal_eval)
data['authors_combined'] = data['authors_parsed']. \
    apply(lambda x: [' '.join(inner_list) for inner_list in x])
# 修改作者名字这一列类型
all_authors = sum(data['authors_parsed'], [])
authors_names = [' '.join(x) for x in all_authors]
authors_names = pd.DataFrame(authors_names)

# 获取前10名作者
most_authors = authors_names[0].value_counts().head(10).reset_index()
most_authors.columns = ['Author', 'Count']
print(most_authors)
# 获取作者姓氏排名
authors_lastnames = [x[0] for x in all_authors]
authors_lastnames = pd.DataFrame(authors_lastnames, columns=['Lastname'])
lastname_counts = authors_lastnames['Lastname'].value_counts().reset_index()
lastname_counts.columns = ['Lastname', 'Count']
top_lastnames = lastname_counts.head(10)

# 进行左右布局
tab1, tab2 = st.tabs(["统计姓名", "统计姓氏"])
title = 25
label = 18
ticks = 12

with tab1:
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.set(style="darkgrid")
    sns.barplot(x='Count', y='Author', data=most_authors, color="#ED6765")

    # 添加标题
    ax1.set_title('2019年12月arXiv上更新论文数量前10位作者', fontproperties=font, fontsize=title)
    ax1.set_xlabel('更新论文数量', fontproperties=font, fontsize=label)
    ax1.set_ylabel('作者名字', fontproperties=font, fontsize=label)

    plt.xticks(fontsize=ticks)
    plt.yticks(fontsize=ticks)
    st.pyplot(fig1)
    st.markdown("### 探究第一名Exner Pavel的学术成果")

    # 探究第一名的研究
    # 修正 authors_combined 列
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    import numpy as np
    import time

    data['authors_combined'] = data['authors_parsed'].apply(
        lambda x: [' '.join(map(str, inner_list)) for inner_list in x])

    # 处理 NaN 值，用空字符串替代
    data['authors_combined'].fillna('', inplace=True)

    # 再进行包含 "Exner Pavel" 的行的筛选
    selected_rows = data[data['authors_combined'].apply(lambda x: any("Exner Pavel" in item for item in x))]

    # 定义分词器，同时去除英语停用词
    vectorizer = CountVectorizer(stop_words=list(ENGLISH_STOP_WORDS))

    # 转换文本为词频矩阵
    X = vectorizer.fit_transform(selected_rows['title'])

    # 获取词汇表和词频
    vocab = vectorizer.get_feature_names_out()
    word_freq = X.toarray().sum(axis=0)

    # 将结果转换为DataFrame
    result = pd.DataFrame(list(zip(vocab, word_freq)), columns=['Word', 'Count'])
    st.markdown("### Exner Pavel学术成果关键词")
    # 初始化进度条和其他元素
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    chart = st.bar_chart(result.head(1).set_index('Word'), color="#DAA520")  # 初始显示结果中的第一行数据

    # 模拟数据更新和进度条
    for i in range(1, result.shape[0]):  # 遍历结果的每一行，从第二行开始
        # 更新状态文本
        status_text.text("完成%i%%" % ((i + 1) / result.shape[0] * 100))

        # 创建包含 'Word' 和 'Count' 列的 DataFrame，用于更新图表
        row_data = pd.DataFrame(result.iloc[[i]])
        chart.add_rows(row_data.set_index('Word'))

        # 更新进度条
        progress_bar.progress((i + 1) / result.shape[0])

        # 等待一小段时间，模拟进度
        time.sleep(0.05)

    # 清空进度条
    progress_bar.empty()
    st.write("x轴为关键词,y轴为词频")
    # 重新运行按钮
    st.button("重新运行")
    col1, col2 = st.columns(2)
    # 获取排名前10的关键词数据
    top_10_word = result.sort_values("Count", ascending=False).head(10)
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(top_10_word["Word"], top_10_word["Count"], marker='o', label='词频', color="#DAA520")
        ax.set_title('Exner Pavel学术成果关键词排名前10', fontproperties=font)
        ax.set_xlabel('关键词', fontproperties=font)
        ax.set_ylabel('词频', fontproperties=font)
        ax.legend(prop=font)

        # 在Streamlit中显示图表
        st.pyplot(fig)
        st.write("Exner Pavel学术成果关键词主要是：spectral,quantum,interaction,operators,graphs,delta"
                 "也即谱分析、光谱学或与频谱量子力学、量子物理学，相互作用")
    with col2:
        st.dataframe(top_10_word)

# 画第二个图
with tab2:
    # 画图左边柱状图右边饼图
    col1, col2 = st.columns(2)
    title = 18
    label = 15
    ticks = 8
    fig2, ax2 = plt.subplots()
    sns.set(style="darkgrid")
    sns.barplot(x='Lastname', y='Count', data=top_lastnames, color="#75BDE3", width=0.5)

    ax2.set_title('2019年12月arXiv上发表论文数量前10姓氏', fontproperties=font, fontsize=title)
    ax2.set_xlabel('姓氏', fontproperties=font, fontsize=label)
    ax2.set_ylabel('发表论文数量', fontproperties=font, fontsize=label)
    ax2.tick_params(axis='both', labelsize=8, width=2)  # 调整刻度文本大小为8，刻度线的宽度为2
    plt.tight_layout()

    st.pyplot(fig2)
    st.markdown("### 发布论文数量排名前一百100个姓氏词云图")
    top_n = 100
    top_df = lastname_counts.head(top_n)

    # 设置字体大小
    t_size = 18

    # 创建词云图
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(
        dict(zip(top_df["Lastname"], top_df["Count"])))

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("".format(top_n), fontsize=t_size, fontproperties=font)

    # 在Streamlit中显示图表
    st.pyplot(plt.gcf())

st.markdown("### 小节：2019年12月发表论文数量最多的是" +
            str(most_authors['Author'][0]) + "一共发表了"
            + str(most_authors['Count'][0]) + "篇论文并且姓"
            + str(lastname_counts['Lastname'][0]) + "论文作者发表数量最多,他们一共发表了"
            + str(lastname_counts['Count'][0]) + "篇论文")

st.markdown("## 从作者的不同领域来探索学术前沿")

# 将数据分类后进行统计
group = data[['categories', 'authors_parsed']]
group = group.groupby(['categories'])

# 获取每个组的长度
group_lengths_top10_name = list(group.size().sort_values(ascending=False)[0:10].index)

# 用于存储所有符合条件的 one_authors
all_one_authors = []

for name, group_data in group:
    # name 是组的名字，group_data 是该组的数据
    flag = 0
    # 合并作者名字
    for i in group_lengths_top10_name:
        if i in name:
            categories = i
            flag = 1
            break
    if flag == 0:
        continue

    all_authors = sum(group_data['authors_parsed'], [])
    authors_names = [' '.join(x) for x in all_authors]
    authors_names = pd.DataFrame(authors_names)

    # 获取排名第一的作者
    one_authors = authors_names.value_counts().head(1).reset_index()
    one_authors['categories'] = categories

    # 将当前 one_authors 添加到列表中
    all_one_authors.append(one_authors)

# 使用 concat 函数将所有 one_authors 合并成一个 DataFrame
result_df = pd.concat(all_one_authors, ignore_index=True)

col1, col2 = st.columns(2)
with col1:
    st.write("更新论文前十领域数量统计")
    st.dataframe(result_df)
with col2:
    tab1, tab2 = st.tabs(["作者论文更新数量图", "作者领域论文关系图"])
    with tab1:
        # 颜色搭配1: 蓝绿搭配
        color_line = "#3498db"
        color_bar = "#2ecc71"
        # 在Streamlit中绘制折线图和柱状图
        fig, ax1 = plt.subplots(figsize=(12, 8))
        ax1.set_title('热门领域发表论文数量第一的作者', fontproperties=font, fontsize=40)
        # 绘制折线图
        ax1.plot(result_df[0].values, result_df["count"].values, color=color_line, label='发表论文数量')
        ax1.set_xlabel('作者名字', fontproperties=font, fontsize=30)
        ax1.set_ylabel('发表论文数量', fontproperties=font, fontsize=30)
        ax1.tick_params('y', colors=color_line)

        # 创建第二个y轴，共享x轴
        ax2 = ax1.twinx()
        ax2.bar(result_df[0].values, result_df["count"].values, color=color_bar, alpha=0.5, label='发表论文数量')

        # 添加图例
        ax1.set_xticks(result_df.index)
        ax1.set_xticklabels(result_df[0].values, rotation=45)
        ax1.set_xlim(-0.5, len(result_df) - 0.5)
        ax1.legend(loc='upper left', prop=font)
        # 在Streamlit中显示图表
        st.pyplot(fig)
    with tab2:
        # 设置字体大小
        t_size = 18
        l_size = 15

        # 创建散点图
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(result_df[0].values, result_df["categories"].values, c=result_df["count"].values,
                              alpha=0.8,
                              s=result_df["count"].values * 50,
                              cmap='Oranges')
        plt.title("领域, 作者，更新论文数量", fontsize=t_size, fontproperties=font)
        plt.xlabel("作者", fontsize=l_size, fontproperties=font)
        plt.ylabel("领域", fontsize=l_size, fontproperties=font)
        plt.colorbar()

        # 旋转横坐标刻度标签
        plt.xticks(rotation=45)

        # 在Streamlit中显示图表
        st.pyplot(plt.gcf())

st.markdown("### 我们通过图看出cs.CV,cs.LG stat.ML,hep-ph,math.AG,math.AP,math.CO"
            "是比较火的的领域，其中Hopkins Sam12发表的比较多,他所研究的领域是Hopkins Sam")
