import streamlit as st
import random
import time

# 1. 强制页面布局
st.set_page_config(page_title="意音圣经 · 背词宝", layout="centered")

# 2. 初始化核心数据（保底词库）
if "vocab" not in st.session_state:
    st.session_state.vocab = [
        {"word": "Spartito", "meaning": "乐谱", "pos": "音乐基础"},
        {"word": "Ripetere", "meaning": "重复", "pos": "上课常用"},
        {"word": "Sipario", "meaning": "帷幕", "pos": "排练演出"},
        {"word": "Soprano", "meaning": "女高音", "pos": "音乐基础"}
    ]
    st.session_state.browse_index = 0

# 3. 侧边栏
if st.sidebar.button("🔄 刷新词库数据"):
    st.rerun()

st.title("🇮🇹 意音圣经 · 背词宝")

# 4. 四大板块实现
tab1, tab2, tab3, tab4 = st.tabs(["📖 泛读", "🕹️ 测试", "🎵 歌词", "🗂️ 总表"])

# 板块 1：泛读模式
with tab1:
    st.subheader("实战泛读速记")
    idx = st.session_state.browse_index
    current = st.session_state.vocab[idx]
    st.info(f"单词: {current['word']}")
    st.success(f"含义: {current['meaning']}")
    if st.button("下一个单词"):
        st.session_state.browse_index = (idx + 1) % len(st.session_state.vocab)
        st.rerun()

# 板块 2：测试模式
with tab2:
    st.subheader("考前通关测试")
    if st.button("开始挑战"):
        q = random.choice(st.session_state.vocab)
        st.write(f"请问 {q['word']} 是什么意思？")
        st.write(f"答案是: {q['meaning']}")

# 板块 3：歌词模式
with tab3:
    st.subheader("歌剧歌词自由泛读")
    st.text_area("粘贴歌词进行练习：", height=100)
    st.write("请粘贴歌词并查看分段分析。")

# 板块 4：总表模式（带强制归类）
with tab4:
    st.subheader("核心单词总表")
    vocab = st.session_state.vocab
    
    # 将词库分类
    cats = {
        "🎵 音乐基础": [i for i in vocab if "基础" in i['pos']],
        "🏫 上课常用": [i for i in vocab if "上课" in i['pos']],
        "🎭 排练演出": [i for i in vocab if "排练" in i['pos']]
    }
    
    # 强制分类按钮
    choice = st.radio("场景切换", list(cats.keys()), horizontal=True)
    words = cats[choice]
    
    st.write(f"当前场景: {choice} (共 {len(words)} 个词)")
    for item in words:
        st.expander(item['word']).write(item['meaning'])
