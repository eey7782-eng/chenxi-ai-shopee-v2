
import io
import json
import os
import re
import zipfile
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

# ============================================================
# 黑金鋼 AI 商業自動化總控台 PRO
# v10.0 圖片穩定版
#
# 核心：
# 1. AVIF / HEIC / HEIF / JPG / PNG / WEBP 自動轉 JPEG
# 2. 多圖上傳
# 3. 圖片自動旋轉 / RGB 標準化 / 壓縮
# 4. 蝦皮圖片輸出包
# 5. Groq Vision AI 商品辨識（API Key 不寫死）
# 6. 文案 / Hashtag / 即夢 / 小云雀 / TikTok 短劇
# 7. 歷史紀錄
# ============================================================

APP_NAME = "黑金鋼 AI 商業自動化總控台 PRO"
APP_VERSION = "10.0.1"

DATA_DIR = Path("data")
HISTORY_DIR = DATA_DIR / "history"
EXPORT_DIR = DATA_DIR / "exports"
DATA_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

# ============================================================
# 可調整圖片參數
# ============================================================

MAX_UPLOAD_MB = 30
SHOPEE_MAX_SIDE = 2000
SHOPEE_QUALITY = 90
SHOPEE_MAX_BYTES = 5 * 1024 * 1024
AI_MAX_SIDE = 1600
AI_MAX_BYTES = 4 * 1024 * 1024

CATEGORIES = [
    "服飾鞋包",
    "3C電子",
    "居家生活",
    "美妝保養",
    "食品飲料",
    "母嬰用品",
    "汽機車用品",
    "運動戶外",
    "寵物用品",
    "其他",
]

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 圖片格式插件
# ============================================================

AVIF_READY = False
HEIF_READY = False

try:
    import pillow_avif  # noqa: F401
    AVIF_READY = True
except Exception:
    pass

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_READY = True
except Exception:
    pass

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
.main { background-color: #FFFFFF; }
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
.ok-box {
    padding: 12px 16px;
    border-radius: 10px;
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
}
.warn-box {
    padding: 12px 16px;
    border-radius: 10px;
    background: #FFFBEB;
    border: 1px solid #FDE68A;
}
.info-box {
    padding: 12px 16px;
    border-radius: 10px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
}
.small-muted {
    color: #6B7280;
    font-size: 13px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# Session State
# ============================================================

DEFAULTS = {
    "auto_name": "",
    "auto_category": "其他",
    "auto_price": "399",
    "auto_selling_points": "",
    "product_link": "https://s.shopee.tw/your_link",
    "last_result": None,
    "processed_image": None,
    "processed_images_list": [],
    "processed_meta": [],
    "ai_analysis": None,
    "image_errors": [],
    "shopee_zip_bytes": None,
    "shopee_files": [],
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# 工具函式：安全檔名
# ============================================================

def safe_filename(name: str, default="product") -> str:
    name = str(name or "").strip()
    name = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "_", name)
    name = re.sub(r"\s+", "_", name)
    return name[:60] or default


# ============================================================
# 圖片處理
# ============================================================

def flatten_to_rgb(image: Image.Image) -> Image.Image:
    """處理 RGBA / LA / P / 透明背景，最後統一 RGB。"""
    image = ImageOps.exif_transpose(image)

    if image.mode in ("RGBA", "LA"):
        rgba = image.convert("RGBA")
        background = Image.new("RGB", rgba.size, "white")
        background.paste(rgba, mask=rgba.getchannel("A"))
        return background

    if image.mode == "P":
        if "transparency" in image.info:
            rgba = image.convert("RGBA")
            background = Image.new("RGB", rgba.size, "white")
            background.paste(rgba, mask=rgba.getchannel("A"))
            return background
        return image.convert("RGB")

    if image.mode != "RGB":
        return image.convert("RGB")

    return image


def resize_keep_ratio(image: Image.Image, max_side: int) -> Image.Image:
    image = image.copy()
    width, height = image.size

    if max(width, height) <= max_side:
        return image

    scale = max_side / float(max(width, height))
    new_size = (
        max(1, int(width * scale)),
        max(1, int(height * scale)),
    )

    return image.resize(new_size, Image.Resampling.LANCZOS)


def encode_jpeg_under_limit(
    image: Image.Image,
    max_side: int,
    quality: int = 90,
    max_bytes: int = 5 * 1024 * 1024,
):
    """
    將圖片輸出成 RGB JPEG。
    若超過大小，逐步降低品質，最後縮小尺寸。
    """
    image = flatten_to_rgb(image)
    image = resize_keep_ratio(image, max_side)

    current_quality = int(quality)

    while True:
        buffer = io.BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=current_quality,
            optimize=True,
            progressive=True,
        )

        data = buffer.getvalue()

        if len(data) <= max_bytes:
            return image, data, current_quality

        if current_quality > 60:
            current_quality -= 5
            continue

        current_width, current_height = image.size
        next_width = int(current_width * 0.85)
        next_height = int(current_height * 0.85)

        if next_width < 320 or next_height < 320:
            return image, data, current_quality

        image = image.resize(
            (next_width, next_height),
            Image.Resampling.LANCZOS,
        )


def process_uploaded_image(uploaded_file):
    """
    後端真正收到檔案後才辨識格式；副檔名/MIME 不作為唯一依據。
    任何支援格式先讀入，再統一輸出成 RGB JPEG。
    """
    raw = uploaded_file.getvalue()

    if not raw:
        raise ValueError("收到的是空檔案。請重新從相簿選取照片。")

    if len(raw) > MAX_UPLOAD_MB * 1024 * 1024:
        raise ValueError(
            f"原始檔案超過 {MAX_UPLOAD_MB} MB，請先縮小照片後再上傳。"
        )

    try:
        image = Image.open(io.BytesIO(raw))
        image.verify()
    except Exception as first_error:
        # verify() 後需要重新開啟；部分格式的 plugin 對 verify 支援不同，
        # 因此再以正常 decode 嘗試一次。
        try:
            image = Image.open(io.BytesIO(raw))
            image.load()
        except Exception as second_error:
            suffix = Path(uploaded_file.name).suffix.lower() or "（無副檔名）"
            raise ValueError(
                f"後端無法解碼此檔案 {suffix}。"
                "若是 AVIF/HEIC，請確認 requirements.txt 已安裝 "
                "pillow-avif-plugin 與 pillow-heif。"
                f" 第一個錯誤：{first_error}；第二個錯誤：{second_error}"
            )
    else:
        # verify() 成功後重新開啟，確保後續 convert/save 有完整像素資料。
        image = Image.open(io.BytesIO(raw))
        image.load()

    original_format = (
        image.format
        or Path(uploaded_file.name).suffix.replace(".", "").upper()
        or "UNKNOWN"
    )
    original_size = image.size

    final_image, jpeg_bytes, quality = encode_jpeg_under_limit(
        image,
        max_side=SHOPEE_MAX_SIDE,
        quality=SHOPEE_QUALITY,
        max_bytes=SHOPEE_MAX_BYTES,
    )

    metadata = {
        "original_name": uploaded_file.name,
        "original_format": str(original_format).upper(),
        "original_width": original_size[0],
        "original_height": original_size[1],
        "final_width": final_image.size[0],
        "final_height": final_image.size[1],
        "final_bytes": len(jpeg_bytes),
        "final_quality": quality,
        "output_format": "JPEG",
    }

    return final_image, jpeg_bytes, metadata


def make_ai_image_bytes(image: Image.Image):
    """產生給 Vision API 使用的較小 JPEG，降低 API 圖片成本與失敗率。"""
    _, data, _ = encode_jpeg_under_limit(
        image,
        max_side=AI_MAX_SIDE,
        quality=85,
        max_bytes=AI_MAX_BYTES,
    )
    return data


def format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.2f} MB"


# ============================================================
# 歷史紀錄
# ============================================================

def save_history_record(
    name,
    category,
    price,
    points,
    result_text,
    ai_analysis=None,
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = safe_filename(name, "product")[:30]
    filename = HISTORY_DIR / f"{timestamp}_{safe_name}.json"

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "category": category,
        "price": price,
        "points": points,
        "result_text": result_text,
        "ai_analysis": ai_analysis,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def load_all_histories():
    records = []
    for file in sorted(HISTORY_DIR.glob("*.json"), reverse=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                records.append((file.name, json.load(f)))
        except Exception:
            continue
    return records


# ============================================================
# API Key / Groq Vision
# ============================================================

def get_groq_api_key():
    """優先讀 Streamlit Secrets，再讀環境變數，最後才讀 Session State。"""
    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        secret_key = ""

    if secret_key:
        return str(secret_key).strip()

    env_key = os.environ.get("GROQ_API_KEY", "")
    if env_key:
        return env_key.strip()

    return st.session_state.get("groq_api_key", "").strip()


def extract_json(text: str):
    """容錯解析 AI 回傳的 JSON。"""
    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    return None


def call_groq_vision(images, model="qwen/qwen3.8-27b"):
    """
    使用 Groq Vision 分析最多 3 張商品圖片。
    API Key 不寫死在程式中。
    """
    api_key = get_groq_api_key()

    if not api_key:
        raise RuntimeError(
            "尚未設定 Groq API Key。請到左側「⚙️ AI 設定」輸入 API Key，"
            "或在 Streamlit Secrets 設定 GROQ_API_KEY。"
        )

    try:
        from groq import Groq
    except ImportError:
        raise RuntimeError(
            "尚未安裝 groq 套件，請在 requirements.txt 加入 groq。"
        )

    client = Groq(api_key=api_key)

    content = [
        {
            "type": "text",
            "text": """
你是「黑金鋼 AI 電商商品視覺分析代理」。

請只根據圖片中「實際可看見」的內容分析商品。
禁止自行編造品牌、材質、功能、容量、規格、認證、價格、優惠、
防水、防摔、抗菌、醫療功效等圖片沒有明確證據的資訊。

如果圖片無法確認，請寫：
「無法由圖片確認，待確認」

請特別注意：
1. 商品名稱：根據外觀與可讀文字提出合理名稱
2. 商品分類
3. 品牌：只有圖片能清楚看到才填
4. 顏色
5. 外觀與可見特色
6. 圖片中可讀取的文字
7. 可由圖片支持的賣點
8. 無法確認的資訊
9. 蝦皮商品標題建議
10. TikTok 短影音切入點
11. 即夢 AI 商品畫面描述
12. 分析信心

請只輸出合法 JSON，不要輸出 Markdown。
JSON 格式：

{
  "商品名稱": "",
  "商品分類": "",
  "品牌": "",
  "顏色": "",
  "可見外觀": [],
  "圖片文字": [],
  "可確認賣點": [],
  "無法確認": [],
  "蝦皮標題建議": "",
  "TikTok切入點": "",
  "即夢畫面描述": "",
  "分析信心": "高/中/低"
}
""",
        }
    ]

    for image in images[:3]:
        image_bytes = make_ai_image_bytes(image)
        import base64

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                },
            }
        )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        temperature=0.2,
        max_completion_tokens=1600,
        response_format={"type": "json_object"},
    )

    text = completion.choices[0].message.content or ""
    result = extract_json(text)

    if not result:
        raise RuntimeError("AI 有回應，但無法解析成商品 JSON。")

    return result


def build_fallback_analysis():
    return {
        "商品名稱": "請輸入商品名稱",
        "商品分類": "其他",
        "品牌": "無法由圖片確認，待確認",
        "顏色": "無法由圖片確認，待確認",
        "可見外觀": [],
        "圖片文字": [],
        "可確認賣點": [],
        "無法確認": ["尚未使用 Vision AI 分析"],
        "蝦皮標題建議": "",
        "TikTok切入點": "",
        "即夢畫面描述": "",
        "分析信心": "低",
    }


def apply_ai_analysis(result):
    st.session_state.ai_analysis = result

    name = str(result.get("商品名稱", "")).strip()
    category = str(result.get("商品分類", "")).strip()

    if name and name != "無法由圖片確認，待確認":
        st.session_state.auto_name = name

    if category in CATEGORIES:
        st.session_state.auto_category = category
    else:
        # 粗略分類對應
        category_text = category
        for item in CATEGORIES:
            if item in category_text or category_text in item:
                st.session_state.auto_category = item
                break

    selling_points = result.get("可確認賣點", [])
    if isinstance(selling_points, list):
        selling_points = "、".join(
            str(x).strip() for x in selling_points if str(x).strip()
        )
    else:
        selling_points = str(selling_points or "").strip()

    if selling_points:
        st.session_state.auto_selling_points = selling_points


# ============================================================
# 行銷內容生成
# ============================================================

def call_ai_generation(
    product_name="質感商品",
    price="399",
    points="優質選物",
    category="其他",
    ai_analysis=None,
):
    api_key = get_groq_api_key()

    if not api_key:
        return f"""
【🛒 蝦皮與社群行銷文案】
🔥 精選推薦：{product_name}
💰 售價：NT$ {price}
✨ 商品亮點：{points}

【🏷️ Hashtag】
#好物推薦 #生活好物 #蝦皮好物 #開箱分享 #短影音推薦

【🎨 即夢 AI 畫面生成指令碼】
Premium commercial product photography of {product_name},
category: {category}, clean luxury e-commerce scene,
professional studio lighting, realistic material texture,
product remains visually faithful to the reference image,
no people, no hands, no extra products, no watermark,
vertical 9:16 composition.

【🎵 小云雀 AI 音訊/配樂指令碼】
Style: upbeat commercial pop, modern short-video rhythm,
clean product showcase atmosphere, friendly commercial voiceover.

【🎬 TikTok 30 秒短劇】
[0-3秒]
「等等，這個商品居然可以這樣用？」

[3-12秒]
快速展示商品外觀與使用情境，
把商品真正能確認的特色用畫面呈現。

[12-22秒]
展示使用前後的差異或實際使用場景，
避免加入圖片無法確認的規格與功效。

[22-30秒]
「想知道更多商品資訊，直接點擊商品連結看看。」
"""

    try:
        from groq import Groq

        client = Groq(api_key=api_key)

        visible_info = ""
        if ai_analysis:
            visible_info = json.dumps(
                ai_analysis,
                ensure_ascii=False,
                indent=2,
            )

        prompt = f"""
你是黑金鋼 AI 電商內容生成代理。

商品名稱：{product_name}
分類：{category}
售價：NT${price}
已確認賣點：{points}

商品視覺分析：
{visible_info}

請產出：
1. 蝦皮商品標題
2. 蝦皮商品描述
3. 5 個 Hashtag
4. 即夢 AI 9:16 商品廣告畫面指令
5. 小云雀音訊/配樂指令
6. TikTok 30 秒短影音劇本

規則：
- 不可自行編造圖片沒有確認的商品規格。
- 不可捏造功效、認證、材質、容量、價格優惠。
- 不要加入代言人、人物、手、模特。
- 商品外觀、品牌、Logo、包裝、文字不得任意改變。
- 即夢畫面必須以商品照片為唯一視覺真實依據。
- TikTok 劇情要有前 3 秒鉤子、商品展示、使用情境、價值、CTA。
"""

        completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=2400,
        )

        return completion.choices[0].message.content or ""

    except Exception as e:
        return f"""
【🛒 蝦皮與社群行銷文案】
🔥 精選推薦：{product_name}
💰 售價：NT$ {price}
✨ 商品亮點：{points}

【🏷️ Hashtag】
#好物推薦 #蝦皮好物 #開箱分享 #生活好物 #短影音

【🎨 即夢 AI 畫面生成指令】
Premium commercial product photography of {product_name},
realistic product texture, cinematic lighting,
clean luxury e-commerce background, vertical 9:16,
reference product must remain unchanged,
no people, no hands, no extra products, no watermark.

【🎵 小云雀 AI 音訊/配樂指令碼】
Upbeat modern commercial music, clean rhythm,
friendly e-commerce voiceover.

【🎬 TikTok 30 秒短劇】
[0-3秒] 商品快速特寫＋吸睛問題
[3-12秒] 展示商品外觀與實際使用情境
[12-22秒] 展示已確認的商品特色
[22-30秒] 引導觀眾查看商品連結

API 生成提示：{e}
"""


# ============================================================
# ZIP：蝦皮圖片包
# ============================================================

def create_shopee_zip(images, product_name):
    zip_buffer = io.BytesIO()
    base = safe_filename(product_name, "shopee_product")

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:
        for index, image in enumerate(images, start=1):
            _, data, _ = encode_jpeg_under_limit(
                image,
                max_side=SHOPEE_MAX_SIDE,
                quality=SHOPEE_QUALITY,
                max_bytes=SHOPEE_MAX_BYTES,
            )
            filename = f"{base}_{index:02d}.jpg"
            zf.writestr(filename, data)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# ============================================================
# 側邊欄
# ============================================================

st.sidebar.title("⚡ 黑金鋼控制台")
mode = st.sidebar.radio(
    "選擇功能模式",
    [
        "🚀 一鍵全自動生成總控台",
        "🛍️ 買家極速導購前台",
    ],
)

st.sidebar.markdown("---")

with st.sidebar.expander("⚙️ AI 設定", expanded=True):
    st.caption("API Key 不寫死在 app.py。")

    existing_key = get_groq_api_key()

    api_key_input = st.text_input(
        "Groq API Key",
        value="",
        type="password",
        placeholder="輸入 gsk_... API Key",
        help="也可以使用 Streamlit Secrets：GROQ_API_KEY",
    )

    if api_key_input.strip():
        st.session_state.groq_api_key = api_key_input.strip()

    if existing_key or api_key_input.strip():
        st.success("AI API 已設定")
    else:
        st.warning("尚未設定 AI API")

    st.caption(
        "Vision 模型：qwen/qwen3.8-27b\n"
        "可分析商品圖片並輸出 JSON。"
    )

st.sidebar.markdown("---")

with st.sidebar.expander("🖼️ 圖片處理設定"):
    st.write(f"蝦皮輸出：JPEG / RGB / 最長邊 ≤ {SHOPEE_MAX_SIDE}px")
    st.write(f"單張輸出目標：≤ {format_bytes(SHOPEE_MAX_BYTES)}")
    st.write(f"AI 分析圖片：最長邊 ≤ {AI_MAX_SIDE}px")
    st.write(
        f"AVIF 插件：{'✅' if AVIF_READY else '❌'}"
    )
    st.write(
        f"HEIC 插件：{'✅' if HEIF_READY else '❌'}"
    )

# ============================================================
# 歷史紀錄
# ============================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📜 歷史生成紀錄")

histories = load_all_histories()

if histories:
    history_options = {
        f"{data.get('timestamp', '')} - {data.get('name', '未命名')}": fname
        for fname, data in histories
    }

    selected_label = st.sidebar.selectbox(
        "選擇歷史紀錄",
        ["-- 請選擇紀錄 --"] + list(history_options.keys()),
    )

    if selected_label != "-- 請選擇紀錄 --":
        target_file = HISTORY_DIR / history_options[selected_label]

        if target_file.exists():
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    h_data = json.load(f)

                if st.sidebar.button(
                    "📂 載入此筆歷史紀錄",
                    use_container_width=True,
                ):
                    st.session_state.auto_name = h_data.get("name", "")
                    st.session_state.auto_category = h_data.get(
                        "category",
                        "其他",
    。
    """
    api_key = get_groq_api_key()

    if not api_key:
        raise RuntimeError(
            "尚未設定 Groq API Key。請到左側「⚙️ AI 設定」輸入 API Key，"
            "或在 Streamlit Secrets 設定 GROQ_API_KEY。"
        )

    try:
        from groq import Groq
    except ImportError:
        raise RuntimeError(
            "尚未安裝 groq 套件，請在 requirements.txt 加入 groq。"
        )

    client = Groq(api_key=api_key)

    content = [
        {
            "type": "text",
            "text": """
你是「黑金鋼 AI 電商商品視覺分析代理」。

請只根據圖片中「實際可看見」的內容分析商品。
禁止自行編造品牌、材質、功能、容量、規格、認證、價格、優惠、
防水、防摔、抗菌、醫療功效等圖片沒有明確證據的資訊。

如果圖片無法確認，請寫：
「無法由圖片確認，待確認」

請特別注意：
1. 商品名稱：根據外觀與可讀文字提出合理名稱
2. 商品分類
3. 品牌：只有圖片能清楚看到才填
4. 顏色
5. 外觀與可見特色
6. 圖片中可讀取的文字
7. 可由圖片支持的賣點
8. 無法確認的資訊
9. 蝦皮商品標題建議
10. TikTok 短影音切入點
11. 即夢 AI 商品畫面描述
12. 分析信心

請只輸出合法 JSON，不要輸出 Markdown。
JSON 格式：

{
  "商品名稱": "",
  "商品分類": "",
  "品牌": "",
  "顏色": "",
  "可見外觀": [],
  "圖片文字": [],
  "可確認賣點": [],
  "無法確認": [],
  "蝦皮標題建議": "",
  "TikTok切入點": "",
  "即夢畫面描述": "",
  "分析信心": "高/中/低"
}
""",
        }
    ]

    for image in images[:3]:
        image_bytes = make_ai_image_bytes(image)
        import base64

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                },
            }
        )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        temperature=0.2,
        max_completion_tokens=1600,
        response_format={"type": "json_object"},
    )

    text = completion.choices[0].message.content or ""
    result = extract_json(text)

    if not result:
        raise RuntimeError("AI 有回應，但無法解析成商品 JSON。")

    return result


def build_fallback_analysis():
    return {
        "商品名稱": "請輸入商品名稱",
        "商品分類": "其他",
        "品牌": "無法由圖片確認，待確認",
        "顏色": "無法由圖片確認，待確認",
        "可見外觀": [],
        "圖片文字": [],
        "可確認賣點": [],
        "無法確認": ["尚未使用 Vision AI 分析"],
        "蝦皮標題建議": "",
        "TikTok切入點": "",
        "即夢畫面描述": "",
        "分析信心": "低",
    }


def apply_ai_analysis(result):
    st.session_state.ai_analysis = result

    name = str(result.get("商品名稱", "")).strip()
    category = str(result.get("商品分類", "")).strip()

    if name and name != "無法由圖片確認，待確認":
        st.session_state.auto_name = name

    if category in CATEGORIES:
        st.session_state.auto_category = category
    else:
        # 粗略分類對應
        category_text = category
        for item in CATEGORIES:
            if item in category_text or category_text in item:
                st.session_state.auto_category = item
                break

    selling_points = result.get("可確認賣點", [])
    if isinstance(selling_points, list):
        selling_points = "、".join(
            str(x).strip() for x in selling_points if str(x).strip()
        )
    else:
        selling_points = str(selling_points or "").strip()

    if selling_points:
        st.session_state.auto_selling_points = selling_points


# ============================================================
# 行銷內容生成
# ============================================================

def call_ai_generation(
    product_name="質感商品",
    price="399",
    points="優質選物",
    category="其他",
    ai_analysis=None,
):
    api_key = get_groq_api_key()

    if not api_key:
        return f"""
【🛒 蝦皮與社群行銷文案】
🔥 精選推薦：{product_name}
💰 售價：NT$ {price}
✨ 商品亮點：{points}

【🏷️ Hashtag】
#好物推薦 #生活好物 #蝦皮好物 #開箱分享 #短影音推薦

【🎨 即夢 AI 畫面生成指令碼】
Premium commercial product photography of {product_name},
category: {category}, clean luxury e-commerce scene,
professional studio lighting, realistic material texture,
product remains visually faithful to the reference image,
no people, no hands, no extra products, no watermark,
vertical 9:16 composition.

【🎵 小云雀 AI 音訊/配樂指令碼】
Style: upbeat commercial pop, modern short-video rhythm,
clean product showcase atmosphere, friendly commercial voiceover.

【🎬 TikTok 30 秒短劇】
[0-3秒]
「等等，這個商品居然可以這樣用？」

[3-12秒]
快速展示商品外觀與使用情境，
把商品真正能確認的特色用畫面呈現。

[12-22秒]
展示使用前後的差異或實際使用場景，
避免加入圖片無法確認的規格與功效。

[22-30秒]
「想知道更多商品資訊，直接點擊商品連結看看。」
"""

    try:
        from groq import Groq

        client = Groq(api_key=api_key)

        visible_info = ""
        if ai_analysis:
            visible_info = json.dumps(
                ai_analysis,
                ensure_ascii=False,
                indent=2,
            )

        prompt = f"""
你是黑金鋼 AI 電商內容生成代理。

商品名稱：{product_name}
分類：{category}
售價：NT${price}
已確認賣點：{points}

商品視覺分析：
{visible_info}

請產出：
1. 蝦皮商品標題
2. 蝦皮商品描述
3. 5 個 Hashtag
4. 即夢 AI 9:16 商品廣告畫面指令
5. 小云雀音訊/配樂指令
6. TikTok 30 秒短影音劇本

規則：
- 不可自行編造圖片沒有確認的商品規格。
- 不可捏造功效、認證、材質、容量、價格優惠。
- 不要加入代言人、人物、手、模特。
- 商品外觀、品牌、Logo、包裝、文字不得任意改變。
- 即夢畫面必須以商品照片為唯一視覺真實依據。
- TikTok 劇情要有前 3 秒鉤子、商品展示、使用情境、價值、CTA。
"""

        completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=2400,
        )

        return completion.choices[0].message.content or ""

    except Exception as e:
        return f"""
【🛒 蝦皮與社群行銷文案】
🔥 精選推薦：{product_name}
💰 售價：NT$ {price}
✨ 商品亮點：{points}

【🏷️ Hashtag】
#好物推薦 #蝦皮好物 #開箱分享 #生活好物 #短影音

【🎨 即夢 AI 畫面生成指令】
Premium commercial product photography of {product_name},
realistic product texture, cinematic lighting,
clean luxury e-commerce background, vertical 9:16,
reference product must remain unchanged,
no people, no hands, no extra products, no watermark.

【🎵 小云雀 AI 音訊/配樂指令碼】
Upbeat modern commercial music, clean rhythm,
friendly e-commerce voiceover.

【🎬 TikTok 30 秒短劇】
[0-3秒] 商品快速特寫＋吸睛問題
[3-12秒] 展示商品外觀與實際使用情境
[12-22秒] 展示已確認的商品特色
[22-30秒] 引導觀眾查看商品連結

API 生成提示：{e}
"""


# ============================================================
# ZIP：蝦皮圖片包
# ============================================================

def create_shopee_zip(images, product_name):
    zip_buffer = io.BytesIO()
    base = safe_filename(product_name, "shopee_product")

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:
        for index, image in enumerate(images, start=1):
            _, data, _ = encode_jpeg_under_limit(
                image,
                max_side=SHOPEE_MAX_SIDE,
                quality=SHOPEE_QUALITY,
                max_bytes=SHOPEE_MAX_BYTES,
            )
            filename = f"{base}_{index:02d}.jpg"
            zf.writestr(filename, data)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# ============================================================
# 側邊欄
# ============================================================

st.sidebar.title("⚡ 黑金鋼控制台")
mode = st.sidebar.radio(
    "選擇功能模式",
    [
        "🚀 一鍵全自動生成總控台",
        "🛍️ 買家極速導購前台",
    ],
)

st.sidebar.markdown("---")

with st.sidebar.expander("⚙️ AI 設定", expanded=True):
    st.caption("API Key 不寫死在 app.py。")

    existing_key = get_groq_api_key()

    api_key_input = st.text_input(
        "Groq API Key",
        value="",
        type="password",
        placeholder="輸入 gsk_... API Key",
        help="也可以使用 Streamlit Secrets：GROQ_API_KEY",
    )

    if api_key_input.strip():
        st.session_state.groq_api_key = api_key_input.strip()

    if existing_key or api_key_input.strip():
        st.success("AI API 已設定")
    else:
        st.warning("尚未設定 AI API")

    st.caption(
        "Vision 模型：qwen/qwen3.8-27b\n"
        "可分析商品圖片並輸出 JSON。"
    )

st.sidebar.markdown("---")

with st.sidebar.expander("🖼️ 圖片處理設定"):
    st.write(f"蝦皮輸出：JPEG / RGB / 最長邊 ≤ {SHOPEE_MAX_SIDE}px")
    st.write(f"單張輸出目標：≤ {format_bytes(SHOPEE_MAX_BYTES)}")
    st.write(f"AI 分析圖片：最長邊 ≤ {AI_MAX_SIDE}px")
    st.write(
        f"AVIF 插件：{'✅' if AVIF_READY else '❌'}"
    )
    st.write(
        f"HEIC 插件：{'✅' if HEIF_READY else '❌'}"
    )

# ============================================================
# 歷史紀錄
# ============================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📜 歷史生成紀錄")

histories = load_all_histories()

if histories:
    history_options = {
        f"{data.get('timestamp', '')} - {data.get('name', '未命名')}": fname
        for fname, data in histories
    }

    selected_label = st.sidebar.selectbox(
        "選擇歷史紀錄",
        ["-- 請選擇紀錄 --"] + list(history_options.keys()),
    )

    if selected_label != "-- 請選擇紀錄 --":
        target_file = HISTORY_DIR / history_options[selected_label]

        if target_file.exists():
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    h_data = json.load(f)

                if st.sidebar.button(
                    "📂 載入此筆歷史紀錄",
                    use_container_width=True,
                ):
                    st.session_state.auto_name = h_data.get("name", "")
                    st.session_state.auto_category = h_data.get(
                        "category",
                        "其他",
                    )
                    st.session_state.auto_price = h_data.get(
                        "price",
                        "399",
                    )
                    st.session_state.auto_selling_points = h_data.get(
                        "points",
                        "",
                    )
                    st.session_state.last_result = h_data.get(
                        "result_text",
                        "",
                    )
                    st.session_state.ai_analysis = h_data.get(
                        "ai_analysis"
                    )

                    st.success("🎉 載入成功！")
                    st.rerun()

            except Exception as e:
                st.sidebar.error(f"載入失敗：{e}")
else:
    st.sidebar.caption("尚無歷史紀錄。")


# ========================================
