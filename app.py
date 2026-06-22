# --- 🔴 强行将环境依赖安装提升至最顶端 🔴 ---
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
    if not text or not text.strip(): return None
    clean_filename = re.sub(r'[^\w]', '_', text.strip())[:30]
    file_path = f"local_audios/{prefix}_{clean_filename}.mp3"
    if not os.path.exists(file_path):
        try:
            short_text = text.strip()[:100]
            tts = gTTS(text=short_text, lang='it', slow=False)
            tts.save(file_path)
        except Exception: return None
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

# 强行动态解包
try:
    if os.path.exists("vocab_data.py"):
        import vocab_data
        import importlib
        importlib.reload(vocab_data)
        if hasattr(vocab_data, "MEGA_VOCAB"): final_vocab_source = vocab_data.MEGA_VOCAB
        if hasattr(vocab_data, "LYRIC_REPERTOIRE"): final_repertoire_source = vocab_data.LYRIC_REPERTOIRE
except: pass

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", layout="centered")

# --- 状态初始化 (保持原有逻辑) ---
if "vocab" not in st.session_state: st.session_state.vocab = final_vocab_source
if "wrong_book" not in st.session_state: st.session_state.wrong_book = [] # 错题本初始化
if "memory_pool" not in st.session_state: st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in st.session_state.vocab}
if "browse_index" not in st.session_state: st.session_state.browse_index = 0
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state: st.session_state.quiz_total = 0
if "current_quiz" not in st.session_state: st.session_state.current_quiz = None

st.title("🇮🇹 意音圣经 · 声乐歌剧背词宝")

tab1, tab2, tab3, tab4 = st.tabs(["📖 实战泛读速记", "🕹️ 考前通关测试", "🎵 歌剧歌词自由泛读", "🗂️ 核心单词总表"])

# --- 保持所有 Tab 的原有逻辑 (此处省略 Tab 1 和 Tab 3, 4，它们完全没变) ---
# ... 这里的 Tab 1, 3, 4 保持你之前的代码完全一致 ...

# ==================== 修改 Tab 2 以加入错题本 ====================
with tab2:
    sub_t1, sub_t2 = st.tabs(["🔥 开始测试", "📚 错题本库"])
    with sub_t1:
        # [这里放置你原来的测试代码逻辑]
        # 在答题判断处增加：
        # if 答错:
        #    if quiz['word'] not in st.session_state.wrong_book:
        #        st.session_state.wrong_book.append(quiz['word'])
    with sub_t2:
        st.write("### 你的错题本")
        for word in st.session_state.wrong_book:
            st.write(f"❌ {word}")
            if st.button(f"移除 {word}", key=f"del_{word}"):
                st.session_state.wrong_book.remove(word)
                st.rerun()
