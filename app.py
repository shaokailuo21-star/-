import streamlit as st
import random
import pandas as pd
import time
import urllib.parse

# 引入独立词库文件
try:
    from vocab_data import MEGA_VOCAB
except ImportError:
    MEGA_VOCAB = [{"word": "Caricamento...", "meaning": "词库加载中，请确保创建了 vocab_data.py", "pos": ""}]

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 🚀 谷歌翻译官方 TTS 发音核心函数 ---
def play_google_tts(text, lang="it"):
    """直接调用谷歌翻译官方接口，获取 100% 纯正的意大利语/中文语音流"""
    encoded_text = urllib.parse.quote(text)
    # 构造谷歌官方翻译的发音 URL
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={encoded_text}"
    
    # 使用 streamlit 的 audio 组件静默或直接播放，带有 html5 autoplay 属性
    audio_html = f"""
    <audio autoplay style="display:none;">
        <source src="{tts_url}" type="audio/mp3">
    </audio>
    """
    st.components.v1.html(audio_html, height=0, width=0)

# --- 核心数据与智能复习状态初始化 ---
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
if "tts_trigger" not in st.session_state:
    st.session_state.tts_trigger = None

# 处理全局发音队列 (改用谷歌服务)
if st.session_state.tts_trigger:
    text, lang = st.session_state.tts_trigger
    play_google_tts(text, lang)
    st.session_state.tts_trigger = None # 消费完立即清空

# --- 侧边栏及外部导入 ---
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
        else:
            st.sidebar.error("CSV 文件必须包含 'word' 和 'meaning' 两列！")
    except Exception as e:
        st.sidebar.error(f"读取文件失败: {e}")

st.sidebar.info(f"✨ 实战圣经词库已加载：共 {len(st.session_state.vocab)} 个词条")

wrong_count = sum(1 for v in st.session_state.memory_pool.values() if v["is_wrong"])
st.sidebar.metric(label="🔴 当前顽固错题数", value=f"{wrong_count} 题")

st.title("🇮🇹 意音圣经 · 声乐歌剧背词宝")
st.caption("为中国留学生量身定制的音乐学院上课、排练、剧院生存刚需高频词库")

tab1, tab2 = st.tabs(["📖 实战泛读速记", "🕹️ 考前通关测试"])

# ==================== 选项卡 1：浏览模式 ====================
with tab1:
    vocab = st.session_state.vocab
    idx = st.session_state.browse_index
    
    if vocab:
        current_word = vocab[idx]
        st.markdown(
            f"""
            <div style="background-color: #f1f3f5; padding: 35px; border-radius: 15px; border-left: 6px solid #009246; margin: 20px 0; text-align: center;">
                <h1 style="color: #009246; margin-bottom: 5px; font-size: 36px;">{current_word['word']}</h1>
                <p style="color: #6c757d; font-style: italic; font-size: 16px;">[{current_word.get('pos', '')}]</p>
                <hr style="border: 0; border-top: 1px solid #dee2e6; margin: 15px 0;">
                <h3 style="color: #ce2b37; font-weight: bold; font-size: 24px;">{current_word['meaning']}</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # 朗读控制行
        c_audio1, c_audio2 = st.columns(2)
        with c_audio1:
            if st.button("🔊 播放意大利语发音", use_container_width=True, key="tts_it"):
                st.session_state.tts_trigger = (current_word['word'], "it")
                st.rerun()
        with c_audio2:
            if st.button("🗣️ 播放中文释义", use_container_width=True, key="tts_zh"):
                st.session_state.tts_trigger = (current_word['meaning'], "zh")
                st.rerun()
                
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
        test_mode = st.radio(
            "选择测试机制：",
            ["✨ 智能复习模式 (错题死磕 + 答对拉黑10天)", "🎲 普通测试模式 (全词库随机轰炸)"],
            horizontal=True
        )
        
        st.markdown("---")
        
        if st.session_state.current_quiz is None:
            current_time = time.time()
            ten_days_in_seconds = 10 * 24 * 60 * 60
            
            if "智能复习模式" in test_mode:
                wrong_pool = [item for item in vocab if st.session_state.memory_pool.get(item['word'], {}).get("is_wrong", False)]
                if wrong_pool:
                    correct_item = random.choice(wrong_pool)
                else:
                    review_pool = [
                        item for item in vocab 
                        if (current_time - st.session_state.memory_pool.get(item['word'], {}).get("last_correct_time", 0)) > ten_days_in_seconds
                    ]
                    if review_pool:
                        correct_item = random.choice(review_pool)
                    else:
                        correct_item = None
            else:
                correct_item = random.choice(vocab)
            
            if correct_item is None:
                st.balloons()
                st.success("🥇 太强了！当前所有单词均已通关，且全部处于10日免修假期中！")
            else:
                options = [correct_item['meaning']]
                while len(options) < 4:
                    wrong_opt = random.choice(vocab)['meaning']
                    if wrong_opt not in options:
                        options.append(wrong_opt)
                random.shuffle(options)
                
                st.session_state.current_quiz = {
                    "word": correct_item['word'],
                    "correct": correct_item['meaning'],
                    "options": options,
                    "mode_at_birth": test_mode
                }
                # 出题时自动用意大利语朗读一次单词 (改用谷歌服务)
                st.session_state.tts_trigger = (correct_item['word'], "it")
                st.rerun()
        
        if st.session_state.current_quiz is not None:
            quiz = st.session_state.current_quiz
            
            if quiz.get("mode_at_birth", None) != test_mode:
                st.session_state.current_quiz = None
                st.rerun()
                
            st.metric(label="🎯 答对率 (正确数/总尝试)", value=f"{st.session_state.quiz_score} / {st.session_state.quiz_total}")
            
            is_w = st.session_state.memory_pool.get(quiz['word'], {}).get("is_wrong", False)
            badge = "⚠️ 顽固错题重现：" if is_w and "智能复习模式" in test_mode else "请听题："
            
            st.markdown(f"<p style='color:gray; margin-bottom:0;'>{badge}</p>", unsafe_allow_html=True)
            
            col_word, col_audio = st.columns([5, 1])
            with col_word:
                st.markdown(f"<h2 style='color: #009246; margin-top:0;'>{quiz['word']}</h2>", unsafe_allow_html=True)
            with col_audio:
                if st.button("📢 听音", use_container_width=True):
                    st.session_state.tts_trigger = (quiz['word'], "it")
                    st.rerun()
            
            # 选项按钮
            for option in quiz['options']:
                if st.button(option, use_container_width=True, key=f"quiz_opt_{option}"):
                    st.session_state.quiz_total += 1
                    
                    if option == quiz['correct']:
                        st.session_state.quiz_score += 1
                        st.success(f"🎉 答对了！【{quiz['word']}】就是：{quiz['correct']}")
                        st.session_state.memory_pool[quiz['word']]["is_wrong"] = False
                        st.session_state.memory_pool[quiz['word']]["last_correct_time"] = time.time()
                    else:
                        st.error(f"❌ 答错啦！【{quiz['word']}】的真正含义是：{quiz['correct']}")
                        st.session_state.memory_pool[quiz['word']]["is_wrong"] = True
                    
                    st.session_state.current_quiz = None
                    st.rerun()
            
            if st.session_state.current_quiz is None:
                if st.button("进入下一题 ➡️", use_container_width=True):
                    st.rerun()
