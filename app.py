import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="意语开心背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

DEFAULT_VOCAB = [
    {"word": "Ciao", "meaning": "你好 / 再见", "pos": "int."},
    {"word": "Grazie", "meaning": "谢谢", "pos": "int."},
    {"word": "Buongiorno", "meaning": "早上好", "pos": "int."},
    {"word": "Prego", "meaning": "不用谢 / 请", "pos": "int."},
    {"word": "Amico", "meaning": "朋友", "pos": "n."},
    {"word": "Casa", "meaning": "家 / 房子", "pos": "n."},
    {"word": "Mangiare", "meaning": "吃", "pos": "v."},
    {"word": "Amore", "meaning": "爱", "pos": "n."},
    {"word": "Bello", "meaning": "漂亮的 / 美好的", "pos": "adj."},
    {"word": "Acqua", "meaning": "水", "pos": "n."}
]

if "vocab" not in st.session_state:
    st.session_state.vocab = DEFAULT_VOCAB
if "browse_index" not in st.session_state:
    st.session_state.browse_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

st.sidebar.title("🎒 词库管理")
uploaded_file = st.sidebar.file_uploader("导入自定义 CSV 词库", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "word" in df.columns and "meaning" in df.columns:
            if "pos" not in df.columns:
                df["pos"] = ""
            st.session_state.vocab = df.to_dict(orient="records")
            st.sidebar.success(f"成功导入 {len(st.session_state.vocab)} 个单词！")
        else:
            st.sidebar.error("CSV 文件必须包含 'word' 和 'meaning' 两列！")
    except Exception as e:
        st.sidebar.error(f"读取文件失败: {e}")

st.sidebar.info(f"当前词库共 {len(st.session_state.vocab)} 个单词")

st.title("🇮🇹 意语开心背词宝")
st.caption("傻瓜式快速泛读与闯关测试，助你轻松掌握意大利语")

tab1, tab2 = st.tabs(["📖 泛读模式", "🕹️ 闯关测试"])

with tab1:
    vocab = st.session_state.vocab
    idx = st.session_state.browse_index
    
    if vocab:
        current_word = vocab[idx]
        st.markdown(
            f"""
            <div style="background-color: #f8f9fa; padding: 30px; border-radius: 15px; border-left: 5px solid #28a745; margin: 20px 0; text-align: center;">
                <h1 style="color: #28a745; margin-bottom: 5px;">{current_word['word']}</h1>
                <p style="color: #6c757d; font-style: italic;">[{current_word.get('pos', '')}]</p>
                <h3 style="color: #343a40; font-weight: normal;">{current_word['meaning']}</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.write(f"进度: {idx + 1} / {len(vocab)}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 上一个", use_container_width=True) and idx > 0:
                st.session_state.browse_index -= 1
                st.rerun()
        with col2:
            if st.button("下一个 ➡️", use_container_width=True) and idx < len(vocab) - 1:
                st.session_state.browse_index += 1
                st.rerun()
    else:
        st.warning("暂无词库，请在侧边栏导入。")

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
        st.metric(label="当前得分 (答对/总数)", value=f"{st.session_state.quiz_score} / {st.session_state.quiz_total}")
        st.markdown(f"<h2 style='text-align: center; color: #dc3545;'>{quiz['word']}</h2>", unsafe_allow_html=True)
        st.write("请选择正确的中文含义：")
        
        for option in quiz['options']:
            if st.button(option, use_container_width=True, key=f"btn_{option}"):
                st.session_state.quiz_total += 1
                if option == quiz['correct']:
                    st.session_state.quiz_score += 1
                    st.success(f"🎉 答对了！ {quiz['word']} 的意思就是：{quiz['correct']}")
                else:
                    st.error(f"❌ 答错了！ {quiz['word']} 的正确意思是：{quiz['correct']}")
                st.session_state.current_quiz = None
                st.button("进入下一题 ➡️")
