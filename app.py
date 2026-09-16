import os
import json
import base64
from datetime import datetime
from pathlib import Path

import streamlit as st

# ============================================================
# 黑金剛 AI 多 AI 電商總控中心 PRO
# 單檔 Streamlit App
# OpenAI 主控版
# ============================================================

APP_NAME = "黑金剛 AI 多 AI 電商總控中心 PRO"
APP_VERSION = "4.0"

DATA_DIR = Path("data")
HISTORY_DIR = DATA_DIR / "history"
MEDIA_DIR = DATA_DIR / "media"

for folder in (DATA_DIR, HISTORY_DIR, MEDIA_DIR):
    folder.mkdir(parents=True, exist_ok=True)


# ============================================================
# 0. 套件自動檢查
# ============================================================
def ensure_openai():
    try:
        from openai import OpenAI
        return OpenAI
    except ImportError:
        import subprocess
        import sys

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "openai"]
        )
        from openai import OpenAI
        return OpenAI


# ============================================================
# 1. Streamlit 設定
# ============================================================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .sub-title {
        color: #888;
        margin-top: 0;
    }
    .agent-card {
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 10px;
        background: rgba(255,255,255,.025);
    }
    .result-box {
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 12px;
        padding: 14px;
        background: rgba(255,255,255,.025);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 2. 基礎工具
# ============================================================
def get_secret(name: str) -> str:
    value = os.environ.get(name, "")
    if value:
        return value

    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""


def save_history(record: dict):
    filename = HISTORY_DIR / (
        datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def image_to_data_url(uploaded_file):
    raw = uploaded_file.getvalue()
    mime = uploaded_file.type or "image/jpeg"
    encoded = base64.b64encode(raw).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def safe_text(value):
    return str(value or "").strip()


def calculate_profit(price, cost, commission):
    try:
        price = float(price or 0)
        cost = float(cost or 0)
        commission = float(commission or 0)
        fee = price * commission / 100
        profit = price - cost - fee
        margin = (profit / price * 100) if price else 0
        return fee, profit, margin
    except Exception:
        return 0, 0, 0


# ============================================================
# 3. OpenAI
# ============================================================
def create_openai_client(api_key):
    if not api_key:
        raise ValueError("尚未設定 OpenAI API Key。")

    OpenAI = ensure_openai()
    return OpenAI(api_key=api_key)


# ============================================================
# 4. AI 核心規則
# ============================================================
CORE_RULES = """
你是「黑金剛 AI 多 AI 電商總控中心 PRO」的商品分析主控 AI。

【最高優先級：商品真實性】
1. 使用者上傳的商品圖片是主要視覺真實依據。
2. 不得自行捏造圖片中無法確認的品牌、規格、容量、材質、成分、
   功效、認證、產地、數量、保固或其他商品資訊。
3. 如果圖片無法確認，必須寫「無法由圖片確認，待確認」。
4. 不得擅自修改品牌名稱、包裝文字、商品外觀、顏色、比例。
5. 不得加入圖片中不存在的其他商品。
6. 不得為商品創造醫療、療效、保證性或誇大性宣稱。
7. 文案可以做行銷整理，但不能把猜測寫成事實。

【圖片分析】
- 優先辨識主要商品。
- 如果有多個商品，選擇最大、最清楚、最主要的一個作為主商品。
- 只能描述圖片可合理確認的內容。

【電商文案】
- 簡潔、清楚、適合電商。
- 避免虛假承諾。
- 不要自行加入價格、贈品、折扣、官方授權等未提供資訊。

【影片 Prompt】
- 上傳商品圖片為唯一產品視覺參考。
- 商品本體、Logo、包裝、文字、顏色、形狀、比例保持一致。
- 不加入人物、手、代言人，除非使用者明確要求。
- 不產生浮水印。
- 不產生額外產品。
- 避免產品變形、融化、閃爍、重複、消失。
- 影片要有清楚主題、商品展示、使用情境或價值呈現，
  避免整段只有單純縮放圖片。
"""


def build_product_prompt(product):
    return f"""
{CORE_RULES}

請分析以下商品資料與商品圖片。

【使用者提供的資料】
商品名稱：{product['name']}
商品分類：{product['category']}
售價：{product['price']}
成本：{product['cost']}
分潤比例：{product['commission']}%
月銷量：{product['sales']}
商品評分：{product['rating']}
商品連結：{product['link']}
商品規格補充：{product['spec']}

請輸出 JSON，格式必須為：

{{
  "image_analysis": "圖片可確認的商品外觀與資訊",
  "uncertain_info": ["無法確認的資訊"],
  "title": "蝦皮商品標題",
  "short_description": "短版商品介紹",
  "full_description": "完整商品描述",
  "features": [
    "特色1",
    "特色2",
    "特色3",
    "特色4",
    "特色5"
  ],
  "specifications": [
    "可確認規格1",
    "可確認規格2"
  ],
  "seo_keywords": [
    "關鍵字1",
    "關鍵字2",
    "關鍵字3",
    "關鍵字4",
    "關鍵字5"
  ],
  "hashtags": [
    "#標籤1",
    "#標籤2",
    "#標籤3",
    "#標籤4",
    "#標籤5"
  ],
  "tiktok_copy": "TikTok短影音文案",
  "video_theme": "影片核心主題",
  "video_script": [
    {{
      "time": "0-3秒",
      "scene": "畫面",
      "camera": "運鏡",
      "text": "畫面文字"
    }},
    {{
      "time": "3-7秒",
      "scene": "畫面",
      "camera": "運鏡",
      "text": "畫面文字"
    }},
    {{
      "time": "7-11秒",
      "scene": "畫面",
      "camera": "運鏡",
      "text": "畫面文字"
    }},
    {{
      "time": "11-15秒",
      "scene": "畫面",
      "camera": "運鏡",
      "text": "畫面文字"
    }}
  ],
  "jimeng_prompt": "即夢AI 2.5英文影片Prompt",
  "kling_prompt": "可靈英文影片Prompt",
  "image_prompt": "商品廣告圖片Prompt"
}}

只輸出合法 JSON，不要輸出 Markdown。
"""


def generate_product_ai(product, image_data_url, model):
    client = create_openai_client(st.session_state.openai_api_key)

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": CORE_RULES,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": build_product_prompt(product),
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url,
                    },
                ],
            },
        ],
    )

    text = response.output_text.strip()

    # 嘗試清理可能的 markdown code fence
    if text.startswith("```"):
        text = text.replace("```json", "", 1).replace("```", "")
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "raw_output": text,
            "parse_error": True,
        }


# ============================================================
# 5. 頁首
# ============================================================
st.markdown(
    f'<div class="main-title">🖤 {APP_NAME}</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="sub-title">PRO {APP_VERSION}｜OpenAI API 主控｜商品 → 文案 → 短影音 → 素材</div>',
    unsafe_allow_html=True,
)
st.markdown("---")


# ============================================================
# 6. Sidebar
# ============================================================
with st.sidebar:
    st.header("⚙️ 系統控制台")

    st.session_state.openai_api_key = st.text_input(
        "OpenAI API Key",
        value=get_secret("OPENAI_API_KEY"),
        type="password",
        help="建議使用 Streamlit Secrets 或環境變數保存 API Key。",
    )

    model = st.selectbox(
        "OpenAI 模型",
        [
            "gpt-5.6",
            "gpt-5.6-mini",
            "gpt-4o",
            "gpt-4o-mini",
        ],
        index=0,
    )

    st.session_state.kling_ak = st.text_input(
        "可靈 AK",
        value=get_secret("KLING_AK"),
        type="password",
    )

    st.session_state.kling_sk = st.text_input(
        "可靈 SK",
        value=get_secret("KLING_SK"),
        type="password",
    )

    st.markdown("---")
    st.subheader("🤖 AI Agent")

    agents = [
        "總控 AI",
        "商品視覺分析",
        "蝦皮上架",
        "定價分析",
        "文案",
        "SEO",
        "TikTok",
        "導演",
        "即夢 Prompt",
        "可靈 Prompt",
        "圖片 Prompt",
        "真實性檢查",
        "歷史紀錄",
    ]

    for agent in agents:
        st.markdown(f"🟢 {agent}")

    st.markdown("---")
    st.info(
        "API Key 由使用者自行提供。\n\n"
        "本版本不把任何 API Key 寫死在程式碼內。"
    )


# ============================================================
# 7. Dashboard
# ============================================================
st.subheader("📊 AI 電商總控 Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("AI Agent", "13+")

with c2:
    st.metric("商品分析", "OpenAI Vision")

with c3:
    st.metric("短影音", "即夢 / 可靈")

with c4:
    st.metric("資料紀錄", "JSON")


# ============================================================
# 8. 商品資料
# ============================================================
st.markdown("---")
st.subheader("📦 商品上架工作台")

left, right = st.columns([1, 1])

with left:
    product_name = st.text_input("商品名稱", placeholder="例如：16000Pa 手持吸塵器")
    category = st.text_input("商品分類", placeholder="例如：居家清潔")

    price = st.number_input(
        "商品售價",
        min_value=0.0,
        value=0.0,
        step=10.0,
    )

    cost = st.number_input(
        "商品成本",
        min_value=0.0,
        value=0.0,
        step=10.0,
    )

    commission = st.number_input(
        "分潤比例 (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5,
    )

with right:
    sales = st.number_input(
        "月銷量",
        min_value=0,
        value=0,
        step=1,
    )

    rating = st.number_input(
        "商品評分",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1,
    )

    link = st.text_input(
        "商品連結",
        placeholder="https://...",
    )

    spec = st.text_area(
        "商品規格 / 已知資訊",
        placeholder="輸入你已確認的尺寸、材質、容量等資訊；不確定就不要填。",
        height=120,
    )


# ============================================================
# 9. 利潤計算
# ============================================================
fee, profit, margin = calculate_profit(
    price,
    cost,
    commission,
)

st.markdown("### 💰 基礎利潤試算")

p1, p2, p3 = st.columns(3)

with p1:
    st.metric("預估分潤 / 手續費", f"${fee:,.2f}")

with p2:
    st.metric("預估單件利潤", f"${profit:,.2f}")

with p3:
    st.metric("預估利潤率", f"{margin:.2f}%")


# ============================================================
# 10. 商品圖片
# ============================================================
st.markdown("---")
st.subheader("🖼️ 商品圖片")

uploaded_file = st.file_uploader(
    "上傳商品圖片 JPG / JPEG / PNG",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file:
    st.image(
        uploaded_file,
        caption="AI 唯一主要商品視覺參考",
        use_container_width=True,
    )

    st.caption(
        "AI 將以此圖片作為商品外觀主要依據，不自行修改品牌、包裝、文字、顏色與比例。"
    )


# ============================================================
# 11. 執行總控
# ============================================================
st.markdown("---")

run_ai = st.button(
    "🚀 啟動黑金剛 AI 商品全流程",
    type="primary",
    use_container_width=True,
)

if run_ai:
    if not st.session_state.openai_api_key:
        st.error("❌ 請先設定 OpenAI API Key。")
        st.stop()

    if not uploaded_file:
        st.error("❌ 請先上傳商品圖片。")
        st.stop()

    product = {
        "name": safe_text(product_name),
        "category": safe_text(category),
        "price": price,
        "cost": cost,
        "commission": commission,
        "sales": sales,
        "rating": rating,
        "link": safe_text(link),
        "spec": safe_text(spec),
    }

    if not product["name"]:
        st.warning("⚠️ 尚未填商品名稱，AI 將主要依圖片判斷。")

    with st.spinner("🧠 黑金剛 AI 正在分析商品並建立完整電商素材……"):
        try:
            image_data_url = image_to_data_url(uploaded_file)

            result = generate_product_ai(
                product,
                image_data_url,
                model,
            )

            st.session_state.ai_result = result
            st.session_state.product_data = product

            record = {
                "created_at": datetime.now().isoformat(),
                "product": product,
                "result": result,
            }

            save_history(record)

            st.success("✅ AI 商品全流程完成！")

        except Exception as e:
            st.error(f"❌ AI 執行失敗：{e}")


# ============================================================
# 12. AI 結果
# ============================================================
if "ai_result" in st.session_state:
    result = st.session_state.ai_result

    st.markdown("---")
    st.subheader("🧠 AI 分析結果")

    if result.get("parse_error"):
        st.warning("AI 已產生結果，但 JSON 格式解析失敗，以下顯示原始內容。")
        st.code(result.get("raw_output", ""), language="text")
        st.stop()

    tabs = st.tabs(
        [
            "📦 商品分析",
            "🛒 蝦皮",
            "🎵 TikTok",
            "🎬 即夢",
            "🎥 可靈",
            "🎨 圖片",
            "🛡️ 真實性",
        ]
    )

    # --------------------------------------------------------
    # 商品分析
    # --------------------------------------------------------
    with tabs[0]:
        st.markdown("### 🔎 圖片辨識")
        st.write(result.get("image_analysis", ""))

        st.markdown("### ⭐ 商品特色")
        for item in result.get("features", []):
            st.write(f"• {item}")

        st.markdown("### 📐 規格")
        for item in result.get("specifications", []):
            st.write(f"• {item}")

    # --------------------------------------------------------
    # 蝦皮
    # --------------------------------------------------------
    with tabs[1]:
        st.markdown("### 🏷️ 商品標題")
        title = result.get("title", "")
        st.code(title, language="text")

        st.markdown("### 📝 短版介紹")
        st.write(result.get("short_description", ""))

        st.markdown("### 📋 完整商品描述")
        description = result.get("full_description", "")
        st.text_area(
            "可直接複製",
            description,
            height=300,
            key="shopee_description",
        )

        st.markdown("### 🔍 SEO")
        st.write("、".join(result.get("seo_keywords", [])))

        st.markdown("### # Hashtag")
        st.write(" ".join(result.get("hashtags", [])))

    # --------------------------------------------------------
    # TikTok
    # --------------------------------------------------------
    with tabs[2]:
        st.markdown("### 🎵 TikTok 文案")
        st.text_area(
            "TikTok",
            result.get("tiktok_copy", ""),
            height=250,
            key="tiktok_copy",
        )

        st.markdown("### 🎬 影片主題")
        st.write(result.get("video_theme", ""))

        st.markdown("### 🎞️ 15 秒腳本")
        for scene in result.get("video_script", []):
            with st.expander(
                f"{scene.get('time', '')}｜{scene.get('scene', '')}"
            ):
                st.write(f"**運鏡：** {scene.get('camera', '')}")
                st.write(f"**畫面文字：** {scene.get('text', '')}")

    # --------------------------------------------------------
    # 即夢
    # --------------------------------------------------------
    with tabs[3]:
        jimeng = result.get("jimeng_prompt", "")
        st.markdown("### 即夢 AI 2.5 Prompt")
        st.text_area(
            "即夢影片指令",
            jimeng,
            height=450,
            key="jimeng_prompt",
        )

        st.caption(
            "此版本產生的是可直接整理 / 貼入即夢工作流使用的 Prompt，"
            "不是假裝已經呼叫即夢 API。"
        )

    # --------------------------------------------------------
    # 可靈
    # --------------------------------------------------------
    with tabs[4]:
        kling = result.get("kling_prompt", "")
        st.markdown("### 可靈 AI Video Prompt")
        st.text_area(
            "可靈影片指令",
            kling,
            height=450,
            key="kling_prompt",
        )

        st.caption(
            "目前先由 OpenAI 產生影片 Prompt。"
            "只有取得並確認可靈 API 的實際 API 文件與權限後，"
            "才應在此接入真正影片生成任務。"
        )

    # --------------------------------------------------------
    # 圖片
    # --------------------------------------------------------
    with tabs[5]:
        st.markdown("### 🎨 商品廣告圖片 Prompt")
        st.text_area(
            "圖片生成指令",
            result.get("image_prompt", ""),
            height=400,
            key="image_prompt",
        )

    # --------------------------------------------------------
    # 真實性
    # --------------------------------------------------------
    with tabs[6]:
        st.markdown("### 🛡️ 無法由圖片確認 / 待確認")

        uncertain = result.get("uncertain_info", [])

        if uncertain:
            for item in uncertain:
                st.warning(str(item))
        else:
            st.success("目前 AI 沒有額外列出需要確認的資訊。")

    # --------------------------------------------------------
    # 全部 JSON
    # --------------------------------------------------------
    st.markdown("---")
    with st.expander("🔧 查看 AI 原始 JSON"):
        st.json(result)


# ============================================================
# 13. 歷史紀錄
# ============================================================
st.markdown("---")
st.subheader("🕘 歷史紀錄")

history_files = sorted(
    HISTORY_DIR.glob("*.json"),
    reverse=True,
)

if not history_files:
    st.info("目前還沒有歷史紀錄。")
else:
    st.write(f"目前共有 {len(history_files)} 筆紀錄。")

    for file in history_files[:20]:
        with st.expander(file.stem):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                st.json(data)

            except Exception as e:
                st.error(f"讀取紀錄失敗：{e}")


# ============================================================
# 14. 系統資訊
# ============================================================
st.markdown("---")

with st.expander("ℹ️ 系統資訊"):
    st.write(f"系統名稱：{APP_NAME}")
    st.write(f"版本：{APP_VERSION}")
    st.write("AI 主控：OpenAI API")
    st.write("介面：Streamlit")
    st.write("資料儲存：data/")
    st.write("影片：由 Prompt / API 工作流處理")
    st.write("會員系統：預留")
    st.write("Shopee 自動上架 API：預留")


# ============================================================
# 15. Footer
# ============================================================
st.markdown(
    """
    <div style="text-align:center;color:#777;padding:30px 0;">
        🖤 黑金剛 AI 多 AI 電商總控中心 PRO<br>
        商品真實性優先｜AI 主控｜電商內容工作流
    </div>
    """,
    unsafe_allow_html=True,
)
