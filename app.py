import streamlit as st
import random
import pandas as pd
import time

# 引入独立词库文件
try:
    from vocab_data import MEGA_VOCAB
except ImportError:
    MEGA_VOCAB = [{"word": "Caricamento...", "meaning": "词库加载中，请确保创建了 vocab_data.py", "pos": ""}]

st.set_page_config(page_title="意音圣经 · 声乐歌剧生存背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 核心数据与智能复习状态初始化 ---
if "vocab" not in st.session_state:
    st.session_state.vocab = MEGA_VOCAB

# 用于记录每个单词的记忆状态，格式为 { "单词": {"last_correct_time": 0, "is_wrong": False} }
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
            # 同步更新记忆池
            st.session_state.memory_pool = {item['word']: {"last_correct_time": 0, "is_wrong": False} for item in new_vocab}
            st.sidebar.success(f"成功导入 {len(new_vocab)} 个外部单词！")
        else:
            st.sidebar.error("CSV 文件必须包含 'word' 和 'meaning' 两列！")
    except Exception as e:
        st.sidebar.error(f"读取文件失败: {e}")

st.sidebar.info(f"✨ 实战圣经词库已加载：共 {len(st.session_state.vocab)} 个词条")

# 侧边栏复习进度看板
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

# ==================== 选项卡 2：测试模式（集成智能复习） ====================
with tab2:
    vocab = st.session_state.vocab
    if len(vocab) < 4:
        st.warning("词库至少需要 4 个单词才能开启测试模式！")
    else:
        # 允许用户选择普通测试还是智能复习
        test_mode = st.radio(
            "选择测试机制：",
            ["✨ 智能复习模式 (错题死磕 + 答对拉黑10天)", "🎲 普通测试模式 (全词库随机轰炸)"],
            horizontal=True
        )
        
        st.markdown("---")
        
        # 实时生成题目逻辑
        if st.session_state.current_quiz is None:
            current_time = time.time()
            ten_days_in_seconds = 10 * 24 * 60 * 60  # 10天的秒数
            
            # 根据模式筛选符合条件的候选词池
            if "智能复习模式" in test_mode:
                # 优先挑选答错的词
                wrong_pool = [item for item in vocab if st.session_state.memory_pool.get(item['word'], {}).get("is_wrong", False)]
                
                if wrong_pool:
                    # 如果有错题，死磕错题池
                    correct_item = random.choice(wrong_pool)
                else:
                    # 如果没错题，选择【没在10天内答对过】的词
                    review_pool = [
                        item for item in vocab 
                        if (current_time - st.session_state.memory_pool.get(item['word'], {}).get("last_correct_time", 0)) > ten_days_in_seconds
                    ]
                    if review_pool:
                        correct_item = random.choice(review_pool)
                    else:
                        correct_item = None
            else:
                # 普通模式：全量随机
                correct_item = random.choice(vocab)
            
            # 如果智能复习模式下，所有词都在10天冷却期且没有错题
            if correct_item is None:
                st.balloons()
                st.success("🥇 太强了！当前所有单词均已通关，且全部处于10日免修假期中！建议切换到普通模式或去休息。")
            else:
                # 混淆项生成（从整个大词库里抓取，确保有4个选项）
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
                    "mode_at_birth": test_mode # 记录生成这道题时的模式
                }
        
        # 渲染题目
        if st.session_state.current_quiz is not None:
            quiz = st.session_state.current_quiz
            
            # 如果用户在答题中途切了模式，强制清除当前题重刷，防止卡死
            if quiz["mode_at_birth"] != test_mode:
                st.session_state.current_quiz = None
                st.rerun()
                
            st.metric(label="🎯 答对率 (正确数/总尝试)", value=f"{st.session_state.quiz_score} / {st.session_state.quiz_total}")
            
            # 标记当前题目状态小标签
            is_w = st.session_state.memory_pool.get(quiz['word'], {}).get("is_wrong", False)
            badge = "⚠️ 顽固错题重现：" if is_w and "智能复习模式" in test_mode else "请听题："
            
            st.markdown(f"<p style='color:gray; margin-bottom:0;'>{badge}</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #009246; font-size: 34px; margin-top:0;'>{quiz['word']}</h2>", unsafe_allow_html=True)
            
            # 按钮交互
            for option in quiz['options']:
                if st.button(option, use_container_width=True, key=f"quiz_opt_{option}"):
                    st.session_state.quiz_total += 1
                    
                    if option == quiz['correct']:
                        st.session_state.quiz_score += 1
                        st.success(f"🎉 答对了！【{quiz['word']}】就是：{quiz['correct']}")
                        
                        # 【核心智能更新逻辑】答对了：解除错误标记，并记下当前的答对时间戳
                        st.session_state.memory_pool[quiz['word']]["is_wrong"] = False
                        st.session_state.memory_pool[quiz['word']]["last_correct_time"] = time.time()
                    else:
                        st.error(f"❌ 答错啦！【{quiz['word']}】的真正含义是：{quiz['correct']}")
                        
                        # 【核心智能更新逻辑】答错了：打上顽固错题标记
                        st.session_state.memory_pool[quiz['word']]["is_wrong"] = True
                    
                    st.session_state.current_quiz = None
                    st.rerun()
            
            if st.session_state.current_quiz is None:
                if st.button("进入下一题 ➡️", use_container_width=True):
                    st.rerun()
