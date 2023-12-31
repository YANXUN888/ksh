import streamlit as st
from PIL import Image
import os

# st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("# 论文代码提交")
# st.sidebar.header("DataFrame Demo")
st.write(
    """"""
)
script_dir = os.path.dirname(os.path.abspath(__file__))
tab1, tab2 = st.tabs(["数据分析", "源代码所占比例"])

with tab1:
    st.header("有无图表数据占比")
    relative_path = 'img/2019年12月论文在8大类中占比.png'
    image1 = Image.open(os.path.join(script_dir, relative_path))
    st.image(image1, caption='有无图表数据占比')
    st.header("有无页数对比")
    relative_path = 'img/有无页数对比.png'
    image1 = Image.open(os.path.join(script_dir, relative_path))
    st.image(image1, caption='有无页数对比')
    st.header("有无页数对比")
    relative_path = 'img/各主要类别平均页数.png'
    image1 = Image.open(os.path.join(script_dir, relative_path))
    st.image(image1, caption='各主要类别平均页数')
    st.write(
        """在进行论文的页数统计后，得到了论文有页数和无页数的数据占比。
        有无页数大概各一半的比例，有图表的论文相对较少
        同时也获取到了20个主要类别的平均页数，可以看到，eess类的平均页数最多"""
    )

with tab2:
    st.header("含源代码论文的数量")
    relative_path = 'img/所有论文类别下包含源代码论文的数量.png'
    image1 = Image.open(os.path.join(script_dir, relative_path))
    st.image(image1, caption='所有论文类别下包含源代码论文的数量')
    st.header("含源代码论文占所在类别的比例")
    relative_path = 'img/所有论文类别下包含源代码论文的比例.png'
    image1 = Image.open(os.path.join(script_dir, relative_path))
    st.image(image1, caption='所有论文类别下包含源代码论文的比例')
    st.write(
        """通过对论文数据集的comments 和abstract查找github，查找到了有源码论文的论文并计算出了数量，
        最后画出了在各个论文类别下源代码论文饼图，可以看到计算机科学论文类别下包含源代码论文占计算机
        科学类别论文的比例最大，侧面反映出了计算机科学类语言参考的源代码比较多，学习时也需要参考。"""
    )
