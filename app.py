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

# --- 🚀 核心数据桥梁：强力打通本地词库文件 ---
DEFAULT_VOCAB = [
    {"word": "Opera", "meaning": "歌剧", "pos": "核心术语"},
    {"word": "Canto", "meaning": "声乐 / 演唱", "pos": "核心术语"},
    {"word": "Soprano", "meaning": "女高音", "pos": "声部分类"},
    {"word": "Tenore", "meaning": "男高音", "pos": "声部分类"}
]

# 优先读取实体 vocab_data.py 文件
final_vocab_source = DEFAULT_VOCAB
final_repertoire_source = {
    "《茶花女》- 饮酒歌 (Libiamo ne' lieti calici)": [
        {"original": "Libiamo, libiamo ne' lieti calici", "translation": "让我们高举起欢乐的酒杯"},
        {"original": "che la bellezza infiora", "translation": "这迷人的美景使人心醉"}
    ]
}

try:
    import vocab_data
    # 强制重新加载，确保文件内所有大词库被强行注入
    import importlib
    importlib.reload(vocab_data)
    
    if hasattr(vocab_data, "MEGA_VOCAB") and len(vocab_data.MEGA_VOCAB) >= 4:
        final_vocab_source = vocab_data.MEGA_VOCAB
    if hasattr(vocab_data, "LYRIC_REPERTOIRE"):
        final_repertoire_source = vocab_data.LYRIC_REPERTOIRE
except Exception:
    pass

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 核心状态初始化（确保第一次加载就把完整大词库灌进去） ---
if "vocab" not in st.session_state:
    st.session_state.vocab = final_vocab_source

if "memory_pool" not in st.session_state:
    st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in st.session_state.vocab}

if "browse_index" not in st.session_state:
    st.session_state.browse_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

# --- 侧边栏控制面板 ---
st.sidebar.title("🎒 词库控制面板")

# 增加一个物理刷新按钮，万一卡住可以手动一键归位
if st.sidebar.button("🔄 强行重载本地大词库文件", use_container_width=True):
    st.session_state.vocab = final_vocab_source
    st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in final_vocab_source}
    st.session_state.browse_index = 0
    st.session_state.current_quiz = None
    st.rerun()

uploaded_file = st.sidebar.file_uploader("导入外部额外词库 (CSV)", type=["csv"], key="sidebar_uploader")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "word" in df.columns and "meaning" in df.columns:
            if "pos" not in df.columns:
                df["pos"] = "自定义导入"
            new_vocab = df.to_dict(orient="records")
            st.session_state.vocab = new_vocab
            st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in new_vocab}
            st.sidebar.success(f"成功导入 {len(new_vocab)} 个外部单词！")
        else:
            st.sidebar.error("CSV 文件必须包含 'word' 和 'meaning' 两列！")
    except Exception as e:
        st.sidebar.error(f"读取失败: {e}")

wrong_count = sum(1 for v in st.session_state.memory_pool.values() if v["is_wrong"])
st.sidebar.metric(label="🔴 当前顽固错题数", value=f"{wrong_count} 题")

st.title("🇮🇹 意音圣经 · 声乐歌剧背词宝")
st.caption("为中国留学生量身定制的音乐学院上课、排练、剧院生存刚需高频词库")

tab1, tab2, tab3, tab4 = st.tabs(["📖 实战泛读速记", "🕹️ 考前通关测试", "🎵 歌剧歌词自由泛读", "🗂️ 核心单词总表"])

# ==================== 选项卡 1：浏览模式 ====================
with tab1:
    vocab = st.session_state.vocab
    idx = st.session_state.browse_index
    if vocab and idx < len(vocab):
        current_word = vocab[idx]
        
        # 补全分类标签的安全提取
        c_tag = current_word.get('pos', '通用词汇')
        if not str(c_tag).strip() or pd.isna(c_tag):
            c_tag = "通用词汇"
            
        st.info(f"🇮🇹 单词： {current_word['word']}   [{c_tag}]")
        st.success(f"🇨🇳 释义： {current_word['meaning']}")
        
        audio_file = get_local_audio(current_word['word'], prefix="word")
        if audio_file and os.path.exists(audio_file):
            st.audio(audio_file, format="audio/mp3")
        
        st.write(f"📊 词库进度: {idx + 1} / {len(vocab)}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 上一个单词", use_container_width=True, key="prev_btn") and idx > 0:
                st.session_state.browse_index -= 1
                st.rerun()
        with col2:
            if st.button("下一个单词 ➡️", use_container_width=True, key="next_btn") and idx < len(vocab) - 1:
                st.session_state.browse_index += 1
                st.rerun()

# ==================== 选项卡 2：测试模式 ====================
with tab2:
    vocab = st.session_state.vocab
    if len(vocab) < 4:
        st.warning("词库至少需要 4 个单词才能开启测试模式！")
    else:
        test_mode = st.radio("选择测试机制：", ["✨ 智能复习模式", "🎲 普通测试模式"], horizontal=True, key="test_mode_radio")
        st.divider()
        
        if st.session_state.current_quiz is None or st.session_state.current_quiz.get("mode_at_birth") != test_mode:
            current_time = time.time()
            ten_days_in_seconds = 10 * 24 * 60 * 60
            if "智能复习模式" in test_mode:
                wrong_pool = [item for item in vocab if st.session_state.memory_pool.get(item['word'], {}).get("is_wrong", False)]
                if wrong_pool: correct_item = random.choice(wrong_pool)
                else:
                    review_pool = [item for item in vocab if (current_time - st.session_state.memory_pool.get(item['word'], {}).get("last_correct_time", 0)) > ten_days_in_seconds]
                    correct_item = random.choice(review_pool) if review_pool else random.choice(vocab)
            else: 
                correct_item = random.choice(vocab)
            
            options = [correct_item['meaning']]
            while len(options) < 4:
                wrong_opt = random.choice(vocab)['meaning']
                if wrong_opt not in options: options.append(wrong_opt)
            random.shuffle(options)
            
            st.session_state.current_quiz = {
                "word": correct_item['word'], 
                "correct": correct_item['meaning'], 
                "options": options, 
                "mode_at_birth": test_mode
            }
        
        quiz = st.session_state.current_quiz
        st.metric(label="🎯 答对率", value=f"{st.session_state.quiz_score} / {st.session_state.quiz_total}")
        
        is_w = st.session_state.memory_pool.get(quiz['word'], {}).get("is_wrong", False)
        badge = "⚠️ 顽固错题重现：" if is_w and "智能复习模式" in test_mode else "请听题："
        st.write(badge)
        st.subheader(f"🎵 意语单词：{quiz['word']}")
        
        quiz_audio = get_local_audio(quiz['word'], prefix="quiz")
        if quiz_audio and os.path.exists(quiz_audio):
            st.audio(quiz_audio, format="audio/mp3")
        
        st.write("")
        
        for option in quiz['options']:
            if st.button(option, use_container_width=True, key=f"quiz_opt_{option}"):
                st.session_state.quiz_total += 1
                if option == quiz['correct']:
                    st.toast("🎉 答对了！", icon="✅")
                    st.session_state.quiz_score += 1
                    st.session_state.memory_pool[quiz['word']]["is_wrong"] = False
                    st.session_state.memory_pool[quiz['word']]["last_correct_time"] = time.time()
                else:
                    st.toast(f"❌ 答错啦！正解是：{quiz['correct']}", icon="🚨")
                    st.session_state.memory_pool[quiz['word']]["is_wrong"] = True
                
                st.session_state.current_quiz = None
                st.rerun()

# ==================== 选项卡 3：歌词自由泛读 ====================
with tab3:
    st.subheader("🎼 歌剧歌词智能泛读面板")
    
    lyric_source = st.radio("选择歌词来源：", ["📋 自由复制粘贴全新歌词", "📚 浏览经典内置唱段"], horizontal=True, key="lyric_src_radio")
    
    final_lyrics = []
    input_title = ""
    
    if lyric_source == "📋 自由复制粘贴全新歌词":
        st.markdown("#### 📥 请在下方粘贴你的意大利语歌词")
        input_title = st.text_input("给这首歌曲起个名字（可选）：", placeholder="例如：Aria di Chiesa", key="song_title_input")
        
        user_lyric_text = st.text_area(
            "把整段意大利语歌词直接粘贴在下面：", 
            placeholder="Libiamo, libiamo ne' lieti calici...",
            height=150,
            key="lyrics_text_area"
        )
        
        if user_lyric_text.strip():
            raw_lines = [line.strip() for line in user_lyric_text.split("\n") if line.strip()]
            for line in raw_lines:
                if len(line) > 50:
                    split_line = re.split(r'[,.;?!]', line)
                    for sub in split_line:
                        if sub.strip():
                            final_lyrics.append({"original": sub.strip(), "translation": "自定义输入"})
                else:
                    final_lyrics.append({"original": line, "translation": "自定义输入"})
    
    else:
        chosen_opera = st.selectbox("请选择要排练精读的内置唱段：", list(final_repertoire_source.keys()), key="opera_select")
        final_lyrics = final_repertoire_source[chosen_opera]

    if final_lyrics:
        st.divider()
        display_title = input_title if lyric_source == '📋 自由复制粘贴全新歌词' and input_title else '选定唱段'
        st.markdown(f"### 🎵 正在精读演练：{display_title}")
        
        for idx, line in enumerate(final_lyrics):
            col_text, col_play = st.columns([5, 3])
            with col_text:
                st.warning(f"🇮🇹 {line['original']}")
                if lyric_source != "📋 自由复制粘贴全新歌词":
                    st.info(f"🇨🇳 {line['translation']}")
            with col_play:
                lyric_audio = get_local_audio(line['original'], prefix=f"lyr_{idx}")
                if lyric_audio and os.path.exists(lyric_audio):
                    st.audio(lyric_audio, format="audio/mp3")
            st.divider()
    else:
        st.info("💡 期待你的台词！请在上方框中粘贴歌词。")

# ==================== 🗂️ 选项卡 4：核心单词总表 ====================
with tab4:
    st.subheader("🗂️ 词库字典总表面板")
    st.caption("以下单词根据功能或词性自动归类。点击单词折叠抽屉，可直接查看中文含义并播放纯正发音。")
    
    vocab_list = st.session_state.vocab
    
    if not vocab_list:
        st.info("💡 当前词库空空如也，请先在左侧侧边栏导入词库。")
    else:
        categories = {}
        for item in vocab_list:
            tag = item.get('pos', '').strip() if item.get('pos') else ""
            if not tag or pd.isna(tag):
                tag = "通用高频词"
            if tag not in categories:
                categories[tag] = []
            categories[tag].append(item)
            
        for cat_name, items in categories.items():
            st.markdown(f"#### 📦 {cat_name} ({len(items)} 个词)")
            
            for word_idx, word_item in enumerate(items):
                w_text = word_item['word']
                w_meaning = word_item['meaning']
                
                with st.expander(f"🇮🇹 {w_text}", expanded=False):
                    col_m, col_a = st.columns([5, 3])
                    with col_m:
                        st.info(f"🇨🇳 中文释义：{w_meaning}")
                    with col_a:
                        dict_audio = get_local_audio(w_text, prefix=f"dict_{cat_name}_{word_idx}")
                        if dict_audio and os.path.exists(dict_audio):
                            st.audio(dict_audio, format="audio/mp3")
            st.write("")
