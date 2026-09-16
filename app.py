# ============================================================
# 10. 商品圖片｜蝦皮上傳圖片規格處理 (支援 AVIF 轉 JPG)
# ============================================================

from PIL import Image, ImageOps
import io
from pathlib import Path
import streamlit as st

# 確保 pillow 支援 avif 格式（部分環境需要 register，若無 pillow-heif 可省略但加上 try/except 保護）
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass


def prepare_shopee_image(uploaded_file, output_size=1000):
    """
    將使用者上傳的商品圖片（支援 JPG, PNG, WEBP, AVIF 等）
    轉換成適合蝦皮商品圖使用的 1:1 標準 JPG 格式。
    """

    raw = uploaded_file.getvalue()
    original = Image.open(io.BytesIO(raw))

    # 修正 EXIF 方向
    original = ImageOps.exif_transpose(original)

    # ========================================================
    # 處理透明通道與格式轉換（轉成 RGB 白底）
    # ========================================================
    if original.mode in ("RGBA", "LA") or (original.mode == "P" and "transparency" in original.info):
        background = Image.new("RGB", original.size, (255, 255, 255))
        if original.mode != "RGBA":
            original = original.convert("RGBA")
        background.paste(original, mask=original.getchannel("A"))
        original = background
    else:
        original = original.convert("RGB")

    # ========================================================
    # 建立 1:1 正方形白底畫布
    # ========================================================
    width, height = original.size
    max_side = max(width, height)

    canvas = Image.new(
        "RGB",
        (max_side, max_side),
        (255, 255, 255),
    )

    x = (max_side - width) // 2
    y = (max_side - height) // 2

    canvas.paste(original, (x, y))

    # ========================================================
    # 調整大小 (Resize)
    # ========================================================
    canvas = canvas.resize(
        (output_size, output_size),
        Image.Resampling.LANCZOS,
    )

    # ========================================================
    # 強制輸出為標準 JPEG (JPG) 格式
    # ========================================================
    output = io.BytesIO()

    canvas.save(
        output,
        format="JPEG",  # 強制轉為 JPG
        quality=95,
        optimize=True,
        progressive=True,
    )

    output.seek(0)

    return canvas, output.getvalue()


# ============================================================
# 介面：圖片尺寸選擇與上傳
# ============================================================

st.markdown("---")
st.subheader("🖼️ 商品圖片｜蝦皮上傳規格 (支援 AVIF 轉 JPG)")

image_size = st.selectbox(
    "蝦皮商品圖片輸出尺寸",
    [
        "1000 × 1000 px",
        "1200 × 1200 px",
        "800 × 800 px",
    ],
    index=0,
)

size_map = {
    "1000 × 1000 px": 1000,
    "1200 × 1200 px": 1200,
    "800 × 800 px": 800,
}

output_size = size_map[image_size]

# 關鍵修正：將 type 加入 "avif" 讓介面允許上傳
uploaded_file = st.file_uploader(
    "上傳商品圖片 (JPG / JPEG / PNG / WEBP / AVIF)",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
        "avif",
    ],
    help="上傳後系統會自動將各種格式（含 AVIF）轉為蝦皮專用的 1:1 標準 JPG 格式。",
)


if uploaded_file:

    try:
        # ========================================================
        # 原始圖片預覽
        # ========================================================
        original_image = Image.open(io.BytesIO(uploaded_file.getvalue()))
        original_image = ImageOps.exif_transpose(original_image)

        st.markdown("### 📷 原始商品圖片")
        st.image(
            original_image,
            caption=f"原始格式: {original_image.format} ｜ 尺寸: {original_image.width} × {original_image.height}px",
            use_container_width=True,
        )

        # ========================================================
        # 轉換為蝦皮 JPG 規格
        # ========================================================
        shopee_image, shopee_bytes = prepare_shopee_image(
            uploaded_file,
            output_size,
        )

        st.markdown("### 🛒 蝦皮上傳專用圖 (JPG)")
        st.image(
            shopee_image,
            caption=f"蝦皮版本 ｜ {output_size} × {output_size}px ｜ JPEG (JPG) ｜ 1:1",
            use_container_width=True,
        )

        st.success(
            f"✅ 成功將圖片轉換為蝦皮標準 JPG 格式："
            f"{output_size} × {output_size}px / RGB / 1:1"
        )

        # ====================================================
        # 下載按鈕
        # ====================================================
        file_name = Path(uploaded_file.name).stem
        shopee_file_name = f"{file_name}_shopee_{output_size}x{output_size}.jpg"

        st.download_button(
            label="⬇️ 下載蝦皮專用 JPG 圖片",
            data=shopee_bytes,
            file_name=shopee_file_name,
            mime="image/jpeg",
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"❌ 圖片處理失敗（可能是 AVIF 解碼需要安裝額外套件）：{e}")

else:
    st.info(
        "請上傳商品圖片（支援 JPG、PNG、WEBP、AVIF），"
        "系統會自動幫您轉成符合蝦皮規範的 1:1 標準 JPG 格式。"
    )
