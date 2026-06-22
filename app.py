# --- 🔴 强行将环境依赖安装提升至最顶端，防止云端加载报错 🔴 ---
import subprocess
import sys

try:
    from gtts import gTTS
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gTTS"])
    from gtts import gTTS

import streamlit as st
import random
import pandas as pd
import time
import os
import re

# --- 🎯 绝对稳定：本地静态音频管理器 ---
@st.cache_resource
def ensure_audio_dir():
    if not os.path.exists("local_audios"):
        os.makedirs("local_audios")

def get_local_audio(text, prefix=""):
    ensure_audio_dir()
    if not text or not text.strip():
        return None
    clean_filename = re.sub(r'[^\w]', '_', text.strip())[:30]
    file_path = f"local_audios/{prefix}_{clean_filename}.mp3"
    
    if not os.path.exists(file_path):
        try:
            short_text = text.strip()[:100]
            tts = gTTS(text=short_text, lang='it', slow=False)
            tts.save(file_path)
        except Exception:
            return None
    return file_path

# --- 🚀 核心数据物理注入器 ---
DEFAULT_VOCAB = [
    {"word": "Spartito", "meaning": "乐谱", "pos": "音乐基础词汇"},
    {"word": "Ripetere", "meaning": "再重复一遍", "pos": "上课常用词汇"},
    {"word": "Sipario", "meaning": "舞台帷幕", "pos": "排练演出词汇"},
    {"word": "Soprano", "meaning": "女高音", "pos": "音乐基础词汇"}
]

final_vocab_source = DEFAULT_VOCAB
final_repertoire_source = {
    "《茶花女》- 饮酒歌 (Libiamo ne' lieti calici)": [
        {"original": "Libiamo, libiamo ne' lieti calici", "translation": "让我们高举起欢乐的酒杯"},
        {"original": "che la bellezza infiora", "translation": "这迷人的美景使人心醉"}
    ]
}

debug_error_message = None
try:
    if os.path.exists("vocab_data.py"):
        import vocab_data
        import importlib
        importlib.reload(vocab_data)
        
        if hasattr(vocab_data, "MEGA_VOCAB") and isinstance(vocab_data.MEGA_VOCAB, list):
            final_vocab_source = vocab_data.MEGA_VOCAB
        if hasattr(vocab_data, "LYRIC_REPERTOIRE") and isinstance(vocab_data.LYRIC_REPERTOIRE, dict):
            final_repertoire_source = vocab_data.LYRIC_REPERTOIRE
except Exception as e:
    debug_error_message = f"读取 vocab_data.py 发生编译错误！错误详情：{str(e)}"

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 状态初始化 ---
if "vocab" not in st.session_state: st.session_state.vocab = final_vocab_source
if "wrong_book" not in st.session_state: st.session_state.wrong_book = []
if "is_wrong_quiz" not in st.session_state: st.session_state.is_wrong_quiz = False

if "memory_pool" not in st.session_state or len(st.session_state.memory_pool) < len(st.session_state.vocab):
    st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in st.session_state.vocab}

if "browse_index" not in st.session_state: st.session_state.browse_index = 0
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state: st.session_state.quiz_total = 0
if "current_quiz" not in st.session_state: st.session_state.current_quiz = None

# --- 侧边栏 ---
st.sidebar.title("🎒 词库控制面板")
if st.sidebar.button("🚨 强行擦除缓存，彻底刷新大词库", use_container_width=True):
    st.session_state.clear()
    st.rerun()

uploaded_file = st.sidebar.file_uploader("导入外部额外词库 (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state.vocab = df.to_dict(orient="records")
    st.rerun()

st.title("🇮🇹 意音圣经 · 声乐歌剧背词宝")
tab1, tab2, tab3, tab4 = st.tabs(["📖 实战泛读速记", "🕹️ 考前通关测试", "🎵 歌剧歌词自由泛读", "🗂️ 核心单词总表"])

with tab1:
    vocab = st.session_state.vocab
    idx = st.session_state.browse_index
    current_word = vocab[idx]
    st.info(f"🇮🇹 单词： {current_word['word']}   [{current_word.get('pos', '通用')}]")
    st.success(f"🇨🇳 释义： {current_word['meaning']}")
    if st.button("⬅️ 上一个单词", key="prev_btn") and idx > 0: st.session_state.browse_index -= 1; st.rerun()
    if st.button("下一个单词 ➡️", key="next_btn") and idx < len(vocab) - 1: st.session_state.browse_index += 1; st.rerun()

with tab2:
    sub_t1, sub_t2 = st.tabs(["🔥 考前测试", "📚 错题本闯关"])
    
    with sub_t1:
        # --- 原有测试逻辑 ---
        if st.session_state.current_quiz is None:
            if st.button("抽取题目"): st.session_state.current_quiz = random.choice(st.session_state.vocab); st.rerun()
        if st.session_state.current_quiz:
            q = st.session_state.current_quiz
            st.write(f"单词: **{q['word']}**")
            ans = st.text_input("翻译:")
            if st.button("提交"):
                if ans == q['meaning']: st.success("✅"); st.session_state.quiz_score += 1
                else: 
                    st.error(f"❌ 正解: {q['meaning']}")
                    if q['word'] not in st.session_state.wrong_book: st.session_state.wrong_book.append(q['word'])
                st.session_state.quiz_total += 1; st.session_state.current_quiz = None; st.rerun()

    with sub_t2:
        # --- 新增：错题闯关模式 ---
        if not st.session_state.wrong_book:
            st.success("目前没有错题，继续加油！")
        else:
            if not st.session_state.is_wrong_quiz:
                if st.button("🚀 开启错题专项闯关"): st.session_state.is_wrong_quiz = True; st.rerun()
                for w in st.session_state.wrong_book: st.write(f"❌ {w}")
            else:
                w_word = random.choice(st.session_state.wrong_book)
                w_item = next((i for i in st.session_state.vocab if i['word'] == w_word), None)
                st.subheader(f"复习中: {w_word}")
                ans = st.text_input("请输入中文释义:")
                if st.button("提交复习"):
                    if ans == w_item['meaning']:
                        st.success("✅ 掌握了！已移出。")
                        st.session_state.wrong_book.remove(w_word)
                        st.session_state.is_wrong_quiz = False
                        st.rerun()
                    else: st.error(f"❌ 不对，正解是: {w_item['meaning']}")
                if st.button("退出闯关"): st.session_state.is_wrong_quiz = False; st.rerun()

with tab3:
    st.write("歌词泛读逻辑...") # 这里保留你原有的完整代码

with tab4:
    st.write("总表逻辑...") # 这里保留你原有的完整代码
