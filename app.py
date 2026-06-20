import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="意语开心背词宝 🇮🇹", page_icon="🇮🇹", layout="centered")

# --- 注入你提供的超专业声乐/歌剧核心词库 ---
MUSIC_VOCAB = [
    # 一、排练指令
    {"word": "iniziare", "meaning": "开始", "pos": "v."},
    {"word": "da capo", "meaning": "从头开始 / 从头", "pos": "adv."},
    {"word": "dall'inizio", "meaning": "从开始处", "pos": "adv."},
    {"word": "riprendere", "meaning": "重新开始 / 继续", "pos": "v."},
    {"word": "ricominciare", "meaning": "重新开始", "pos": "v."},
    {"word": "continuare", "meaning": "继续", "pos": "v."},
    {"word": "fermarsi", "meaning": "停止", "pos": "v."},
    {"word": "stop", "meaning": "停止", "pos": "int."},
    {"word": "ancora", "meaning": "再 / 再次", "pos": "adv."},
    {"word": "ancora una volta", "meaning": "再来一次", "pos": "phrase"},
    {"word": "un'altra volta", "meaning": "另一次 / 再一次", "pos": "phrase"},
    {"word": "ripetere", "meaning": "重复", "pos": "v."},
    {"word": "attenzione", "meaning": "注意", "pos": "n."},
    {"word": "ascoltare", "meaning": "听", "pos": "v."},
    {"word": "guardare", "meaning": "看", "pos": "v."},
    {"word": "seguire", "meaning": "跟随", "pos": "v."},
    {"word": "osservare", "meaning": "观察 / 看", "pos": "v."},
    {"word": "lento", "meaning": "慢", "pos": "adj."},
    {"word": "veloce", "meaning": "快", "pos": "adj."},
    {"word": "accelerare", "meaning": "加速", "pos": "v."},
    {"word": "accelerando", "meaning": "渐快 (加速中)", "pos": "adv."},
    {"word": "rallentare", "meaning": "减速 / 渐慢", "pos": "v."},
    {"word": "ritardando", "meaning": "渐慢", "pos": "adv."},
    {"word": "ritardare", "meaning": "延迟 / 减速", "pos": "v."},
    {"word": "mantenere", "meaning": "保持", "pos": "v."},
    {"word": "a tempo", "meaning": "恢复原速 / 保持速度", "pos": "phrase"},
    {"word": "tempo", "meaning": "节奏 / 拍子 / 速度", "pos": "n."},
    {"word": "battito", "meaning": "拍子 / 强拍", "pos": "n."},
    {"word": "pulsazione", "meaning": "脉动 / 拍子", "pos": "n."},
    {"word": "levare", "meaning": "弱拍 / 弱起", "pos": "n."},
    {"word": "battere", "meaning": "强拍 / 打拍", "pos": "n."},
    {"word": "sincronia", "meaning": "同步 / 一致", "pos": "n."},
    {"word": "piano", "meaning": "弱 / 轻", "pos": "adj./adv."},
    {"word": "pianissimo", "meaning": "极弱", "pos": "adj./adv."},
    {"word": "forte", "meaning": "强 / 响亮", "pos": "adj./adv."},
    {"word": "fortissimo", "meaning": "极强", "pos": "adj./adv."},
    {"word": "crescendo", "meaning": "渐强", "pos": "adv."},
    {"word": "diminuendo", "meaning": "渐弱", "pos": "adv."},
    {"word": "mezzoforte", "meaning": "中强", "pos": "adj./adv."},
    {"word": "legato", "meaning": "连音 / 连奏", "pos": "adj./adv."},
    {"word": "staccato", "meaning": "断音 / 断奏", "pos": "adj./adv."},
    {"word": "marcato", "meaning": "强调 / 加重", "pos": "adj./adv."},
    {"word": "sostenuto", "meaning": "持续的", "pos": "adj./adv."},
    {"word": "espressivo", "meaning": "有表现力的", "pos": "adj."},
    {"word": "con espressione", "meaning": "富有表情地", "pos": "phrase"},
    {"word": "cantabile", "meaning": "如歌地", "pos": "adj./adv."},
    {"word": "più forte", "meaning": "更响 / 更强", "pos": "phrase"},
    {"word": "più piano", "meaning": "更轻 / 更弱", "pos": "phrase"},
    {"word": "dal segno", "meaning": "从记号处反复", "pos": "phrase"},
    {"word": "prova", "meaning": "排练 / 考试", "pos": "n."},
    {"word": "prova generale", "meaning": "总排练 / 彩排", "pos": "n."},
    {"word": "marcare", "meaning": "标记 (轻声唱)", "pos": "v."},
    {"word": "mezza voce", "meaning": "半声 / 轻声", "pos": "n."},
    {"word": "insieme", "meaning": "一起", "pos": "adv."},
    {"word": "all'unisono", "meaning": "齐唱 / 齐奏 / 同步", "pos": "phrase"},

    # 二、乐谱与音乐理论
    {"word": "spartito", "meaning": "乐谱 (通常指单谱/声乐谱)", "pos": "n."},
    {"word": "partitura", "meaning": "总谱", "pos": "n."},
    {"word": "parte", "meaning": "部分 / 声部", "pos": "n."},
    {"word": "pagina", "meaning": "页", "pos": "n."},
    {"word": "riga", "meaning": "行", "pos": "n."},
    {"word": "sistema", "meaning": "系统 / 大谱表", "pos": "n."},
    {"word": "battuta", "meaning": "小节 / 拍子", "pos": "n."},
    {"word": "misura", "meaning": "小节 / 测量", "pos": "n."},
    {"word": "sezione", "meaning": "段落 / 部分", "pos": "n."},
    {"word": "frase", "meaning": "乐句", "pos": "n."},
    {"word": "periodo", "meaning": "乐段", "pos": "n."},
    {"word": "introduzione", "meaning": "引子 / 前奏", "pos": "n."},
    {"word": "coda", "meaning": "尾声", "pos": "n."},
    {"word": "finale", "meaning": "终曲 / 尾声", "pos": "n."},
    {"word": "nota", "meaning": "音符", "pos": "n."},
    {"word": "altezza", "meaning": "音高", "pos": "n."},
    {"word": "intervallo", "meaning": "音程", "pos": "n."},
    {"word": "scala", "meaning": "音阶", "pos": "n."},
    {"word": "semitono", "meaning": "半音", "pos": "n."},
    {"word": "tono", "meaning": "全音 / 音调", "pos": "n."},
    {"word": "accordo", "meaning": "和弦", "pos": "n."},
    {"word": "tonalità", "meaning": "调性", "pos": "n."},
    {"word": "tonica", "meaning": "主音 / 主和弦", "pos": "n."},
    {"word": "dominante", "meaning": "属音 / 属和弦", "pos": "n."},
    {"word": "modulazione", "meaning": "转调", "pos": "n."},
    {"word": "cadenza", "meaning": "终止 / 华彩段", "pos": "n."},
    {"word": "metro", "meaning": "节拍", "pos": "n."},
    {"word": "ritmo", "meaning": "节奏", "pos": "n."},
    {"word": "tempo composto", "meaning": "复拍子", "pos": "n."},
    {"word": "tempo semplice", "meaning": "单拍子", "pos": "n."},
    {"word": "forma", "meaning": "曲式 / 形式", "pos": "n."},
    {"word": "tema", "meaning": "主题", "pos": "n."},
    {"word": "variazione", "meaning": "变奏", "pos": "n."},
    {"word": "sviluppo", "meaning": "发展 / 展开部", "pos": "n."},
    {"word": "ripresa", "meaning": "再现部 / 重复", "pos": "n."},
    {"word": "recitativo", "meaning": "宣叙调", "pos": "n."},
    {"word": "recitativo secco", "meaning": "清宣叙调", "pos": "n."},
    {"word": "recitativo accompagnato", "meaning": "伴奏宣叙调", "pos": "n."},
    {"word": "arioso", "meaning": "咏叹调风格 / 咏叙调", "pos": "n./adj."},
    {"word": "riduzione per canto e pianoforte", "meaning": "钢琴伴奏谱 / 简化谱", "pos": "phrase"},
    {"word": "partitura d'orchestra", "meaning": "乐队总谱", "pos": "phrase"},

    # 三、声乐技术
    {"word": "respiro", "meaning": "呼吸", "pos": "n."},
    {"word": "fiato", "meaning": "气息", "pos": "n."},
    {"word": "inspirazione", "meaning": "吸气", "pos": "n."},
    {"word": "espirazione", "meaning": "呼气", "pos": "n."},
    {"word": "sostegno", "meaning": "支持", "pos": "n."},
    {"word": "appoggio", "meaning": "支点 / 气息支持", "pos": "n."},
    {"word": "diaframma", "meaning": "横膈膜", "pos": "n."},
    {"word": "voce", "meaning": "声音 / 声部", "pos": "n."},
    {"word": "emissione", "meaning": "发声 / 放出", "pos": "n."},
    {"word": "fonazione", "meaning": "发音 / 发声动作", "pos": "n."},
    {"word": "attacco", "meaning": "起音 / 攻击", "pos": "n."},
    {"word": "vibrato", "meaning": "颤音 / 揉弦", "pos": "n."},
    {"word": "risonanza", "meaning": "共鸣", "pos": "n."},
    {"word": "maschera", "meaning": "面罩共鸣 / 面具", "pos": "n."},
    {"word": "cavità orale", "meaning": "口腔", "pos": "n."},
    {"word": "cavità nasale", "meaning": "鼻腔", "pos": "n."},
    {"word": "chiaroscuro", "meaning": "明暗对比 / 共鸣平衡", "pos": "n."},
    {"word": "registro", "meaning": "声区 / 登记", "pos": "n."},
    {"word": "registro di petto", "meaning": "胸声区", "pos": "n."},
    {"word": "registro di testa", "meaning": "头声区", "pos": "n."},
    {"word": "registro misto", "meaning": "混声区", "pos": "n."},
    {"word": "passaggio", "meaning": "换声区 / 乐段", "pos": "n."},
    {"word": "timbro", "meaning": "音色", "pos": "n."},
    {"word": "colore", "meaning": "颜色 / 音色特点", "pos": "n."},
    {"word": "brillante", "meaning": "明亮的 / 辉煌的", "pos": "adj."},
    {"word": "scuro", "meaning": "暗的 / 深沉的", "pos": "adj."},
    {"word": "chiaro", "meaning": "明亮的 / 清晰的", "pos": "adj."},
    {"word": "squillo", "meaning": "穿透力 / 金属般亮光", "pos": "n."},
    {"word": "vocale", "meaning": "元音", "pos": "n."},
    {"word": "consonante", "meaning": "辅音", "pos": "n."},
    {"word": "dizione", "meaning": "吐字 / 咬字", "pos": "n."},
    {"word": "articolazione", "meaning": "发音器官动作", "pos": "n."},
    {"word": "pronuncia", "meaning": "发音 / 读音", "pos": "n."},
    {"word": "intonazione", "meaning": "音准", "pos": "n."},
    {"word": "calante", "meaning": "偏低的 (音准)", "pos": "adj."},
    {"word": "crescente", "meaning": "偏高的 (音准)", "pos": "adj."},
    {"word": "stonato", "meaning": "跑调的 / 不准的", "pos": "adj."},
    {"word": "intonato", "meaning": "音准正确的", "pos": "adj."},
    {"word": "aprire", "meaning": "打开 (如打开喉咙)", "pos": "v."},
    {"word": "chiudere", "meaning": "关闭", "pos": "v."},
    {"word": "coprire", "meaning": "遮盖 (声音掩盖技术)", "pos": "v."},
    {"word": "sostenere", "meaning": "支持 / 保持", "pos": "v."},
    {"word": "rilassare", "meaning": "放松", "pos": "v."},
    {"word": "postura", "meaning": "姿态 / 体态", "pos": "n."},
    {"word": "messa di voce", "meaning": "渐强渐弱发声法", "pos": "phrase"},
    {"word": "portamento", "meaning": "滑音", "pos": "n."},
    {"word": "copertura", "meaning": "声音遮盖", "pos": "n."},
    {"word": "filato", "meaning": "延长音 / 弱拉长音", "pos": "n."},
    {"word": "impostazione", "meaning": "发声位置 / 安放", "pos": "n."},
    {"word": "proiezione", "meaning": "声音穿透力 / 投射", "pos": "n."},
    {"word": "trillo", "meaning": "颤音", "pos": "n."},
    {"word": "fioritura", "meaning": "装饰音 / 花腔", "pos": "n."},
    {"word": "coloratura", "meaning": "花腔声乐技巧", "pos": "n."},

    # 四、歌剧与舞台
    {"word": "palcoscenico", "meaning": "舞台", "pos": "n."},
    {"word": "quinta", "meaning": "侧幕 / 舞台侧翼", "pos": "n."},
    {"word": "sipario", "meaning": "舞台大幕", "pos": "n."},
    {"word": "scena", "meaning": "场景 / 场", "pos": "n."},
    {"word": "fondale", "meaning": "背景幕 / 舞台深处", "pos": "n."},
    {"word": "destra", "meaning": "右边", "pos": "n./adj."},
    {"word": "sinistra", "meaning": "左边", "pos": "n./adj."},
    {"word": "centro", "meaning": "中心", "pos": "n."},
    {"word": "avanti", "meaning": "向前 / 舞台前方", "pos": "adv."},
    {"word": "indietro", "meaning": "向后 / 舞台后方", "pos": "adv."},
    {"word": "entrare", "meaning": "上场 / 进入", "pos": "v."},
    {"word": "uscire", "meaning": "下场 / 出去", "pos": "v."},
    {"word": "camminare", "meaning": "走", "pos": "v."},
    {"word": "sedersi", "meaning": "坐下", "pos": "v."},
    {"word": "alzarsi", "meaning": "站起来", "pos": "v."},
    {"word": "girarsi", "meaning": "转身", "pos": "v."},
    {"word": "regista", "meaning": "导演", "pos": "n."},
    {"word": "direttore", "meaning": "指挥 / 负责人", "pos": "n."},
    {"word": "maestro collaboratore", "meaning": "合作导师 / 艺术指导", "pos": "n."},
    {"word": "pianista repetiteur", "meaning": "排练钢琴伴奏", "pos": "n."},
    {"word": "scenografo", "meaning": "舞台布景师", "pos": "n."},
    {"word": "costumista", "meaning": "服装设计师", "pos": "n."},
    {"word": "direttore di scena", "meaning": "舞台监督", "pos": "n."},
    {"word": "luce", "meaning": "灯光", "pos": "n."},
    {"word": "riflettore", "meaning": "追光灯 / 聚光灯", "pos": "n."},
    {"word": "oscurità", "meaning": "黑暗", "pos": "n."},
    {"word": "illuminazione", "meaning": "照明", "pos": "n."},
    {"word": "soprano", "meaning": "女高音", "pos": "n."},
    {"word": "tenore", "meaning": "男高音", "pos": "n."},
    {"word": "baritono", "meaning": "男中音", "pos": "n."},
    {"word": "mezzosoprano", "meaning": "女中音", "pos": "n."},
    {"word": "basso", "meaning": "男低音", "pos": "n."},
    {"word": "fach", "meaning": "声部细分类型 (德语借词常用)", "pos": "n."},
    {"word": "prova all'italiana", "meaning": "坐排 (不带动作只唱)", "pos": "n."},
    {"word": "prova di regia", "meaning": "导演排练 / 戏剧排练", "pos": "n."},
    {"word": "trucco", "meaning": "化妆", "pos": "n."},
    {"word": "parrucco", "meaning": "假发 / 发型", "pos": "n."},
    {"word": "costume", "meaning": "戏服 / 服装", "pos": "n."},
    {"word": "scenografia", "meaning": "舞台布景", "pos": "n."},
    {"word": "atto", "meaning": "幕", "pos": "n."},
    {"word": "applauso", "meaning": "掌声", "pos": "n."},
    {"word": "inchino", "meaning": "谢幕 / 鞠躬", "pos": "n."},
    {"word": "suggeritore", "meaning": "舞台提示员", "pos": "n."},

    # 五、声乐曲目
    {"word": "aria", "meaning": "咏叹调", "pos": "n."},
    {"word": "romanza", "meaning": "浪漫曲", "pos": "n."},
    {"word": "duetto", "meaning": "二重唱", "pos": "n."},
    {"word": "terzetto", "meaning": "三重唱", "pos": "n."},
    {"word": "coro", "meaning": "合唱", "pos": "n."},
    {"word": "ouverture", "meaning": "序曲", "pos": "n."},
    {"word": "cabaletta", "meaning": "卡巴列塔 (快板咏叹调)", "pos": "n."},
    {"word": "stretta", "meaning": "紧板尾声", "pos": "n."},
    {"word": "lied", "meaning": "艺术歌曲 (德语常用)", "pos": "n."},
    {"word": "mélodie", "meaning": "艺术歌曲 (法语常用)", "pos": "n."},
    {"word": "canzone", "meaning": "歌曲 / 歌", "pos": "n."},
    {"word": "barocco", "meaning": "巴洛克风格", "pos": "adj./n."},
    {"word": "classico", "meaning": "古典风格", "pos": "adj./n."},
    {"word": "romantico", "meaning": "浪漫风格", "pos": "adj./n."},
    {"word": "verista", "meaning": "真实主义风格的", "pos": "adj./n."},
    {"word": "contemporaneo", "meaning": "现代 / 当代的", "pos": "adj."},
    {"word": "bel canto", "meaning": "美声唱法", "pos": "n."},
    {"word": "opera buffa", "meaning": "喜歌剧", "pos": "n."},
    {"word": "opera seria", "meaning": "正歌剧", "pos": "n."},
    {"word": "verismo", "meaning": "真实主义", "pos": "n."},

    # 六、音乐学院行政
    {"word": "iscrizione", "meaning": "注册 / 报名", "pos": "n."},
    {"word": "immatricolazione", "meaning": "正式入学注册", "pos": "n."},
    {"word": "ammissione", "meaning": "录取 / 准入", "pos": "n."},
    {"word": "audizione", "meaning": "面试 / 听音试唱", "pos": "n."},
    {"word": "diploma", "meaning": "文凭 / 毕业证书", "pos": "n."},
    {"word": "corso", "meaning": "课程", "pos": "n."},
    {"word": "lezione", "meaning": "课 / 讲课", "pos": "n."},
    {"word": "seminario", "meaning": "研讨课", "pos": "n."},
    {"word": "laboratorio", "meaning": "工作坊 / 实验室", "pos": "n."},
    {"word": "masterclass", "meaning": "大师班", "pos": "n."},
    {"word": "esame", "meaning": "考试", "pos": "n."},
    {"word": "valutazione", "meaning": "评分 / 评估", "pos": "n."},
    {"word": "commissione", "meaning": "评委会 / 委员会", "pos": "n."},
    {"word": "modulo", "meaning": "表格", "pos": "n."},
    {"word": "domanda", "meaning": "申请书 / 问题", "pos": "n."},
    {"word": "certificato", "meaning": "证书 / 证明", "pos": "n."},
    {"word": "documento", "meaning": "文件", "pos": "n."},
    {"word": "credito", "meaning": "学分", "pos": "n."},
    {"word": "frequenza", "meaning": "出勤率", "pos": "n."},
    {"word": "obbligatorio", "meaning": "必修的", "pos": "adj."},
    {"word": "facoltativo", "meaning": "选修的", "pos": "adj."},
    {"word": "tesi", "meaning": "毕业论文", "pos": "n."},
    {"word": "dissertazione", "meaning": "学术论文", "pos": "n."},
    {"word": "ricerca", "meaning": "研究", "pos": "n."},
    {"word": "concorso", "meaning": "比赛", "pos": "n."},
    {"word": "borsa di studio", "meaning": "奖学金", "pos": "n."},
    {"word": "biblioteca", "meaning": "图书馆", "pos": "n."},
    {"word": "prestito", "meaning": "借阅 / 贷款", "pos": "n."},
    {"word": "catalogo", "meaning": "目录", "pos": "n."},

    # 七、音乐史与分析课
    {"word": "compositore", "meaning": "作曲家", "pos": "n."},
    {"word": "repertorio", "meaning": "保留剧目 / 曲目库", "pos": "n."},
    {"word": "stile", "meaning": "风格", "pos": "n."},
    {"word": "analisi", "meaning": "分析", "pos": "n."},
    {"word": "struttura", "meaning": "结构", "pos": "n."},
    {"word": "armonia", "meaning": "和声", "pos": "n."},
    {"word": "melodia", "meaning": "旋律", "pos": "n."},
    {"word": "contrappunto", "meaning": "对位法", "pos": "n."},
    {"word": "Medioevo", "meaning": "中世纪", "pos": "n."},
    {"word": "Rinascimento", "meaning": "文艺复兴", "pos": "n."},
    {"word": "Barocco", "meaning": "巴洛克时期", "pos": "n."},
    {"word": "Classicismo", "meaning": "古典主义时期", "pos": "n."},
    {"word": "Romanticismo", "meaning": "浪漫主义时期", "pos": "n."},
    {"word": "Novecento", "meaning": "20世纪", "pos": "n."},
    {"word": "sviluppo tematico", "meaning": "主题发展", "pos": "phrase"},
    {"word": "orchestrazione", "meaning": "配器法", "pos": "n."}
]

if "vocab" not in st.session_state:
    st.session_state.vocab = MUSIC_VOCAB
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

st.title("🇮🇹 声乐意语开心背词宝")
st.caption("专为声乐/歌剧专业定制的傻瓜式高频词汇通关利器")

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
