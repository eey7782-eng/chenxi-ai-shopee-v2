# ============================================================
# 10. 商品圖片｜蝦皮上傳圖片規格處理 (強制輸出 JPG)
# ============================================================

from PIL import Image, ImageOps
import io
from pathlib import Path
import streamlit as st


def prepare_shopee_image(uploaded_file, output_size=1000):
    """
    將使用者上傳的商品圖片轉換成適合蝦皮商品圖使用的格式，
    並強制轉為標準 JPG / JPEG 格式。
    """

    raw = uploaded_file.getvalue()
    original = Image.open(io.BytesIO(raw))

    # 修正 EXIF 方向
    original = ImageOps.exif_transpose(original)

    # ========================================================
    # 處理透明通道（如 PNG 轉白底 JPG）
    # ========================================================
    if original.mode in ("RGBA", "LA") or (original.mode == "P" and "transparency" in original.info):
        # 如果有透明背景，貼到純白畫布上避免變黑
        background = Image.new("RGB", original.size, (255, 255, 255))
        if original.mode != "RGBA":
            original = original.convert("RGBA")
        background.paste(original, mask=original.getchannel("A"))
        original = background
    else:
        # 其他模式一律轉成標準 RGB
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
        format="JPEG",  # 強制指定格式為 JPEG
        quality=95,     # 高畫質品質
        optimize=True,
        progressive=True,
    )

    output.seek(0)

    return canvas, output.getvalue()


# ============================================================
# 蝦皮圖片尺寸選擇與介面
# ============================================================

st.markdown("---")
st.subheader("🖼️ 商品圖片｜蝦皮上傳規格 (強制 JPG)")

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


uploaded_file = st.file_uploader(
    "上傳商品原始圖片",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
    ],
    help="上傳後系統會自動轉為 1:1 正方形的 JPG 格式。",
)


if uploaded_file:

    # ========================================================
    # 原始圖片預覽
    # ========================================================

    st.markdown("### 📷 原始商品圖片")

    original_image = Image.open(
        io.BytesIO(uploaded_file.getvalue())
    )

    original_image = ImageOps.exif_transpose(original_image)

    st.image(
        original_image,
        caption=f"原始圖片｜格式: {original_image.format} ｜ {original_image.width} × {original_image.height}px",
        use_container_width=True,
    )

    # ========================================================
    # 蝦皮規格轉換 (轉 JPG)
    # ========================================================

    try:

        shopee_image, shopee_bytes = prepare_shopee_image(
            uploaded_file,
            output_size,
        )

        st.markdown("### 🛒 蝦皮上傳圖片 (JPG)")

        st.image(
            shopee_image,
            caption=f"蝦皮版本｜{output_size} × {output_size}px ｜ 格式: JPEG (JPG) ｜ 1:1",
            use_container_width=True,
        )

        st.success(
            f"✅ 已成功轉為蝦皮標準 JPG 商品圖："
            f"{output_size} × {output_size}px / JPG / RGB / 1:1"
        )

        # ====================================================
        # 下載按鈕 (強制 .jpg)
        # ====================================================

        file_name = Path(uploaded_file.name).stem

        shopee_file_name = (
            f"{file_name}_shopee_{output_size}x{output_size}.jpg"
        )

        st.download_button(
            label="⬇️ 下載蝦皮專用 JPG 圖片",
            data=shopee_bytes,
            file_name=shopee_file_name,
            mime="image/jpeg",
            use_container_width=True,
        )

        # ====================================================
        # 圖片規格檢查
        # ====================================================

        with st.expander("🔍 圖片規格檢查"):

            st.write(
                f"原始尺寸：{original_image.width} × {original_image.height}px"
            )

            st.write(
                f"輸出尺寸：{output_size} × {output_size}px"
            )

            st.write("比例：1:1 正方形")

            st.write("格式：JPEG (.jpg)")

            st.write("色彩模式：RGB (自動處理透明背景轉白底)")

            st.write("用途：蝦皮商品圖片上傳")

    except Exception as e:

        st.error(
            f"❌ 圖片處理失敗：{e}"
        )

else:

    st.info(
        "請先上傳商品圖片（支援 JPG、PNG、WEBP），"
        "系統會自動幫您轉成符合蝦皮規範的 1:1 標準 JPG 格式。"
    )
