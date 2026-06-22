# (此处代码结构保持不变，仅更新第 4 个 Tab 的逻辑)

# ==================== 🗂️ 选项卡 4：核心单词总表（含分类诊断器） ====================
with tab4:
    st.subheader("🗂️ 核心单词总表面板")
    
    vocab_list = st.session_state.vocab
    categories = {
        "🎵 音乐基础词汇": [],
        "🏫 上课常用词汇": [],
        "🎭 排练演出词汇": [],
        "🌍 其他高频生存词": []
    }
    
    for item in vocab_list:
        meaning = str(item.get('meaning', ''))
        tag = str(item.get('pos', ''))
        
        # 宽泛化雷达逻辑
        if any(k in meaning + tag for k in ["谱", "音", "唱", "声", "调", "节奏", "拍", "旋律", "小节", "音阶", "力度"]):
            categories["🎵 音乐基础词汇"].append(item)
        elif any(k in meaning + tag for k in ["重复", "开始", "停", "再", "听", "看", "读", "写", "错", "对", "明白", "知道", "问", "回答", "从", "到", "解释"]):
            categories["🏫 上课常用词汇"].append(item)
        elif any(k in meaning + tag for k in ["台", "幕", "剧", "演", "排练", "服装", "走位", "位置", "动作", "灯光", "指示", "角色", "乐队"]):
            categories["🎭 排练演出词汇"].append(item)
        else:
            categories["🌍 其他高频生存词"].append(item)

    # 诊断器：显示分类统计
    st.info(f"📊 词库分布诊断：基础({len(categories['🎵 音乐基础词汇'])}) | 上课({len(categories['🏫 上课常用词汇'])}) | 排练({len(categories['🎭 排练演出词汇'])}) | 其他({len(categories['🌍 其他高频生存词'])})")
    
    selected_cat = st.radio("👇 请选择生存场景：", options=list(categories.keys()), horizontal=True)
    st.divider()
    
    target_words = categories[selected_cat]
    st.markdown(f"### 当前：{selected_cat} *({len(target_words)} 个词)*")
    
    for word_idx, word_item in enumerate(target_words):
        with st.expander(f"🇮🇹 {word_item['word']}"):
            st.write(f"**中文含义**：{word_item['meaning']}")
            st.write(f"**原始标签**：{word_item.get('pos', '无')}")
            # ... (后续播放音频逻辑)
