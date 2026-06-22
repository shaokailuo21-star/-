import streamlit as st
import random
import os

# 1. 页面配置
st.set_page_config(page_title="意音圣经 · 背词宝", layout="centered")

# 2. 初始化缓存
if "vocab" not in st.session_state:
    # 这里加载你的大词库，如果词库太大，建议放到 vocab_data.py 里加载
    st.session_state.vocab = [
        {"word": "Spartito", "meaning": "乐谱", "pos": "音乐基础"},
        {"word": "Ripetere", "meaning": "重复", "pos": "上课常用"},
        {"word": "Sipario", "meaning": "帷幕", "pos": "排练演出"}
    ]

# 侧边栏
if st.sidebar.button("🚨 重置所有数据"):
    st.session_state.clear()
    st.rerun()

st.title("🇮🇹 意音圣经 · 背词宝")

# 3. 四大板块
tab1, tab2, tab3, tab4 = st.tabs(["📖 泛读", "🕹️ 测试", "🎵 歌词", "🗂️ 总表"])

with tab1:
    st.write("浏览模式：这里展示所有单词。")
    # 此处放置你之前的浏览逻辑...

with tab2:
    st.write("测试模式：考前通关。")
    # 此处放置你之前的测试逻辑...

with tab3:
    st.write("歌词模式：泛读练习。")
    # 此处放置你之前的歌词逻辑...

with tab4:
    st.subheader("核心单词总表")
    vocab = st.session_state.vocab
    
    # 智能分类逻辑：强制将所有词分配到四个桶
    categories = {
        "🎵 音乐基础": [i for i in vocab if "基础" in str(i.get('pos', '')) or "音" in str(i.get('meaning', ''))],
        "🏫 上课常用": [i for i in vocab if "上课" in str(i.get('pos', '')) or "重复" in str(i.get('meaning', ''))],
        "🎭 排练演出": [i for i in vocab if "排练" in str(i.get('pos', '')) or "台" in str(i.get('meaning', ''))],
        "🌍 其他": [i for i in vocab if not any(k in str(i.get('pos', '')) + str(i.get('meaning', '')) for k in ["基础", "上课", "排练"])]
    }
    
    # 使用 radio 确保分类按钮一定出现
    choice = st.radio("选择分类场景：", list(categories.keys()), horizontal=True)
    
    words = categories[choice]
    st.write(f"当前分类：{choice} (共 {len(words)} 个词)")
    
    for item in words:
        with st.expander(f"{item['word']} - {item['meaning']}"):
            st.write(f"详细释义: {item['meaning']}")
