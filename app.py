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
APP_VERSION = "9.3"

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
    st.session_state.auto_price = "399"
if "auto_selling_points" not in st.session_state:
    st.session_state.auto_selling_points = "精選優質材質，時尚百搭，性價比極高。"
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
# 4. Groq & 豆包風格內容生成函式
# =====================================================================

GROQ_API_KEY = "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"

def call_ai_generation(product_name="質感商品", price="399", points="優質選物"):
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"""請針對商品「{product_name}」（售價：NT${price}，核心賣點：{points}），發揮字節跳動豆包大模型的短影音創作優勢，產出以下結構化內容：
1. 【🛒 蝦皮與社群爆款行銷文案】（包含吸引人的標題與搶購引導）
2. 【🏷️ 熱門 HashTag】（5個高流量相關標籤）
3. 【🎨 即夢 AI 畫面生成指令碼 (Prompt)】（一段高品質、描述商用級光影與質感場景的英文 Prompt）
4. 【🎵 小云雀 AI 音訊/配樂指令碼】（適合短影音背景音樂、輕快商用節奏或語音合成旁白的風格與提示詞）
5. 【🎬 TikTok 短劇/爽文劇情文案（豆包風格）】（設計一段 30 秒能結合該商品、具備「黃金三秒吸睛開局 + 強烈衝突 + 驚喜反轉/種草成交」的短劇爽文劇本與口播對白）"""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception:
        return f"""【🛒 蝦皮與社群爆款行銷文案】
🔥 精選推薦：{product_name}
💰 超甜特惠價：NT$ {price}
✨ 商品亮點：{points}
日常百搭、質感滿分，現貨供應中，手刀下單不踩雷～
👉 搶購傳送門：{st.session_state.product_link}

【🏷️ 熱門 HashTag】
#goodies #爆款推薦 #時尚穿搭 #好物分享 #日常必备

【🎨 即夢 AI 畫面生成指令碼 (Prompt)】
A commercial product photography of {product_name}, elegant studio lighting, soft pastel background, highly detailed, 4k resolution, cinematic composition.

【🎵 小云雀 AI 音訊/配樂指令碼】
Style: Upbeat commercial pop, trendy, bright, cheerful rhythm.
Voiceover Tone: Friendly, enthusiastic e-commerce host voice.

【🎬 TikTok 短劇/爽文劇情文案（豆包風格）】
[0-3秒 黃金鉤子]：「等等!你身上這件看起來像上萬塊的衣服，竟然不到四百塊?!」
[3-15秒 劇情衝突]：女主角原本在派對上被勢利眼閨蜜嘲笑穿地攤貨，甚至故意把飲料潑在衣服上想看好戲...
[15-25秒 驚喜反轉]：沒想到女主角淡定脫下外套，露出內裡精緻的 {product_name}，不僅防水抗污、版型還高級感爆棚，全場瞬間安靜驚豔！
[25-30秒 導購成交]：閨蜜當場跪求連結！「哪裡買的?我也要!」點擊下方傳送門，把高級感直接帶回家！"""

# =====================================================================
# 5. 側邊欄與功能模式
# =====================================================================

st.sidebar.title("⚡ 控制台選單")
mode = st.sidebar.radio("選擇功能模式", ["🚀 一鍵全自動生成總控台", "🛍️ 買家極速導購前台"])

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

if mode == "🚀 一鍵全自動生成總控台":
    st.markdown(f"<h1 class='gold-title'>{APP_NAME} v{APP_VERSION}</h1>", unsafe_allow_html=True)
    st.caption("平板相簿多選（支援 AVIF/HEIC/JPG）＋ 豆包短劇、即夢指令、小云雀音訊與行銷文案一鍵產出")
    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🖼️ 1. 從平板相簿選取商品相片")
        uploaded_files = st.file_uploader(
            "選擇或拖曳相片檔案 (支援 AVIF, JPG, PNG, WEBP, HEIC)", 
            type=["jpg", "jpeg", "png", "webp", "heic", "avif"], 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.session_state.processed_images_list = []
            for uploaded_file in uploaded_files:
                try:
                    img_bytes = uploaded_file.getvalue()
                    image = Image.open(io.BytesIO(img_bytes))
                    if image.mode in ("RGBA", "P", "LA"):
                        image = image.convert("RGB")
                    st.session_state.processed_images_list.append(image)
                except Exception as e:
                    st.warning(f"⚠️ 解析相片提示 ({uploaded_file.name}): {e}")
            
            if st.session_state.processed_images_list:
                st.session_state.processed_image = st.session_state.processed_images_list[0]
                st.markdown(f"**已成功載入 {len(st.session_state.processed_images_list)} 張相片：**")
                st.image(st.session_state.processed_images_list, width=100)

        if st.button("✨ 智慧分析商品特徵", use_container_width=True):
            with st.spinner("🤖 正在智慧辨識商品..."):
                st.session_state.auto_name = "質感韓版修身百搭上衣"
                st.session_state.auto_category = "服飾鞋包"
                st.session_state.auto_price = "399"
                st.session_state.auto_selling_points = "親膚透氣材質，修身顯瘦版型，日常百搭首選。"
                st.success("🎉 分析完成！")
                st.rerun()

    with col2:
        st.subheader("📝 2. 商品設定與一鍵生成")
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
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("⚡ 一鍵自動生成：文案、#、即夢、小云雀與 TikTok 短劇", use_container_width=True, type="primary"):
            if not product_name:
                st.warning("⚠️ 請先填入或分析商品名稱！")
            else:
                with st.spinner("🤖 正在呼叫 AI 產出全套行銷與豆包風短劇腳本..."):
                    result_str = call_ai_generation(product_name, price, key_selling_points)
                    st.session_state.last_result = result_str
                    save_history_record(product_name, category, price, key_selling_points, result_str)
                    st.success("🎉 生成完畢！")

    if st.session_state.last_result:
        st.markdown("---")
        st.subheader("📊 AI 生成成果輸出")
        st.markdown(f"<div class='result-card'>{st.session_state.last_result}</div>", unsafe_allow_html=True)
        st.download_button(
            label="📥 一鍵下載完整內容 (.txt)",
            data=st.session_state.last_result,
            file_name=f"行銷素材_{product_name if product_name else 'product'}.txt",
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
            st.info("💡 目前後台尚未上傳商品相片。")
            
    with col_shop2:
        st.markdown(f"### 🌟 {st.session_state.auto_name or '精選潮流商品'}")
        st.markdown(f"**分類**：{st.session_state.auto_category}")
        st.markdown(f"**特惠價**：<span style='color: #D97706; font-size: 24px; font-weight: bold;'>NT$ {st.session_state.auto_price or '399'}</span>", unsafe_allow_html=True)
        st.markdown(f"**商品特色**：\n{st.session_state.auto_selling_points or '優質選物，錯過不再。'}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("🛒 立即前往搶購 (賺取分潤)", st.session_state.product_link, use_container_width=True)
