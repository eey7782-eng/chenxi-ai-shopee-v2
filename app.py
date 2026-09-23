# ============================================================
# 黑金鋼 AI 商業自動化總控台 PRO
# VERSION 10.0
#
# 圖片穩定版
#
# 功能：
# 1. AVIF / HEIC / HEIF / JPG / JPEG / PNG / WEBP
# 2. 多圖上傳
# 3. 自動格式轉換
# 4. EXIF 自動旋轉
# 5. 圖片壓縮
# 6. 蝦皮 1:1 商品圖片處理
# 7. 最多 9 張蝦皮商品圖片
# 8. AI 商品圖片辨識
# 9. AI 商品名稱 / 分類 / 賣點
# 10. 蝦皮文案
# 11. Hashtag
# 12. 即夢 AI Prompt
# 13. 小云雀音訊指令
# 14. TikTok 短劇
# 15. 歷史紀錄
# 16. 買家導購前台
#
# API Key：
# 不寫死在程式碼
# 使用者可以：
# - 側邊欄輸入 Groq API Key
# - Streamlit Secrets
# - 環境變數 GROQ_API_KEY
# ============================================================

import io
import os
import re
import json
import base64
import zipfile
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

# ============================================================
# 0. 第三方圖片格式支援
# ============================================================

# AVIF
try:
    import pillow_avif
except Exception:
    pillow_avif = None

# HEIC / HEIF
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass


# ============================================================
# 1. APP 基本設定
# ============================================================

APP_NAME = "黑金鋼 AI 商業自動化總控台 PRO"
APP_VERSION = "10.0"

DATA_DIR = Path("data")
HISTORY_DIR = DATA_DIR / "history"
EXPORT_DIR = DATA_DIR / "exports"

DATA_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CSS
# ============================================================

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

.info-card {
    background: #FFF7ED;
    border: 1px solid #FED7AA;
    border-radius: 12px;
    padding: 18px;
    margin: 12px 0;
}

.success-card {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 12px;
    padding: 18px;
}

.small-text {
    color: #6B7280;
    font-size: 14px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 3. Session State
# ============================================================

DEFAULT_STATE = {
    "auto_name": "",
    "auto_category": "其他",
    "auto_price": "399",
    "auto_selling_points": "",
    "product_link": "",
    "processed_image": None,
    "processed_images_list": [],
    "original_names": [],
    "image_metadata": [],
    "shopee_images": [],
    "last_result": None,
    "ai_analysis": None,
    "groq_key": "",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# 4. API Key 管理
# ============================================================

def get_saved_api_key():
    """
    優先順序：

    1. Session State
    2. Streamlit Secrets
    3. 環境變數

    絕不把 API Key 寫死。
    """

    session_key = st.session_state.get("groq_key", "").strip()

    if session_key:
        return session_key

    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
        if secret_key:
            return str(secret_key).strip()
    except Exception:
        pass

    env_key = os.environ.get("GROQ_API_KEY", "").strip()

    return env_key


# ============================================================
# 5. 圖片工具
# ============================================================

SUPPORTED_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "webp",
    "heic",
    "heif",
    "avif",
]


def safe_filename(name):
    """
    清理檔名
    """

    name = Path(name).stem

    name = re.sub(
        r"[^a-zA-Z0-9_\-\u4e00-\u9fff]",
        "_",
        name
    )

    name = name.strip("_")

    if not name:
        name = "product"

    return name[:50]


def load_image_from_bytes(image_bytes):
    """
    將任意支援格式載入 PIL。
    """

    image = Image.open(io.BytesIO(image_bytes))

    # 強制載入
    image.load()

    # 自動處理手機照片 EXIF 方向
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    # 統一 RGB
    if image.mode != "RGB":
        image = image.convert("RGB")

    return image


def resize_keep_ratio(image, max_side=1800):
    """
    保持比例縮放。
    """

    image = image.copy()

    width, height = image.size

    if max(width, height) <= max_side:
        return image

    scale = max_side / max(width, height)

    new_size = (
        max(1, int(width * scale)),
        max(1, int(height * scale))
    )

    return image.resize(
        new_size,
        Image.Resampling.LANCZOS
    )


def image_to_jpeg_bytes(
    image,
    quality=88,
    max_side=1800
):
    """
    將圖片轉成 JPEG bytes。
    """

    image = resize_keep_ratio(
        image,
        max_side=max_side
    )

    if image.mode != "RGB":
        image = image.convert("RGB")

    output = io.BytesIO()

    image.save(
        output,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True
    )

    return output.getvalue()


def make_shopee_square(
    image,
    size=1024,
    background=(255, 255, 255),
    padding_ratio=0.90
):
    """
    製作蝦皮 1:1 商品圖片。

    不強制裁切商品。
    保持比例縮放後置中。
    """

    image = image.copy()

    if image.mode != "RGB":
        image = image.convert("RGB")

    # 自動 EXIF
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    # 正方形畫布
    canvas = Image.new(
        "RGB",
        (size, size),
        background
    )

    # 商品最大顯示尺寸
    max_product_size = int(size * padding_ratio)

    width, height = image.size

    scale = min(
        max_product_size / width,
        max_product_size / height
    )

    new_width = max(
        1,
        int(width * scale)
    )

    new_height = max(
        1,
        int(height * scale)
    )

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    x = (size - new_width) // 2
    y = (size - new_height) // 2

    canvas.paste(
        image,
        (x, y)
    )

    return canvas


def build_shopee_jpeg(
    image,
    size=1024,
    quality=88
):
    """
    轉成蝦皮商品圖片 JPEG。
    """

    square = make_shopee_square(
        image,
        size=size
    )

    return image_to_jpeg_bytes(
        square,
        quality=quality,
        max_side=size
    )


def get_image_info(image):
    """
    圖片資訊。
    """

    width, height = image.size

    return {
        "width": width,
        "height": height,
        "ratio": round(width / height, 4) if height else 0,
        "mode": image.mode,
    }


# ============================================================
# 6. 多圖處理
# ============================================================

def process_uploaded_images(uploaded_files):
    """
    將使用者上傳的圖片全部轉成穩定 RGB JPEG。
    """

    processed = []
    names = []
    metadata = []

    for uploaded_file in uploaded_files:

        try:

            raw_bytes = uploaded_file.getvalue()

            image = load_image_from_bytes(
                raw_bytes
            )

            original_info = get_image_info(
                image
            )

            # 一般工作區圖片
            jpeg_bytes = image_to_jpeg_bytes(
                image,
                quality=90,
                max_side=1800
            )

            final_image = load_image_from_bytes(
                jpeg_bytes
            )

            processed.append(
                final_image
            )

            names.append(
                uploaded_file.name
            )

            metadata.append(
                {
                    "original_name": uploaded_file.name,
                    "original_size_bytes": len(raw_bytes),
                    "original_width": original_info["width"],
                    "original_height": original_info["height"],
                    "final_size_bytes": len(jpeg_bytes),
                    "final_width": final_image.size[0],
                    "final_height": final_image.size[1],
                    "format": "JPEG",
                }
            )

        except Exception as e:

            st.error(
                f"❌ 圖片「{uploaded_file.name}」處理失敗\n\n"
                f"{str(e)}"
            )

    return processed, names, metadata


# ============================================================
# 7. 建立蝦皮圖片
# ============================================================

def create_all_shopee_images(
    images,
    max_images=9,
    size=1024,
    quality=88
):

    results = []

    for index, image in enumerate(
        images[:max_images]
    ):

        try:

            jpeg_bytes = build_shopee_jpeg(
                image,
                size=size,
                quality=quality
            )

            results.append(
                {
                    "index": index + 1,
                    "bytes": jpeg_bytes,
                    "image": load_image_from_bytes(
                        jpeg_bytes
                    ),
                    "filename": (
                        f"shopee_product_"
                        f"{index + 1:02d}.jpg"
                    ),
                    "size_bytes": len(jpeg_bytes),
                }
            )

        except Exception as e:

            st.warning(
                f"⚠️ 第 {index + 1} 張圖片轉換失敗：{e}"
            )

    return results


# ============================================================
# 8. ZIP
# ============================================================

def create_zip_from_shopee_images(
    shopee_images
):

    output = io.BytesIO()

    with zipfile.ZipFile(
        output,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        for item in shopee_images:

            zip_file.writestr(
                item["filename"],
                item["bytes"]
            )

    output.seek(0)

    return output.getvalue()


# ============================================================
# 9. Base64
# ============================================================

def image_to_data_url(image):
    """
    PIL Image → data URL
    """

    jpeg_bytes = image_to_jpeg_bytes(
        image,
        quality=88,
        max_side=1800
    )

    encoded = base64.b64encode(
        jpeg_bytes
    ).decode("utf-8")

    return (
        "data:image/jpeg;base64,"
        + encoded
    )


# ============================================================
# 10. Groq Client
# ============================================================

def get_groq_client():

    api_key = get_saved_api_key()

    if not api_key:
        return None

    try:

        from groq import Groq

        return Groq(
            api_key=api_key
        )

    except Exception:
        return None


# ============================================================
# 11. AI 商品圖片辨識
# ============================================================

def ai_analyze_product_images(images):

    client = get_groq_client()

    if client is None:

        return {
            "success": False,
            "error": (
                "尚未設定 Groq API Key。"
                "請在左側 AI API 設定輸入 API Key。"
            )
        }

    # Groq Vision 單次最多 3 張
    selected_images = images[:3]

    content = [
        {
            "type": "text",
            "text": """
你是「黑金鋼 AI 商品視覺分析代理」。

請只根據商品照片中「實際看得到」的資訊分析。

非常重要：

1. 不可以幻想商品不存在的規格。
2. 不可以自行捏造品牌。
3. 不可以自行捏造材質。
4. 不可以自行捏造容量。
5. 不可以自行捏造尺寸。
6. 不可以自行捏造功能。
7. 不可以自行捏造認證。
8. 不可以自行捏造功效。
9. 如果照片無法確認，請寫：
   「無法由圖片確認，待確認」
10. 如果有品牌文字，只能按照照片中看到的文字。
11. 如果有產品文字，盡量忠實辨識。
12. 多張照片如果是同一商品，請合併分析。
13. 不要因為商品外觀而自行增加不存在的功能。

請輸出 JSON：

{
  "product_name": "",
  "category": "",
  "brand": "",
  "visible_text": [],
  "colors": [],
  "materials": [],
  "visible_features": [],
  "confirmed_specifications": [],
  "uncertain_items": [],
  "selling_points_based_on_image": [],
  "image_quality_notes": "",
  "main_product_description": ""
}

請只輸出 JSON。
"""
        }
    ]

    for image in selected_images:

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": image_to_data_url(image)
                }
            }
        )

    try:

        completion = client.chat.completions.create(

            model="qwen/qwen3.8-27b",

            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],

            temperature=0.2,

            max_completion_tokens=1800,

            response_format={
                "type": "json_object"
            }
        )

        raw = (
            completion
            .choices[0]
            .message
            .content
        )

        data = json.loads(raw)

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# 12. AI 行銷內容生成
# ============================================================

def call_ai_generation(
    product_name="質感商品",
    category="其他",
    price="399",
    points="",
    analysis=None
):

    client = get_groq_client()

    analysis_text = ""

    if analysis:

        try:
            analysis_text = json.dumps(
                analysis,
                ensure_ascii=False,
                indent=2
            )
        except Exception:
            analysis_text = str(
                analysis
            )

    prompt = f"""
你是「黑金鋼 AI 商業自動化總控台」的電商內容代理。

商品名稱：
{product_name}

商品分類：
{category}

售價：
NT$ {price}

使用者提供的核心賣點：
{points}

AI 商品圖片分析：
{analysis_text}

請建立完整商品行銷素材。

重要規則：

1. 不可以捏造圖片沒有確認的規格。
2. 不可以捏造品牌。
3. 不可以捏造材質。
4. 不可以捏造功效。
5. 不可以捏造認證。
6. 不可以宣稱圖片無法確認的資訊。
7. 不確定資訊請寫「待確認」。
8. 文案要適合台灣電商。
9. 不要使用誇張到無法證實的醫療或功效宣稱。

請輸出：

【🛒 蝦皮商品標題】

【📝 蝦皮商品描述】

【🔥 商品核心賣點】

【🏷️ Hashtag】
提供 5～10 個。

【🎨 即夢 AI 圖片 Prompt】
英文。
商業攝影。
商品本體保持真實。
不要改變商品外觀。
不要增加不存在的產品。
不要人物。
不要手。
不要代言人。
不要浮水印。
9:16。

【🎬 即夢 AI 影片指令】
6～15 秒。
需要有商品展示、使用情境、畫面價值。
不能只有單純 Zoom。
商品外觀保持一致。
不要憑空增加功能。

【🎵 小云雀音訊指令】
包含：
音樂風格
節奏
音效
旁白風格

【📱 TikTok 30 秒短劇】

0-3 秒：
黃金鉤子

3-10 秒：
問題／衝突

10-20 秒：
商品出場與使用

20-26 秒：
商品特色

26-30 秒：
自然導購 CTA

請避免虛假承諾。
"""

    if client is None:

        return f"""
【🛒 蝦皮商品標題】
{product_name}｜{points[:60]}

【📝 蝦皮商品描述】
{product_name}
商品分類：{category}
售價：NT$ {price}

{points}

※ 商品規格與實際內容請以商品實物及賣場資訊為準。

【🔥 商品核心賣點】
{points}

【🏷️ Hashtag】
#好物推薦
#電商好物
#蝦皮購物
#生活好物
#商品分享

【🎨 即夢 AI 圖片 Prompt】
Commercial product photography of {product_name},
premium e-commerce advertising scene,
realistic product appearance,
clean composition,
professional studio lighting,
cinematic lighting,
high detail,
vertical 9:16,
no people,
no hands,
no watermark,
no extra products,
preserve the original product design.

【🎬 即夢 AI 影片指令】
9:16 vertical commercial product video.
Start with a clear product reveal.
Show the real product in a useful everyday context.
Use a gentle camera push-in and subtle camera movement.
Show the product clearly for most of the video.
Preserve the original appearance.
No people, no hands, no extra products,
no deformation, no melting, no flickering,
no watermark.

【🎵 小云雀音訊指令】
Upbeat commercial background music,
clean modern rhythm,
positive shopping atmosphere,
friendly natural voiceover.

【📱 TikTok 30 秒短劇】

0-3 秒：
「等等，這個商品真的很值得看看！」

3-10 秒：
先提出日常使用上的問題。

10-20 秒：
商品出場並展示實際使用情境。

20-26 秒：
整理商品已確認的特色。

26-30 秒：
「想了解商品資訊，可以點進商品頁看看。」
"""

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,

            max_completion_tokens=3000
        )

        return (
            completion
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return (
            "AI 內容生成失敗。\n\n"
            f"錯誤：{e}"
        )


# ============================================================
# 13. 歷史紀錄
# ============================================================

def save_history_record(
    name,
    category,
    price,
    points,
    result_text,
    ai_analysis=None
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    safe_name = safe_filename(
        name
    )

    filename = (
        HISTORY_DIR
        / f"{timestamp}_{safe_name}.json"
    )

    record = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "name": name,
        "category": category,
        "price": price,
        "points": points,
        "result_text": result_text,
        "ai_analysis": ai_analysis,
    }

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            record,
            f,
            ensure_ascii=False,
            indent=2
        )


def load_all_histories():

    records = []

    files = sorted(
        HISTORY_DIR.glob("*.json"),
        reverse=True
    )

    for file in files:

        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                records.append(
                    (
                        file.name,
                        json.load(f)
                    )
                )

        except Exception:
            pass

    return records


# ============================================================
# 14. 側邊欄
# ============================================================

st.sidebar.title("⚡ 黑金鋼控制台")

mode = st.sidebar.radio(
    "選擇功能模式",
    [
        "🚀 一鍵全自動生成",
        "🖼️ 蝦皮圖片處理中心",
        "🛍️ 買家導購前台",
        "📜 歷史紀錄"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader(
    "🔐 AI API 設定"
)

saved_key = get_saved_api_key()

api_key_input = st.sidebar.text_input(
    "Groq API Key",
    value=(
        st.session_state.groq_key
        if st.session_state.groq_key
        else saved_key
    ),
    type="password",
    help="API Key 不會寫入歷史紀錄。"
)

if api_key_input:
    st.session_state.groq_key = (
        api_key_input.strip()
    )

if get_saved_api_key():

    st.sidebar.success(
        "🟢 AI API 已設定"
    )

else:

    st.sidebar.warning(
        "🟡 尚未設定 AI API"
    )

st.sidebar.caption(
    "API Key 不會硬寫在 app.py。"
)


# ============================================================
# 15. 歷史紀錄側邊欄
# ============================================================

histories = load_all_histories()

if histories:

    st.sidebar.markdown("---")
    st.sidebar.subheader(
        "📜 最近歷史紀錄"
    )

    history_options = {
        f"{data.get('timestamp', '')} - "
        f"{data.get('name', '商品')}":
        fname

        for fname, data in histories[:30]
    }

    selected_label = st.sidebar.selectbox(
        "選擇紀錄",
        ["-- 請選擇 --"]
        + list(history_options.keys())
    )

    if selected_label != "-- 請選擇 --":

        target_file = (
            HISTORY_DIR
            / history_options[selected_label]
        )

        if target_file.exists():

            if st.sidebar.button(
                "📂 載入此筆紀錄",
                use_container_width=True
            ):

                try:

                    with open(
                        target_file,
                        "r
