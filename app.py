import streamlit as st
import random

# 设置页面
st.set_page_config(page_title="意音圣经", layout="centered")

# 1. 绝对安全的初始化逻辑
if "vocab" not in st.session_state:
    st.session_state.vocab = [
        {"word": "Spartito", "meaning": "乐谱", "pos": "音乐基础"},
        {"word": "Ripetere", "meaning": "重复", "pos": "上课常用"},
        {"word": "Sipario", "meaning": "帷幕", "pos": "排练演出"}
    ]
if "browse_index" not in st.session_state:
    st.session_state.browse_index = 0

st.title("🇮🇹 意音圣经 · 背词宝")

# 2. 四大板块
tab1, tab2, tab3, tab4 = st.tabs(["📖 泛读", "🕹️ 测试", "🎵 歌词", "🗂️ 总表"])

with tab1:
    st.subheader("实战泛读速记")
    # 只要 session_state 初始化了，这里就不会报错
    vocab = st.session_state.vocab
    idx = st.session_state.browse_index
    
    current = vocab[idx]
    st.info(f"单词: {current['word']}")
    st.success(f"含义: {current['meaning']}")
    
    if st.button("下一个"):
        st.session_state.browse_index = (idx + 1) % len(vocab)
        st.rerun()

with tab2:
    st.subheader("考前通关测试")
    st.write("点击按钮开始随机测试")
    if st.button("抽一题"):
        q = random.choice(st.session_state.vocab)
        st.write(f"单词: {q['word']}")
        st.write(f"含义: {q['meaning']}")

with tab3:
    st.subheader("歌剧歌词泛读")
    st.write("待开发内容")

with tab4:
    st.subheader("核心单词总表")
    # 定义分类，这里简单匹配
    cat_map = {
        "音乐基础": "基础",
        "上课常用": "上课",
        "排练演出": "排练"
    }
    
    choice = st.radio("选择分类", list(cat_map.keys()), horizontal=True)
    
    # 过滤筛选
    filtered = [i for i in st.session_state.vocab if cat_map[choice] in i['pos']]
    
    st.write(f"当前场景: {choice} (共 {len(filtered)} 个词)")
    for item in filtered:
        with st.expander(item['word']):
            st.write(item['meaning'])
