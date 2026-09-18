import os
import base64
from pathlib import Path
import streamlit as st
from PIL import Image

# =====================================================================
# 0. APP 基本設定 (全白清爽介面)
# =====================================================================

APP_NAME = "黑金剛 AI 電商總控中心 PRO"
APP_VERSION = "5.4"

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
# 1. 簡約白底 CSS 樣式
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
.clean-card {
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
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
# 4. 側邊欄與功能切換
# =====================================================================

st.sidebar.title("⚡ 控制台選單")
mode = st.sidebar.radio("選擇功能模式", ["🚀 AI 商品與影音總控台", "🛍️ 買家極速導購前台"])

if mode == "🚀 AI 商品與影音總控台":
    st.markdown(f"<h1 class='gold-title'>{APP_NAME} v{APP_VERSION}</h1>", unsafe_allow_html=True)
    st.caption("結合 Gemini AI，一鍵生成蝦皮 SEO 文案、TikTok 爆款腳本與多模態影音指令！")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📦 商品資訊輸入")
        product_name = st.text_input("商品名稱", placeholder="例如：Snoopy 史努比寬鬆短T")
        category = st.selectbox("商品分類", ["3C電子", "服飾鞋包", "居家生活", "美妝保養", "食品飲料", "其他"])
        price = st.text_input("售價 (NT$)", placeholder="399")
        product_link = st.text_input("蝦皮商品/分潤連結", placeholder="https://s.shopee.tw/...")
        
        # 移除格式限制（type=None），允許上傳任何規格/格式的圖片
        uploaded_file = st.file_uploader(
            "上傳商品圖片 (支援全規格/所有圖片格式)", 
            type=None
        )
        
        if uploaded_file is not None:
            try:
                # 嘗試讀取並預覽圖片
                image = Image.open(uploaded_file)
                st.image(image, caption=f"已成功載入圖片: {uploaded_file.name}", use_column_width=True)
            except Exception as e:
                st.info(f"💡 檔案已成功上傳（格式：{uploaded_file.name.split('.')[-1]}），AI 將直接進行深度多模態解析。")

    with col2:
        st.subheader("⚙️ 行銷與生成設定")
        tone = st.selectbox("文案風格語氣", ["Z世代真實推薦", "高級質感電商", "強導購降價風", "幽默毒舌避雷"])
        platforms = st.multiselect("發布平台", ["蝦皮", "TikTok", "Instagram", "Threads"], default=["蝦皮", "Threads"])
        
        if st.button("🚀 開始執行 AI 多模態生成", use_container_width=True):
            api_key = get_api_key()
            if not api_key:
                st.error("❌ 尚未設定 GEMINI_API_KEY，請至 Streamlit Secrets 設定金鑰。")
            elif not product_name:
                st.warning("⚠️ 請至少輸入商品名稱！")
            else:
                with st.spinner("🤖 黑金剛 AI 正在深度分析商品與生成全套素材..."):
                    client = get_gemini_client()
                    prompt = f"請為商品「{product_name}」（分類：{category}，售價：{price}）生成繁體中文的蝦皮 SEO 標題、商品描述、Threads 爆款文案以及 30 秒短影音腳本。風格為：{tone}。"
                    
                    try:
                        if uploaded_file and client:
                            uploaded_file.seek(0)  # 重置讀取指標
                            image_bytes = uploaded_file.getvalue()
                            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                            mime_type = uploaded_file.type or "image/jpeg"
                            
                            response = client.interactions.create(
                                model=GEMINI_MODEL,
                                input=[
                                    {"type": "text", "text": prompt},
                                    {"type": "image", "data": image_b64, "mime_type": mime_type}
                                ]
                            )
                        elif client:
                            response = client.interactions.create(
                                model=GEMINI_MODEL,
                                input=prompt
                            )
                        else:
                            raise RuntimeError("Gemini Client 初始化失敗")

                        result_text = getattr(response, "output_text", None) or str(response)
                        st.session_state.last_result = result_text
                        st.success("🎉 生成完畢！")
                    except Exception as e:
                        st.error(f"❌ 呼叫 AI 發生錯誤: {e}")

    # 顯示結果
    if st.session_state.last_result:
        st.markdown("---")
        st.subheader("📊 AI 生成成果輸出")
        st.markdown(f"<div class='clean-card'>{st.session_state.last_result}</div>", unsafe_allow_html=True)

elif mode == "🛍️ 買家極速導購前台":
    st.markdown("<h2 style='text-align: center;'>🔥 精選好物導購</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>無腦直達，閉眼入不踩雷的好物推薦</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.info("💡 這裡展示您的前台導購介面。點擊按鈕將直接帶入指定的蝦皮分潤連結。")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🌟 熱銷好物範例")
        st.write("精選高回購、高評價的優質商品。")
        st.link_button("🛒 點擊前往蝦皮搶購", "https://s.shopee.tw/your_link", use_container_width=True)
