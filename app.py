import os
import io
from pathlib import Path
import streamlit as st
from PIL import Image

# =====================================================================
# 0. APP 基本設定 (全白清爽介面)
# =====================================================================

APP_NAME = "黑金剛 AI 商業自動化總控台 PRO"
APP_VERSION = "6.0"

DATA_DIR = Path("data")
HISTORY_DIR = DATA_DIR / "history"

DATA_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# 1. 簡約白底與卡片 CSS 樣式
# =====================================================================

st.markdown(
    """
<style>
.main {
    background-color: #FFFFFF;
}
[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF;
    color: #111111;
}
[data-testid="stSidebar"] {
    background-color: #F8F9FA;
    border-right: 1px solid #E5E7EB;
}
h1, h2, h3, h4, h5, h6 {
    color: #111111 !important;
}
.gold-title {
    color: #D97706 !important;
    font-weight: 800;
    letter-spacing: 1px;
}
.result-card {
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================================
# 2. Session State 初始化
# =====================================================================

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "processed_images" not in st.session_state:
    st.session_state.processed_images = []

# =====================================================================
# 3. Gemini API 設定
# =====================================================================

try:
    from google import genai
except ImportError:
    genai = None

GEMINI_MODEL = "gemini-2.5-flash"

def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    if not key:
        key = os.getenv("GEMINI_API_KEY", "")
    return str(key).strip()

@st.cache_resource
def get_gemini_client():
    if genai is None:
        return None
    api_key = get_api_key()
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None

# =====================================================================
# 4. 側邊欄與功能模式
# =====================================================================

st.sidebar.title("⚡ 控制台選單")
mode = st.sidebar.radio("選擇功能模式", ["🚀 AI 跨平台行銷自動化", "🛍️ 買家極速導購前台"])

if mode == "🚀 AI 跨平台行銷自動化":
    st.markdown(f"<h1 class='gold-title'>{APP_NAME} v{APP_VERSION}</h1>", unsafe_allow_html=True)
    st.caption("多圖智慧辨識 × 蝦皮電商 SEO × Threads 流量引流 × 短影音腳本全自動生成")
    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📦 商品與行銷資訊輸入")
        
        product_name = st.text_input("商品名稱", placeholder="例如：Snoopy 史努比寬鬆落肩短T")
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            category = st.selectbox("商品分類", ["服飾鞋包", "3C電子", "居家生活", "美妝保養", "食品飲料", "其他"])
        with c_col2:
            price = st.text_input("售價 (NT$)", placeholder="399")

        key_selling_points = st.text_area(
            "核心賣點 / 促銷優惠 (選填)", 
            placeholder="例如：100%純棉、重磅耐磨、現在下單送同款襪子、滿千免運"
        )
        
        product_link = st.text_input("蝦皮商品/分潤導購連結", placeholder="https://s.shopee.tw/...")
        
        # 多圖上傳支援
        uploaded_files = st.file_uploader(
            "上傳商品多角度照片 (支援多張：正面、細節、情境照等)", 
            type=None,
            accept_multiple_files=True
        )
        
        st.session_state.processed_images = []
        if uploaded_files:
            st.write(f"✅ 已成功上傳 {len(uploaded_files)} 張圖片：")
            img_cols = st.columns(min(len(uploaded_files), 3))
            for idx, file in enumerate(uploaded_files):
                try:
                    img_bytes = file.getvalue()
                    image = Image.open(io.BytesIO(img_bytes))
                    if image.mode in ("RGBA", "P"):
                        image = image.convert("RGB")
                    st.session_state.processed_images.append(image)
                    with img_cols[idx % 3]:
                        st.image(image, caption=f"圖 {idx+1}", use_column_width=True)
                except Exception as e:
                    st.warning(f"⚠️ 圖 {idx+1} 解析提示: {e}")

    with col2:
        st.subheader("⚙️ 自動化生成配置")
        tone = st.selectbox(
            "文案風格語氣", 
            ["Z世代真實推薦 (帶有共鳴與微毒舌)", "高級質感電商 (強調美學與生活風格)", "強導購降價風 (限時搶購、促銷刺激)", "幽默搞笑吐槽風"]
        )
        
        target_audience = st.text_input("目標客群 (Target Audience)", placeholder="例如：大學生、情侶裝、喜歡休閒穿搭的年輕人")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 開始執行全自動 AI 素材生成", use_container_width=True):
            api_key = get_api_key()
            if not api_key:
                st.error("❌ 尚未設定 GEMINI_API_KEY，請至 Streamlit Secrets 設定金鑰。")
            elif not product_name:
                st.warning("⚠️ 請至少輸入商品名稱！")
            else:
                with st.spinner("🤖 黑金剛 AI 正在進行多模態深度解析並撰寫跨平台行銷套組..."):
                    client = get_gemini_client()
                    
                    # 精準結構化 Prompt，要求分流輸出
                    prompt = f"""
請扮演頂級的電商營運長與社群行銷總監。針對以下商品進行深度分析，並產出繁體中文的「跨平台行銷自動化套組」。

【商品資訊】
- 名稱：{product_name}
- 分類：{category}
- 售價：NT$ {price if price else '未定'}
- 核心賣點/促銷：{key_selling_points if key_selling_points else '無特別指定'}
- 目標客群：{target_audience if target_audience else '大眾市場'}
- 風格語氣：{tone}

請嚴格按照以下三大區塊輸出內容（請使用 Markdown 標題分隔）：

# 1. 🛒 蝦皮 / 網拍平台 SEO 專用文案
- **SEO 吸引人標題**（內含高流量搜尋關鍵字）
- **賣點介紹與規格亮點**（條列式優勢）
- **安心保障與下單引導**

# 2. 📱 Threads / IG 爆款引流貼文
- 抓眼球的開頭（結合風格語氣）
- 能夠引起互動、留言「+1」或私訊的高共鳴內文
- 建議標籤 (Hashtags)

# 3. 🎬 TikTok / Reels 30秒短影音腳本
- **秒數與畫面設定** (0-3秒黃金吸睛畫面)
- **口語化旁白與對白**
- **字幕與音樂風格建議**
"""
                    try:
                        if client:
                            contents = [prompt]
                            # 將所有上傳的照片加入多模態輸入清單
                            if st.session_state.processed_images:
                                contents.extend(st.session_state.processed_images)
                            
                            response = client.models.generate_content(
                                model=GEMINI_MODEL,
                                contents=contents
                            )
                            result_text = getattr(response, "text", None) or str(response)
                        else:
                            raise RuntimeError("Gemini Client 初始化失敗，請檢查 API Key")

                        st.session_state.last_result = result_text
                        st.success("🎉 全平台行銷套組生成完畢！")
                    except Exception as e:
                        st.error(f"❌ 呼叫 AI 發生錯誤: {e}")

    # 顯示結構化成果輸出
    if st.session_state.last_result:
        st.markdown("---")
        st.subheader("📊 AI 商業自動化生成成果")
        st.markdown(f"<div class='result-card'>{st.session_state.last_result}</div>", unsafe_allow_html=True)

elif mode == "🛍️ 買家極速導購前台":
    st.markdown("<h2 style='text-align: center;'>🔥 精選好物導購</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>無腦直達，閉眼入不踩雷的好物推薦</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.info("💡 這裡展示您的前台導購介面。點擊按鈕將直接帶入指定的蝦皮分潤連結。")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🌟 熱銷好物範例：史努比寬鬆短T")
        st.write("精選高回購、高評價的優質潮流服飾。")
        if product_link:
            st.link_button("🛒 點擊前往蝦皮搶購", product_link, use_container_width=True)
        else:
            st.link_button("🛒 點擊前往蝦皮搶購", "https://s.shopee.tw/your_link", use_container_width=True)
