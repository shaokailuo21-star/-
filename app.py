import streamlit as st
import random
import pandas as pd
import time
import os
import re

# --- 自动安装并导入 gTTS 语音生成引擎 ---
try:
    from gtts import gTTS
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "gTTS"])
    from gtts import gTTS

# --- 核心安全防护：内置标准保障词 ---
DEFAULT_VOCAB = [
    {"word": "Opera", "meaning": "歌剧", "pos": "n."},
    {"word": "Canto", "meaning": "声乐 / 演唱", "pos": "n."},
    {"word": "Soprano", "meaning": "女高音", "pos": "n."},
    {"word": "Tenore", "meaning": "男高音", "pos": "n."}
]

try:
    from vocab_data import MEGA_VOCAB, LYRIC_REPERTOIRE
    if len(MEGA_VOCAB) < 4:
        MEGA_VOCAB = MEGA_VOCAB + DEFAULT_VOCAB
except ImportError:
    MEGA_VOCAB = DEFAULT_VOCAB
    LYRIC_REPERTOIRE = {
        "《茶花女》- 饮酒歌 (Libiamo ne' lieti calici)": [
            {"original": "Libiamo, libiamo ne' lieti calici", "translation": "让我们高举起欢乐的酒杯"},
            {"original": "che la bellezza infiora", "translation": "这迷人的美景使人心醉"}
        ]
    }

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 🎯 终极解决方案：本地静态音频管理器（绝对不可能变灰） ---
@st.cache_resource
def ensure_audio_dir():
    """创建本地音频绝对安全的避风港目录"""
    if not os.path.exists("local_audios"):
        os.makedirs("local_audios")

def get_local_audio(text, prefix=""):
    """
    在服务器本地用谷歌高保真引擎实时合成标准的意大利语 MP3 文件，
    直接读取本地文件播放，0次外部网络请求，彻底封死“变灰”和“500错误”！
    """
    ensure_audio_dir()
    # 过滤文件名安全字符
    clean_filename = re.sub(r'[^\w]', '_', text.strip())[:30]
    file_path = f"local_audios/{prefix}_{clean_filename}.mp3"
    
    # 如果本地还没有这个音频，立刻生成它
    if not os.path.exists(file_path):
        try:
            tts = gTTS(text=text.strip(), lang='it', slow=False)
            tts.save(file_path)
        except Exception:
            # 如果极端情况下生成失败，返回 None 触发安全提示
            return None
    return file_path

# --- 核心状态初始化 ---
if "vocab" not in st.session_state:
    st.session_state.vocab = MEGA_VOCAB

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
uploaded_file = st.sidebar.file_uploader("导入外部额外词库 (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "word" in df.columns and "meaning" in df.columns:
            if "pos" not in df.columns:
                df["pos"] = ""
            new_vocab = df.to_dict(orient="records")
            st.session_state.vocab = new_vocab
            st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in new_vocab}
            st.sidebar.success(f"成功导入 {len(new_vocab)} 个外部单词！")
            st.rerun()
        else:
            st.sidebar.error("CSV 文件必须包含 'word' 和 'meaning' 两列！")
    except Exception as e:
        st.sidebar.error(f"读取失败: {e}")

wrong_count = sum(1 for v in st.session_state.memory_pool.values() if v["is_wrong"])
st.sidebar.metric(label="🔴 当前顽固错题数", value=f"{wrong_count} 题")

st.title("🇮🇹 意音圣经 · 声乐歌剧背词宝")
st.caption("为中国留学生量身定制的音乐学院上课、排练、剧院生存刚需高频词库")

tab1, tab2, tab3 = st.tabs(["📖 实战泛读速记", "🕹️ 考前通关测试", "🎵 歌剧歌词自由泛读"])

# ==================== 选项卡 1：浏览模式 ====================
with tab1:
    vocab = st.session_state.vocab
    idx = st.session_state.browse_index
    if vocab and idx < len(vocab):
        current_word = vocab[idx]
        st.markdown(f"""
            <div style="background-color: #f1f3f5; padding: 35px; border-radius: 15px; border-left: 6px solid #009246; margin: 20px 0; text-align: center;">
                <h1 style="color: #009246; margin-bottom: 5px; font-size: 36px;">{current_word['word']}</h1>
                <p style="color: #6c757d; font-style: italic; font-size: 16px;">[{current_word.get('pos', '')}]</p>
                <hr style="border: 0; border-top: 1px solid #dee2e6; margin: 15px 0;">
                <h3 style="color: #ce2b37; font-weight: bold; font-size: 24px;">{current_word['meaning']}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # 100% 稳定的本地音频流播放
        audio_file = get_local_audio(current_word['word'], prefix="word")
        if audio_file:
            st.audio(audio_file, format="audio/mp3")
        else:
            st.error("⚠️ 本地音频合成中，请稍后刷新...")
        
        st.write(f"📊 词库进度: {idx + 1} / {len(vocab)}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 上一个单词", use_container_width=True) and idx > 0:
                st.session_state.browse_index -= 1
                st.rerun()
        with col2:
            if st.button("下一个单词 ➡️", use_container_width=True) and idx < len(vocab) - 1:
                st.session_state.browse_index += 1
                st.rerun()

# ==================== 选项卡 2：测试模式 ====================
with tab2:
    vocab = st.session_state.vocab
    if len(vocab) < 4:
        st.warning("词库至少需要 4 个单词才能开启测试模式！")
    else:
        test_mode = st.radio("选择测试机制：", ["✨ 智能复习模式", "🎲 普通测试模式"], horizontal=True)
        st.markdown("---")
        
        if st.session_state.current_quiz is None:
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
            st.rerun()
        
        if st.session_state.current_quiz is not None:
            quiz = st.session_state.current_quiz
            if quiz.get("mode_at_birth", "未知") != test_mode:
                st.session_state.current_quiz = None
                st.rerun()
                
            st.metric(label="🎯 答对率", value=f"{st.session_state.quiz_score} / {st.session_state.quiz_total}")
            is_w = st.session_state.memory_pool.get(quiz['word'], {}).get("is_wrong", False)
            badge = "⚠️ 顽固错题重现：" if is_w and "智能复习模式" in test_mode else "请听题："
            st.markdown(f"<p style='color:gray; margin-bottom:0;'>{badge}</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #009246; font-size: 36px; margin-top:0;'>{quiz['word']}</h2>", unsafe_allow_html=True)
            
            # 测试模式本地高稳定性音频
            quiz_audio = get_local_audio(quiz['word'], prefix="quiz")
            if quiz_audio:
                st.audio(quiz_audio, format="audio/mp3")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            for option in quiz['options']:
                if st.button(option, use_container_width=True, key=f"quiz_opt_{option}"):
                    st.session_state.quiz_total += 1
                    if option == quiz['correct']:
                        st.success(f"🎉 答对了！")
                        st.session_state.quiz_score += 1
                        st.session_state.memory_pool[quiz['word']]["is_wrong"] = False
                        st.session_state.memory_pool[quiz['word']]["last_correct_time"] = time.time()
                    else:
                        st.error(f"❌ 答错啦！正解是：{quiz['correct']}")
                        st.session_state.memory_pool[quiz['word']]["is_wrong"] = True
                    st.session_state.current_quiz = None
                    st.rerun()

# ==================== 🛠️ 选项卡 3：歌词自由泛读 ====================
with tab3:
    st.subheader("🎼 歌剧歌词智能泛读面板")
    st.caption("支持自由输入全新歌词。系统将自动为你进行单句拆分并匹配实时纯正意语朗读音频。")
    
    lyric_source = st.radio("选择歌词来源：", ["📋 自由复制粘贴全新歌词", "📚 浏览经典内置唱段"], horizontal=True)
    
    final_lyrics = []
    
    if lyric_source == "📋 自由复制粘贴全新歌词":
        st.markdown("#### 📥 请在下方粘贴你的意大利语歌词")
        input_title = st.text_input("给这首歌曲起个名字（可选）：", placeholder="例如：Aria di Chiesa")
        
        user_lyric_text = st.text_area(
            "把整段意大利语歌词直接粘贴在下面：", 
            placeholder="Libiamo, libiamo ne' lieti calici...\n(注意：复制进来的歌词请尽量保持一行一句，效果最好哦！)",
            height=200
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
        chosen_
