import streamlit as st
from PIL import Image
import pandas as pd
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="绘图演示", page_icon="📈")

st.markdown("# 以下是2019年12月计算机各个方向论文数量展示")
# st.sidebar.header("以下是2019年12月计算机各个方向论文数量展示")
st.write(
    """可以看到，论文共分为8大类。分别是："""
)
dict = {'Physics': '物理学',
        'Mathematics': '数学',
        'Computer Science': '计算机科学',
        'Statistics': '统计学',
        'Electrical Engineering and Systems Science': '电气工程与系统科学',
        'Quantitative Biology': '定量生物学',
        'Quantitative Finance': '量化金融',
        'Economics': '经济学'}
kinds = pd.DataFrame(list(dict.items()))
# print(kinds)
st.table(kinds)
relative_path = 'img/2019年12月论文在8大类中占比.png'
image1 = Image.open(os.path.join(script_dir, relative_path))
st.image(image1, caption='2019年12月论文在8大类中占比')
st.write(
    """由图可以看出，该数据集论文数量在8大类中占比有多有少，其中物理学类和数学类占比最多，计算机科学类次之，其他类的论文发表都比较少。"""
)
relative_path = "img/2019年12月论文在计算机各个方向的数量.png"
image2 = Image.open(os.path.join(script_dir, relative_path))
st.image(image2, caption='2019年12月论文在计算机各个方向的数量')
st.write(
    """其中，计算机科学大类里面的37个小类中论文的数量最多的是第7个小类，也就是'Computer Vision and Pattern Recognition'
    小类，发表了432篇学术论文。其余小类的论文发表数量都相对较小。"""
)
