# ============================================================
# 10. 商品圖片｜蝦皮上傳圖片規格處理
# ============================================================

from PIL import Image, ImageOps
import io


def prepare_shopee_image(uploaded_file, output_size=1000):
    """
    將使用者上傳的商品圖片轉換成適合蝦皮商品圖使用的格式。

    功能：
    1. JPG / JPEG / PNG / WEBP 皆可讀取
    2. 自動轉 RGB
    3. 自動裁切 / 留白至 1:1
    4. 輸出正方形圖片
    5. JPEG 品質 95
    6. 不拉伸商品
    """

    raw = uploaded_file.getvalue()

    original = Image.open(io.BytesIO(raw))

    # 修正 EXIF 方向
    original = ImageOps.exif_transpose(original)

    # RGB
    if original.mode not in ("RGB", "RGBA"):
        original = original.convert("RGB")

    if original.mode == "RGBA":
        background = Image.new(
            "RGB",
            original.size,
            (255, 255, 255),
        )
        background.paste(
            original,
            mask=original.getchannel("A"),
        )
        original = background
    else:
        original = original.convert("RGB")

    # ========================================================
    # 建立 1:1 正方形畫布
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
    # Resize
    # ========================================================

    canvas = canvas.resize(
        (output_size, output_size),
        Image.Resampling.LANCZOS,
    )

    # ========================================================
    # JPEG 輸出
    # ========================================================

    output = io.BytesIO()

    canvas.save(
        output,
        format="JPEG",
        quality=95,
        optimize=True,
        progressive=True,
    )

    output.seek(0)

    return canvas, output.getvalue()


# ============================================================
# 蝦皮圖片尺寸選擇
# ============================================================

st.markdown("---")
st.subheader("🖼️ 商品圖片｜蝦皮上傳規格")

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
    help="上傳後系統會自動轉成 1:1 JPEG 商品圖。",
)


if uploaded_file:

    # ========================================================
    # 原始圖片
    # ========================================================

    st.markdown("### 📷 原始商品圖片")

    original_image = Image.open(
        io.BytesIO(
            uploaded_file.getvalue()
        )
    )

    original_image = ImageOps.exif_transpose(
        original_image
    )

    st.image(
        original_image,
        caption=f"原始圖片｜{original_image.width} × {original_image.height}px",
        use_container_width=True,
    )

    # ========================================================
    # 蝦皮規格轉換
    # ========================================================

    try:

        shopee_image, shopee_bytes = prepare_shopee_image(
            uploaded_file,
            output_size,
        )

        st.markdown("### 🛒 蝦皮上傳圖片")

        st.image(
            shopee_image,
            caption=f"蝦皮版本｜{output_size} × {output_size}px｜JPEG｜1:1",
            use_container_width=True,
        )

        st.success(
            f"✅ 已完成蝦皮商品圖處理："
            f"{output_size} × {output_size}px / JPEG / RGB / 1:1"
        )

        # ====================================================
        # 下載
        # ====================================================

        file_name = Path(
            uploaded_file.name
        ).stem

        shopee_file_name = (
            f"{file_name}_shopee_{output_size}x{output_size}.jpg"
        )

        st.download_button(
            label="⬇️ 下載蝦皮上傳圖片",
            data=shopee_bytes,
            file_name=shopee_file_name,
            mime="image/jpeg",
            use_container_width=True,
        )

        # ====================================================
        # 圖片資訊
        # ====================================================

        with st.expander("🔍 圖片規格檢查"):

            st.write(
                f"原始尺寸："
                f"{original_image.width} × "
                f"{original_image.height}px"
            )

            st.write(
                f"輸出尺寸："
                f"{output_size} × "
                f"{output_size}px"
            )

            st.write("比例：1:1")

            st.write("格式：JPEG")

            st.write("色彩模式：RGB")

            st.write("用途：蝦皮商品圖片")

    except Exception as e:

        st.error(
            f"❌ 圖片處理失敗：{e}"
        )

else:

    st.info(
        "請先上傳商品圖片。"
        "系統會自動建立蝦皮 1:1 商品圖。"
    )
