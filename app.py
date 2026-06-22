import streamlit as st
import random
import os
import re
from gtts import gTTS

# --- 1. 基础配置 ---
st.set_page_config(page_title="意音圣经 · 歌剧背词宝", layout="wide")

# --- 2. 核心状态初始化 (确保所有数据结构都完整) ---
if "initialized" not in st.session_state:
    try:
        import vocab_data
        st.session_state.vocab = vocab_data.MEGA_VOCAB
        st.session_state.repertoire = vocab_data.LYRIC_REPERTOIRE
    except:
        st.session_state.vocab = [{"word": "Spartito", "meaning": "乐谱", "pos": "音乐基础"}]
        st.session_state.repertoire = {}
    
    st.session_state.browse_index = 0
    st.session_state.memory_pool = {item['word']: False for item in st.session_state.vocab}
    st.session_state.initialized = True

# --- 3. 音频生成器 (功能还原) ---
def get_local_audio(text):
    if not os.path.exists("audios"): os.makedirs("audios")
    path = f"audios/{text}.mp3"
    if not os.path.exists(path):
        tts = gTTS(text=text, lang='it')
        tts.save(path)
    return path

# --- 4. 四大板块 (功能完整还原) ---
tab1, tab2, tab3, tab4 = st.tabs(["📖 实战泛读", "🕹️ 智能测试", "🎵 歌词泛读", "🗂️ 核心分类总表"])

with tab1:
    st.header("实战泛读速记")
    idx = st.session_state.browse_index
    item = st.session_state.vocab[idx]
    st.subheader(f"🇮🇹 {item['word']}")
    st.write(f"🇨🇳 {item['meaning']}")
    st.audio(get_local_audio(item['word']))
    if st.button("⬅️ 上一个"): st.session_state.browse_index = (idx - 1) % len(st.session_state.vocab); st.rerun()
    if st.button("下一个 ➡️"): st.session_state.browse_index = (idx + 1) % len(st.session_state.vocab); st.rerun()

with tab2:
    st.header("智能记忆测试")
    if st.button("抽一题进行测试"):
        q = random.choice(st.session_state.vocab)
        st.write(f"请翻译: **{q['word']}**")
        if st.checkbox("查看答案"): st.success(q['meaning'])

with tab3:
    st.header("歌剧歌词精读")
    options = list(st.session_state.repertoire.keys())
    if options:
        sel = st.selectbox("选择唱段", options)
        for line in st.session_state.repertoire[sel]:
            st.warning(line['original'])
            st.info(line['translation'])

with tab4:
    st.header("核心单词总表")
    # 这一块是分类的灵魂
    # 如果你的 pos 字段不标准，我们可以通过 meaning 字段来强制归类
    def classify(item):
        m = item.get('meaning', '')
        p = item.get('pos', '')
        if any(x in m+p for x in ["谱", "音", "唱", "拍", "节"]): return "🎵 音乐基础"
        if any(x in m+p for x in ["重复", "开始", "停", "听", "看", "明白", "错"]): return "🏫 上课常用"
        if any(x in m+p for x in ["台", "幕", "演", "排练", "服装", "位置"]): return "🎭 排练演出"
        return "🌍 其他生存"

    # 分组逻辑
    groups = {"🎵 音乐基础": [], "🏫 上课常用": [], "🎭 排练演出": [], "🌍 其他生存": []}
    for item in st.session_state.vocab:
        groups[classify(item)].append(item)
    
    # 交互式分类展示
    cat = st.radio("选择分类场景，点击即可展开单词：", list(groups.keys()), horizontal=True)
    st.write(f"当前分类共有 {len(groups[cat])} 个词")
    
    for item in groups[cat]:
        with st.expander(f"🇮🇹 {item['word']}  |  🇨🇳 {item['meaning']}"):
            st.audio(get_local_audio(item['word']))    st.subheader("考前通关测试")
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
