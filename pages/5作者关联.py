import pandas as pd
import matplotlib.pyplot as plt
import json
import networkx as nx
import streamlit as st
import os
st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="Mapping Demo", page_icon="")

st.markdown("# 论文作者统计")
st.sidebar.header("论文作者统计")
st.write(
    """我们探讨论文作者之间的关系"""
)


def readArxivFile(path, columns=['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref', 'doi',
                                 'report-no', 'categories', 'license', 'abstract', 'versions',
                                 'update_date', 'authors_parsed'], count=None):
    data = []
    with open(path, 'r') as f:
        for idx, line in enumerate(f):
            if idx == count:
                break
            d = json.loads(line)
            d = {col: d[col] for col in columns}
            data.append(d)

    data = pd.DataFrame(data)
    return data


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 回到上一级目录
    parent_dir = os.path.dirname(script_dir)
    print(parent_dir)
    # 导入数据
    relative_path = 'arxiv-metadata-oai-2019.json'
    data_dir = os.path.join(parent_dir, relative_path)
    data = readArxivFile(data_dir, ['id', 'authors_parsed'])
    print(data)
    # 创建无向图
    G = nx.Graph()
    # 只用五篇论文进行构建
    for row in data.iloc[:10].itertuples():
        # 如果我们500片论文构建图，则可以得到更加完整作者关系，并选择最大联通子图进行绘制，折线图为子图节点度值。
        # itertuples:将DataFrame迭代成元组eg:[['Dugmore', 'B.','' ], ['Ntumba', 'PP.','' ]] -->  Pandas(Index=1, id='0704.0342', authors_parsed=[['Dugmore', 'B.', ''], ['Ntumba', 'PP.', '']])['Dugmore B.', 'Ntumba PP.']
        print(row)
        print(row[0])
        print(row[1])
        authors = row[2]
        print(authors)
        authors = [' '.join(x[:-1]) for x in authors]  # --> ['Dugmore B.', 'Ntumba PP.']

        # 把第一个作者与其他作者链接起来
        for author in authors[1:]:
            G.add_edge(authors[0], author)  # 即以1结点为中心节点

    # 绘制图像
    nx.draw(G, with_labels=True)
    # plt.show()
    st.pyplot()
    try:
        print(nx.dijkstra_path(G, 'Podsiadlowski Philipp', 'Rosswog Stephan'))  # 求两顶点间的最短路径
    except:
        print('No path')
    # 绘制最大连通子图
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # 将各个顶点的度的大小，降序排列
    # dmax = max(degree_sequence)#得到图中顶点最大的度

    plt.loglog(degree_sequence, "b-", marker="o")
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")

    # 嵌入最大连通子图
    plt.axes([0.45, 0.45, 0.45, 0.45])
    # sorted( nx.connected_components(G),key = len ,reverse = True )： 所有连通子图的降序排列，Gcc即是最大连通子图
    Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

    pos = nx.spring_layout(Gcc)
    plt.axis("off")
    nx.draw_networkx_nodes(Gcc, pos, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
    # plt.show()
    st.pyplot()
