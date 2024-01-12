import streamlit as st
import time
import numpy as np
import pandas as pd
import os

# 获取当前脚本所在的目录
st.write("# 学术前沿趋势分析 👋")

st.sidebar.title("可视化结果")
st.sidebar.success("在上方选择一个演示。")

st.markdown(
    """
    arXiv 重要的学术公开网站，也是搜索、浏览和下载学术论文的重要工具。
    arXiv论文涵盖的范围非常广，涉及物理学的庞大分支和计算机科学的众多子学科，如数学、统计学、电气工程、定量生物学和经济学等等。
    本次赛题将使用arXiv在公开的论文数据集，希望各位选手通过数据分析能够挖掘出最近学术的发展趋势和学术关键词。
    ### 👈 从侧边栏演示我们的结果
"""
)

st.markdown("# 绘图演示")
st.sidebar.header("绘图演示")
st.write(
    """这个演示展示了 Streamlit 的绘图和动画组合。我们在一个循环中生成一些随机数大约5秒钟。希望你喜欢！"""
)
# 获取当前脚本所在的目录
import os

current_path = os.getcwd()  # 获取当前文件夹的绝对路径
relative_path = os.path.join(current_path, '2019-12.csv')  # 构建相对路径

data = pd.read_csv(relative_path, parse_dates=['update_date'], encoding='gbk')

st.title('2019年12月份每天发表论文的数量')
group = data.groupby(data.update_date.dt.day)
num = []
data_date = pd.DataFrame(columns=["论文数量"])

for date, group in data.groupby(['update_date']):
    num_g = group['update_date'].count()
    series = pd.Series({"论文数量": group['update_date'].count()}, name=date)  # 获取组内记录数目
    data_date = data_date._append(series)

# 尝试处理不符合格式的日期
try:
    data_date.index = pd.to_datetime(data_date.index).strftime('%d')  # 简化日期转换
except (TypeError, ValueError):
    # 提取日期部分
    data_date.index = data_date.index.map(lambda x: x[0].day)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
st.text("x轴表示2019年12月份的每天，y轴表示2019年12月份每天发表的论文数")
# 创建空容器
container = st.empty()

# 模拟数据更新和进度条
for i in range(1, 31, 1):
    # 更新状态文本
    status_text.text("完成%i%%" % (i * 3.33))

    # 更新折线图数据
    new_values = data_date.head(i)

    # 更新图表
    chart = container.line_chart(data=new_values, use_container_width=True)

    # 更新进度条
    progress_bar.progress(i * 3)
    # 等待一小段时间，模拟进度
    time.sleep(0.4)

# 清空进度条
progress_bar.empty()

# 重新运行按钮
st.button("重新运行")

# import pandas as pd
# import matplotlib.pyplot as plt
#
# relative_path = "../2019-12.csv"
#
# data = pd.read_csv(relative_path, encoding='ISO-8859-1')
#
# datas = pd.DataFrame(data)
# # 转换数据形式
# datas['title'].to_csv('result.txt', index=False, sep=' ', encoding='utf_8_sig')
# relative_path = "../result.txt"
# text = open(relative_path, encoding="utf-8").read()  # 标明文本路径，打开
#
# import wordcloud
# from wordcloud import ImageColorGenerator
# from PIL import Image
#
# st.title('2019年12月份学术研究热门关键词')
#
# # 读取图片
# relative_path = "../great.png"
# pic = np.array(Image.open(relative_path))
# image_colors = ImageColorGenerator(pic)  # 生成图片颜色中的颜色
# wd = wordcloud.WordCloud(
#     mask=pic,  # 背景图形,如果根据图片绘制，则需要设置
#     font_path='simhei.ttf',  # 可以改成自己喜欢的字体
#     background_color='white',  # 词云图背景颜色可以换成自己喜欢的颜色
# )
# wd.generate(text)
# fig, ax = plt.subplots()  # 生成词云
# # 图片颜色渲染词云图的颜色，用color_func指定
# ax.imshow(wd.recolor(color_func=image_colors), interpolation='bilinear')
#
# ax.axis("off")
# st.pyplot(fig)
# st.text("关键词展示着学术研究的趋势：量子、神经网络、深度学习、图论...")
# # plt.show()
