import os
import io
import json
from datetime import datetime
from pathlib import Path
import streamlit as st
from PIL import Image

# =====================================================================
# 0. APP 基本設定
# =====================================================================

APP_NAME = "黑金鋼 AI 商業自動化總控台 PRO"
APP_VERSION = "7.9"

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
# 1. 樣式設定
# =====================================================================

st.markdown(
    """
<style>
.main { background-color: #FFFFFF; }
[data-testid="stAppViewContainer"] { background-color: #FFFFFF; color: #111111; }
[data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #E5E7EB; }
h1, h2, h3, h4, h5, h6 { color: #111111 !important; }
.gold-title { color: #D97706 !important; font-weight: 800; letter-spacing: 1px; }
.result-card { background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 12px; padding: 24px; margin-bottom: 20px; }
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================================
# 2. Session State 初始化
# =====================================================================

if "auto_name" not in st.session_state:
    st.session_state.auto_name = ""
if "auto_category" not in st.session_state:
    st.session_state.auto_category = "服飾鞋包"
if "auto_price" not in st.session_state:
    st.session_state.auto_price = ""
if "auto_selling_points" not in st.session_state:
    st.session_state.auto_selling_points = ""
if "product_link" not in st.session_state:
    st.session_state.product_link = "https://s.shopee.tw/your_link"
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "processed_images_list" not in st.session_state:
    st.session_state.processed_images_list = []

# =====================================================================
# 3. 歷史紀錄存取函式
# =====================================================================

def save_history_record(name, category, price, points, result_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip()[:20]
    filename = HISTORY_DIR / f"{timestamp}_{safe_name}.json"
    
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name, "category": category, "price": price, "points": points, "result_text": result_text
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

def load_all_histories():
    records = []
    files = sorted(HISTORY_DIR.glob("*.json"), reverse=True)
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                records.append((file.name, json.load(f)))
        except Exception:
            pass
    return records

# =====================================================================
# 4. API 設定與強固型客戶端初始化
# =====================================================================

try:
    from google import genai
except ImportError:
    genai = None

GEMINI_MODEL = "gemini-2.5-flash"

def get_api_key():
    key = ""
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
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
        # 優先嘗試新版 SDK Client 初始化
        return genai.Client(api_key=api_key)
    except Exception:
        try:
            # 相容性備援機制
            import google.generativeai as fallback_genai
            fallback_genai.configure(api_key=api_key)
            return fallback_genai
        except Exception:
            return None

# =====================================================================
# 5. 側邊欄與功能模式
# =====================================================================

st.sidebar.title("⚡ 控制台選單")
mode = st.sidebar.radio("選擇功能模式", ["🚀 圖片辨識與行銷總控台", "🛍️ 買家極速導購前台"])

st.sidebar.markdown("---")
st.sidebar.subheader("📜 歷史生成紀錄")
histories = load_all_histories()

if histories:
    history_options = {f"{data['timestamp']} - {data['name']}": fname for fname, data in histories}
    selected_label = st.sidebar.selectbox("選擇歷史紀錄載入", ["-- 請選擇紀錄 --"] + list(history_options.keys()))
    
    if selected_label != "-- 請選擇紀錄 --":
        target_file = HISTORY_DIR / history_options[selected_label]
        if target_file.exists():
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    h_data = json.load(f)
                if st.sidebar.button("📂 載入此筆歷史紀錄", use_container_width=True):
                    st.session_state.auto_name = h_data.get("name", "")
                    st.session_state.auto_category = h_data.get("category", "服飾鞋包")
                    st.session_state.auto_price = h_data.get("price", "")
                    st.session_state.auto_selling_points = h_data.get("points", "")
                    st.session_state.last_result = h_data.get("result_text", "")
                    st.success("🎉 載入成功！")
                    st.rerun()
            except Exception as e:
                st.sidebar.error(f"載入失敗: {e}")
else:
    st.sidebar.caption("尚無歷史紀錄。")

# =====================================================================
# 主畫面邏輯
# =====================================================================

if mode == "🚀 圖片辨識與行銷總控台":
    st.markdown(f"<h1 class='gold-title'>{APP_NAME} v{APP_VERSION}</h1>", unsafe_allow_html=True)
    st.caption("平板相簿多選 ＋ 智慧辨識填空 ＋ 跨平台行銷套組 ＋ 歷史自動歸檔")
    st.markdown("---")

    current_key = get_api_key()
    if not current_key:
        st.error("❌ 尚未設定 GEMINI_API_KEY！請至 Streamlit Secrets 檢查設定。")
    else:
        st.success("✅ GEMINI_API_KEY 已順利連線！")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🖼️ 1. 從平板相簿選取商品相片")
        uploaded_files = st.file_uploader(
            "選擇或拖曳相片檔案 (支援平板多張相片選取)", 
            type=["jpg", "jpeg", "png", "webp", "heic"], 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.session_state.processed_images_list = []
            for uploaded_file in uploaded_files:
                try:
                    img_bytes = uploaded_file.getvalue()
                    image = Image.open(io.BytesIO(img_bytes))
                    if image.mode in ("RGBA", "P"):
                        image = image.convert("RGB")
                    st.session_state.processed_images_list.append(image)
                except Exception as e:
                    st.warning(f"⚠️ 解析相片提示: {e}")
            
            if st.session_state.processed_images_list:
                st.session_state.processed_image = st.session_state.processed_images_list[0]
                st.markdown(f"**已成功載入 {len(st.session_state.processed_images_list)} 張相片：**")
                st.image(st.session_state.processed_images_list, width=100)

        if st.button("✨ 讓 AI 自動辨識相片並填入空格", use_container_width=True):
            if not current_key:
                st.error("❌ 尚未設定 GEMINI_API_KEY")
            elif not st.session_state.processed_images_list:
                st.warning("⚠️ 請先從平板相簿上傳至少一張商品相片！")
            else:
                with st.spinner("🤖 AI 正在深度辨識平板相片中的商品..."):
                    client = get_gemini_client()
                    if not client:
                        st.error("❌ Gemini Client 初始化失敗。")
                        st.stop()

                    parse_prompt = """
請分析這些商品相片，並以嚴格的 JSON 格式回傳以下欄位（不要包在 markdown code block 裡，直接回傳純 JSON）：
{
  "name": "建議的商品名稱",
  "category": "分類（必須從這幾個裡面選一個：服飾鞋包, 3C電子, 居家生活, 美妝保養, 食品飲料, 其他）",
  "price": "建議售價數字（例如 399）",
  "selling_points": "核心賣點與材質特徵描述"
}
"""
                    try:
                        contents = [parse_prompt] + st.session_state.processed_images_list
                        # 相容新舊版 SDK 呼叫方式
                        if hasattr(client, "models"):
                            response = client.models.generate_content(model=GEMINI_MODEL, contents=contents)
                        else:
                            model = client.GenerativeModel(GEMINI_MODEL)
                            response = model.generate_content(contents)

                        raw_text = getattr(response, "text", "").strip()
                        if raw_text.startswith("```json"): raw_text = raw_text[7:]
                        if raw_text.endswith("```"): raw_text = raw_text[:-3]
                        
                        data = json.loads(raw_text.strip())
                        st.session_state.auto_name = data.get("name", "")
                        st.session_state.auto_category = data.get("category", "服飾鞋包")
                        st.session_state.auto_price = str(data.get("price", ""))
                        st.session_state.auto_selling_points = data.get("selling_points", "")
                        st.success("🎉 AI 辨識完成！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 自動辨識失敗: {e}")

    with col2:
        st.subheader("📝 2. 自動填入與行銷設定")
        product_name = st.text_input("商品名稱", value=st.session_state.auto_name)
        
        c_col1, c_col2 = st.columns(2)
        categories_list = ["服飾鞋包", "3C電子", "居家生活", "美妝保養", "食品飲料", "其他"]
        cat_index = categories_list.index(st.session_state.auto_category) if st.session_state.auto_category in categories_list else 0
        with c_col1:
            category = st.selectbox("商品分類", categories_list, index=cat_index)
        with c_col2:
            price = st.text_input("售價 (NT$)", value=st.session_state.auto_price)

        key_selling_points = st.text_area("核心賣點 / 促銷優惠", value=st.session_state.auto_selling_points)
        st.session_state.product_link = st.text_input("分潤導購連結", value=st.session_state.product_link)
        tone = st.selectbox("文案風格語氣", ["Z世代真實推薦 (微毒舌共鳴)", "高級質感電商", "強導購降價風"])
        
        if st.button("🚀 產出完整跨平台行銷文案套組", use_container_width=True):
            if not current_key:
                st.error("❌ 尚未設定 GEMINI_API_KEY")
            elif not product_name:
                st.warning("⚠️ 請先填入商品名稱！")
            else:
                with st.spinner("🤖 正在生成各平台文案並自動歸檔..."):
                    client = get_gemini_client()
                    if not client:
                        st.error("❌ Gemini Client 初始化失敗。")
                        st.stop()

                    prompt = f"""
請針對商品「{product_name}」（分類：{category}，售價：NT${price}，賣點：{key_selling_points}，風格：{tone}）生成：
1. 🛒 蝦皮 SEO 賣場文案
2. 📱 Threads 爆款引流貼文
3. 🎬 30秒短影音旁白腳本
"""
                    try:
                        contents = [prompt] + (st.session_state.processed_images_list if st.session_state.processed_images_list else [])
                        if hasattr(client, "models"):
                            response = client.models.generate_content(model=GEMINI_MODEL, contents=contents)
                        else:
                            model = client.GenerativeModel(GEMINI_MODEL)
                            response = model.generate_content(contents)

                        result_str = getattr(response, "text", "")
                        st.session_state.last_result = result_str
                        save_history_record(product_name, category, price, key_selling_points, result_str)
                        st.success("🎉 文案生成完畢，已自動存入歷史紀錄！")
                    except Exception as e:
                        st.error(f"❌ 發生錯誤: {e}")

    if st.session_state.last_result:
        st.markdown("---")
        st.subheader("📊 AI 行銷生成成果輸出與匯出")
        st.markdown(f"<div class='result-card'>{st.session_state.last_result}</div>", unsafe_allow_html=True)
        st.download_button(
            label="📥 一鍵下載完整行銷文案 (.txt)",
            data=st.session_state.last_result,
            file_name=f"行銷文案_{product_name if product_name else 'product'}.txt",
            mime="text/plain",
            use_container_width=True
        )

elif mode == "🛍️ 買家極速導購前台":
    st.markdown("<h2 style='text-align: center;'>🔥 精選好物導購中心</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>無腦直達，嚴選優質好物，點擊立即搶購</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_shop1, col_shop2 = st.columns([1, 1], gap="large")
    with col_shop1:
        if st.session_state.processed_images_list:
            st.image(st.session_state.processed_images_list[0], caption=st.session_state.auto_name or "精選主打商品", use_container_width=True)
        elif st.session_state.processed_image is not None:
            st.image(st.session_state.processed_image, caption=st.session_state.auto_name or "精選主打商品", use_container_width=True)
        else:
            st.info("💡 目前後台尚未上傳平板相簿中的商品相片。")
            
    with col_shop2:
        st.markdown(f"### 🌟 {st.session_state.auto_name or '精選潮流商品'}")
        st.markdown(f"**分類**：{st.session_state.auto_category}")
        st.markdown(f"**特惠價**：<span style='color: #D97706; font-size: 24px; font-weight: bold;'>NT$ {st.session_state.auto_price or '399'}</span>", unsafe_allow_html=True)
        st.markdown(f"**商品特色**：\n{st.session_state.auto_selling_points or '優質選物，錯過不再。'}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("🛒 立即前往搶購 (賺取分潤)", st.session_state.product_link, use_container_width=True)
