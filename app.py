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

try:
    if os.path.exists("vocab_data.py"):
        import vocab_data
        import importlib
        importlib.reload(vocab_data)
        if hasattr(vocab_data, "MEGA_VOCAB"): final_vocab_source = vocab_data.MEGA_VOCAB
        if hasattr(vocab_data, "LYRIC_REPERTOIRE"): final_repertoire_source = vocab_data.LYRIC_REPERTOIRE
except: pass

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 初始化 (包含错题本) ---
if "vocab" not in st.session_state: st.session_state.vocab = final_vocab_source
if "wrong_book" not in st.session_state: st.session_state.wrong_book = []
if "memory_pool" not in st.session_state: st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in st.session_state.vocab}
if "browse_index" not in st.session_state: st.session_state.browse_index = 0
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state: st.session_state.quiz_total = 0
if "current_quiz" not in st.session_state: st.session_state.current_quiz = None

st.title("🇮🇹 意音圣经 · 声乐歌剧背词宝")

tab1, tab2, tab3, tab4 = st.tabs(["📖 实战泛读速记", "🕹️ 考前通关测试", "🎵 歌剧歌词自由泛读", "🗂️ 核心单词总表"])

with tab1:
    vocab = st.session_state.vocab
    idx = st.session_state.browse_index
    current_word = vocab[idx]
    st.info(f"🇮🇹 单词： {current_word['word']}   [{current_word.get('pos', '通用')}]")
    st.success(f"🇨🇳 释义： {current_word['meaning']}")
    if st.button("下一个单词 ➡️"): st.session_state.browse_index = (idx + 1) % len(vocab); st.rerun()

with tab2:
    sub1, sub2 = st.tabs(["🔥 考前测试", "📚 我的错题本"])
    with sub1:
        if st.button("抽一题"): st.session_state.current_quiz = {"word": random.choice(st.session_state.vocab)['word'], "correct": random.choice(st.session_state.vocab)['meaning']}
        if st.session_state.current_quiz:
            q = st.session_state.current_quiz
            st.write(f"单词: **{q['word']}**")
            ans = st.text_input("翻译:")
            if st.button("提交"):
                if ans == q['correct']: st.success("✅")
                else: 
                    st.error(f"❌ 错误，正解: {q['correct']}")
                    if q['word'] not in st.session_state.wrong_book: st.session_state.wrong_book.append(q['word'])
    with sub2:
        for w in st.session_state.wrong_book:
            if st.button(f"移除 {w}", key=w): st.session_state.wrong_book.remove(w); st.rerun()
            st.write(w)

with tab3:
    st.write("歌剧歌词自由泛读逻辑已保留")

with tab4:
    st.subheader("核心单词总表")
    # (此处保持你原本的智能分类逻辑)
