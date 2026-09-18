# =====================================================================
# 黑金剛 AI 多 AI 電商總控中心 PRO
# UNIVERSAL PRODUCT AI ENGINE
# Version 5.0
#
# 全商品 / 選項式 / Gemini API / 商品圖片分析
# Shopee / TikTok / IG / Threads / Affiliate
# 即夢 AI 2.5 / Seedance 2.0 Prompt
#
# API KEY 不寫在程式裡
# 使用 Streamlit Secrets:
# GEMINI_API_KEY = "你的 API KEY"
# =====================================================================

import os
import io
import re
import json
import base64
from pathlib import Path
from datetime import datetime

import streamlit as st
from PIL import Image


# =====================================================================
# 0. APP 基本設定
# =====================================================================

APP_NAME = "黑金剛 AI 多 AI 電商總控中心 PRO"
APP_VERSION = "5.0"

DATA_DIR = Path("data")
HISTORY_DIR = DATA_DIR / "history"

DATA_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================================
# 1. CSS
# =====================================================================

st.markdown(
    """
<style>

.main {
    background-color: #090909;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top right, rgba(255,190,60,0.08), transparent 30%),
        radial-gradient(circle at bottom left, rgba(120,80,20,0.08), transparent 30%),
        #090909;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111111, #080808);
    border-right: 1px solid #292929;
}

h1, h2, h3 {
    color: #f4f4f4;
}

.gold-title {
    color: #d9a441;
    font-weight: 800;
    letter-spacing: 1px;
}

.black-card {
    background: linear-gradient(145deg, #161616, #0d0d0d);
    border: 1px solid #292929;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.status-ok {
    background: rgba(20,120,60,0.15);
    border: 1px solid rgba(50,180,100,0.35);
    padding: 12px;
    border-radius: 12px;
}

.status-warn {
    background: rgba(180,130,20,0.12);
    border: 1px solid rgba(220,170,50,0.35);
    padding: 12px;
    border-radius: 12px;
}

.status-danger {
    background: rgba(180,30,30,0.12);
    border: 1px solid rgba(230,60,60,0.35);
    padding: 12px;
    border-radius: 12px;
}

.small-gray {
    color: #999;
    font-size: 13px;
}

.result-box {
    background: #111;
    border: 1px solid #2d2d2d;
    border-radius: 14px;
    padding: 16px;
    margin-top: 10px;
}

</style>
""",
    unsafe_allow_html=True,
)


# =====================================================================
# 2. Session State
# =====================================================================

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_product" not in st.session_state:
    st.session_state.last_product = {}

if "history" not in st.session_state:
    st.session_state.history = []


# =====================================================================
# 3. Gemini API
# =====================================================================

try:
    from google import genai
except ImportError:
    genai = None


GEMINI_MODEL = "gemini-3.8-flash"


def get_api_key():
    """
    優先使用 Streamlit Secrets
    其次使用環境變數
    """

    key = ""

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


def gemini_available():
    return get_gemini_client() is not None


# =====================================================================
# 4. Gemini 文字 + 圖片分析
# =====================================================================

def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


def detect_mime_type(uploaded_file):
    mime = getattr(uploaded_file, "type", None)

    if mime:
        return mime

    name = getattr(uploaded_file, "name", "").lower()

    if name.endswith(".png"):
        return "image/png"

    if name.endswith(".webp"):
        return "image/webp"

    return "image/jpeg"


def call_gemini_with_image(prompt, image_bytes, mime_type="image/jpeg"):
    """
    Gemini Interactions API
    商品圖片 + Prompt
    """

    client = get_gemini_client()

    if client is None:
        raise RuntimeError(
            "尚未設定 GEMINI_API_KEY，請到 Streamlit Secrets 設定 API 金鑰。"
        )

    image_b64 = image_to_base64(image_bytes)

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=[
            {
                "type": "text",
                "text": prompt,
            },
            {
                "type": "image",
                "data": image_b64,
                "mime_type": mime_type,
            },
        ],
    )

    text = getattr(interaction, "output_text", None)

    if not text:
        text = str(interaction)

    return text


def call_gemini_text(prompt):
    """
    Gemini 純文字 API
    """

    client = get_gemini_client()

    if client is None:
        raise RuntimeError(
            "尚未設定 GEMINI_API_KEY，請到 Streamlit Secrets 設定 API 金鑰。"
        )

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
    )

    text = getattr(interaction, "output_text", None)

    if not text:
        text = str(interaction)

    return text


# =====================================================================
# 5. 商品分類
# =====================================================================

CATEGORY_OPTIONS = [
    "自動辨識",
    "食品飲料",
    "服飾鞋包",
    "美妝保養",
    "3C電子",
    "家電",
    "居家生活",
    "家具收納",
    "母嬰用品",
    "寵物用品",
    "汽機車用品",
    "戶外運動",
    "旅行用品",
    "文具辦公",
    "食品保健",
    "五金工具",
    "玩具遊戲",
    "日用品",
    "其他",
]


# =====================================================================
# 6. 輸出項目
# =====================================================================

OUTPUT_OPTIONS = [
    "商品 AI 視覺分析",
    "商品核心賣點",
    "蝦皮 SEO 標題",
    "蝦皮商品描述",
    "TikTok 短影音腳本",
    "TikTok 影片分鏡",
    "即夢 AI 2.5 生圖指令",
    "即夢 AI 2.5 影片指令",
    "Seedance 2.0 影片指令",
    "KIVA 英文影片指令",
    "IG 文案",
    "Threads 文案",
    "蝦皮分潤導購文案",
    "商品介紹圖文字",
    "合規風險檢查",
]


# =====================================================================
# 7. 風格選項
# =====================================================================

STYLE_OPTIONS = [
    "高級電商廣告",
    "黑金科技",
    "極簡高級",
    "生活感開箱",
    "爆款短影音",
    "實用教學",
    "商品功能展示",
    "情境式廣告",
    "電影感 Cinematic",
    "自然真實",
    "社群種草",
    "品牌質感",
]


TONE_OPTIONS = [
    "專業",
    "自然",
    "年輕活潑",
    "Z世代",
    "高級質感",
    "真實推薦",
    "理性分析",
    "強導購",
]


PLATFORM_OPTIONS = [
    "蝦皮",
    "TikTok",
    "Instagram",
    "Threads",
    "蝦皮分潤",
]


DURATION_OPTIONS = [
    "15 秒",
    "30 秒",
    "45 秒",
    "60 秒",
]


RATIO_OPTIONS = [
    "9:16",
    "1:1",
    "4:5",
    "16:9",
]


CTA_OPTIONS = [
    "蝦皮商品頁",
    "蝦皮分潤連結",
    "TikTok 個人頁",
    "Instagram",
    "Threads",
    "不放 CTA",
]


# =====================================================================
# 8. Gemini 商品分析 Prompt
# =====================================================================

def build_master_prompt(
    product_name,
    category,
    price,
    cost,
    commission,
    monthly_sales,
    rating,
    product_link,
    specs,
    outputs,
    style,
    tone,
    platforms,
    duration,
    ratio,
    cta,
):
    product_info = f"""
商品名稱：{product_name or "未提供"}
商品分類：{category}
商品價格：{price or "未提供"}
商品成本：{cost or "未提供"}
分潤比例：{commission or "未提供"}
月銷量：{monthly_sales or "未提供"}
商品評分：{rating or "未提供"}
商品連結：{product_link or "未提供"}
商品規格：{specs or "未提供"}
"""

    output_list = "\n".join([f"- {x}" for x in outputs])
    platform_list = "、".join(platforms)

    prompt = f"""
你現在是「黑金剛 AI 多 AI 電商總控中心 PRO」的核心商品分析 Agent。

你的工作不是憑空創造商品資料。

【最重要規則】
1. 上傳商品圖片是商品外觀的唯一視覺依據。
2. 不得擅自修改、替換、重畫商品。
3. 不得虛構品牌、材質、規格、功能、認證、產地、效果。
4. 圖片無法確認的資料必須寫「無法由圖片確認」。
5. 使用者提供的商品資料與圖片衝突時，必須標記「資料衝突，待確認」。
6. 不得自動宣稱「100%純棉」「官方正品」「醫療效果」「快速瘦身」等未被證實的內容。
7. 不得製造虛假評論、虛假使用者心得或虛假銷售數字。
8. 如果商品圖片出現第三方品牌、角色、Logo、人物、商標，必須提醒可能涉及授權/IP 問題。
9. 如果要產生 AI 圖片或影片 Prompt，必須要求商品外觀保持一致。
10. AI 生成影片若用於蝦皮等平台，使用者應依平台最新規則正確標示 AI 生成內容。
11. 所有文案以「可驗證資訊」為優先。
12. 不得把推測寫成事實。

【商品資料】
{product_info}

【行銷設定】
平台：{platform_list}
影片風格：{style}
語氣：{tone}
影片長度：{duration}
畫面比例：{ratio}
CTA：{cta}

【要求輸出】
{output_list}

請用繁體中文。

如果要求英文 Prompt：
Prompt 主體使用英文。
必要的控制規則可以使用英文。
不要自行加入不存在的商品資訊。

請按照以下結構輸出：

========================
A. 商品真實資訊分析
========================

商品：
分類：
圖片中可以確認：
圖片中無法確認：
可能衝突：
IP/品牌風險：

========================
B. 商品核心賣點
========================

列出 3～7 個。
每一個都必須建立在圖片或使用者提供資料上。

========================
C. 商品行銷定位
========================

目標客群：
使用情境：
內容主軸：
避免使用的宣稱：

========================
D. 蝦皮 SEO 標題
========================

提供 3 個版本。

========================
E. 蝦皮商品描述
========================

使用清楚的段落。
不要虛構規格。

========================
F. TikTok 短影音腳本
========================

依照指定秒數。
必須包含：
0～3 秒 Hook
商品展示
核心價值
使用情境
CTA

不能只是連續圖片縮放。
必須有清楚的內容主題與商品價值。

========================
G. TikTok 分鏡
========================

Scene 1
Scene 2
Scene 3
Scene 4
Scene 5
Scene 6

每個 Scene 說明：
畫面
鏡頭
商品狀態
字幕
旁白

========================
H. 即夢 AI 2.5 生圖指令
========================

英文 Prompt。
商品必須保持：
shape
color
logo
packaging
text
material
proportion

禁止：
people
hands
extra products
fake logos
fake text
watermark
product deformation

========================
I. 即夢 AI 2.5 影片指令
========================

英文 Prompt。
必須是 image-to-video 思維。

原商品照片是唯一商品來源。
商品不可變形。
不可新增商品。
不可改 Logo。
不可改文字。
不可改顏色。

影片必須具有：
camera movement
product demonstration
clear visual purpose
commercial composition
stable product identity

========================
J. Seedance 2.0 影片指令
========================

英文 Prompt。
同樣遵守商品一致性。

========================
K. KIVA 英文影片指令
========================

英文 Prompt。
適合商品短影音生成。

========================
L. 社群文案
========================

IG：
Threads：

========================
M. 蝦皮分潤導購
========================

不要虛構折扣。
不要虛構優惠。
不要虛構庫存。
如果沒有真實連結，只顯示「請放入你的蝦皮分潤連結」。

========================
N. 商品介紹圖文字
========================

只使用可驗證賣點。

========================
O. 合規風險檢查
========================

輸出：

🟢 可直接使用
🟡 建議確認
🔴 高風險

並列出原因。

========================
P. 最終 AI 商品一致性檢查
========================

商品外觀：
品牌：
文字：
顏色：
規格：
宣稱：
IP：
平台風險：

最後給出：
「通過」
或
「需要人工確認」

不要保證 100% 通過任何平台審核。
"""

    return prompt


# =====================================================================
# 9. 本地快速合規檢查
# =====================================================================

RISK_WORDS = [
    "保證",
    "100%",
    "絕對",
    "最強",
    "第一",
    "永久",
    "零風險",
    "治療",
    "治癒",
    "減肥",
    "瘦身",
    "醫療",
    "藥效",
    "官方正品",
    "正品
