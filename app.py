import streamlit as st
import random
import pandas as pd

# 引入我们刚才创建的独立词库
try:
    from vocab_data import MEGA_VOCAB
except ImportError:
    MEGA_VOCAB = [{"word": "Caricamento...", "meaning": "词库加载中，请确保创建了 vocab_data.py", "pos": ""}]

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 核心数据初始化 ---
if "vocab" not in st.session_state:
    st.session_state.vocab = MEGA_VOCAB
if "browse_index" not in st.session_state:
    st.session_state.browse_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

st.sidebar.title("🎒 词库控制面板")
uploaded_file = st.sidebar.file_uploader("导入外部额外词库 (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "word" in df.columns and "meaning" in df.columns:
            if "pos" not in df.columns:
                df["pos"] = ""
            st.session_state.vocab = df.to_dict(orient="records")
            st.sidebar.success(f"成功导入 {len(st.session_state.vocab)} 个外部单词！")
        else:
            st.sidebar.error("CSV 文件必须包含 'word' 和 'meaning' 两列！")
    except Exception as e:
        st.sidebar.error(f"读取文件失败: {e}")

st.sidebar.info(f"✨ 实战圣经词库已加载：共 {len(st.session_state.vocab)} 个词条")

st.title("🇮🇹 意音圣经 · 声乐歌剧背词宝")
st.caption("为中国留学生量身定制的音乐学院上课、排练、剧院生存刚需高频词库")

tab1, tab2 = st.tabs(["📖 实战泛读速记", "🕹️ 考前通关测试"])

# 选项卡 1：浏览模式
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

# 选项卡 2：测试模式
with tab2:
    vocab = st.session_state.vocab
    if len(vocab) < 4:
        st.warning("词库至少需要 4 个单词才能开启测试模式！")
    else:
        if st.session_state.current_quiz is None:
            correct_item = random.choice(vocab)
            options = [correct_item['meaning']]
            while len(options) < 4:
                wrong_opt = random.choice(vocab)['meaning']
                if wrong_opt not in options:
                    options.append(wrong_opt)
            random.shuffle(options)
            
            st.session_state.current_quiz = {
                "word": correct_item['word'],
                "correct": correct_item['meaning'],
                "options": options
            }
        
        quiz = st.session_state.current_quiz
        st.metric(label="🎯 答对率 (正确数/总尝试)", value=f"{st.session_state.quiz_score} / {st.session_state.quiz_total}")
        st.markdown(f"<h2 style='text-align: center; color: #009246; font-size: 34px;'>{quiz['word']}</h2>", unsafe_allow_html=True)
        st.write("请选出符合该场景的正确中文释义：")
        
        for option in quiz['options']:
            if st.button(option, use_container_width=True, key=f"quiz_opt_{option}"):
                st.session_state.quiz_total += 1
                if option == quiz['correct']:
                    st.session_state.quiz_score += 1
                    st.success(f"🎉 太准了！老师正是在说：{quiz['correct']}")
                else:
                    st.error(f"❌ 意会错了！【{quiz['word']}】的真正含义是：{quiz['correct']}")
                st.session_state.current_quiz = None
                st.rerun()
        
        if st.session_state.current_quiz is None:
            if st.button("进入下一题 ➡️", use_container_width=True):
                st.rerun()
