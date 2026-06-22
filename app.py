import streamlit as st
import random
import os

# --- 简单且稳固的初始化 ---
st.set_page_config(page_title="背词宝", layout="centered")

# 设置默认词库
if "vocab" not in st.session_state:
    st.session_state.vocab = [
        {"word": "Spartito", "meaning": "乐谱", "pos": "音乐基础词汇"},
        {"word": "Ripetere", "meaning": "重复", "pos": "上课常用词汇"},
        {"word": "Sipario", "meaning": "帷幕", "pos": "排练演出词汇"}
    ]

# 侧边栏按钮：暴力重置
if st.sidebar.button("🚨 强制重置词库"):
    st.session_state.clear()
    st.rerun()

st.title("意音圣经 · 背词宝")
tab1, tab2, tab3, tab4 = st.tabs(["泛读", "测试", "歌词", "总表"])

with tab4:
    st.subheader("核心单词总表")
    vocab = st.session_state.vocab
    
    # 简单的分类逻辑
    cats = {
        "🎵 音乐基础": [i for i in vocab if "基础" in i['pos']],
        "🏫 上课常用": [i for i in vocab if "上课" in i['pos']],
        "🎭 排练演出": [i for i in vocab if "排练" in i['pos']]
    }
    
    # 强制显示分类按钮
    choice = st.radio("选择场景", list(cats.keys()), horizontal=True)
    
    words_to_show = cats[choice]
    st.write(f"当前分类：{choice} (共 {len(words_to_show)} 个词)")
    
    for item in words_to_show:
        with st.expander(item['word']):
            st.write(item['meaning'])
