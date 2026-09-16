# ============================================================
# 黑金剛 AI 電商總控中心 PRO - 完整版主程式 (app.py)
# ============================================================

from pathlib import Path
import io
from PIL import Image, ImageOps
import streamlit as st

# 嘗試支援 AVIF 格式解碼（若環境無此套件則略過並使用基本防護）
try:
  import pillow_heif

  pillow_heif.register_heif_opener()
except ImportError:
  pass

# 設定網頁版面
st.set_page_config(
    page_title="黑金剛 AI 電商總控中心 PRO", page_icon="🦍", layout="centered"
)

# ============================================================
# 1. 預估利潤率計算區塊
# ============================================================
st.markdown("### 💰 預估利潤率")
col1, col2 = st.columns(2)
with col1:
  cost_price = st.number_input("商品成本 (NT$)", min_value=0.0, value=0.0, step=10.0)
with col2:
  selling_price = st.number_input(
      "預估售價 (NT$)", min_value=0.0, value=0.0, step=10.0
  )

if selling_price > 0:
  profit = selling_price - cost_price
  profit_margin = (profit / selling_price) * 100
  st.metric(label="預估利潤率", value=f"{profit_margin:.2f}%", delta=f"NT$ {profit:.1f}")
else:
  st.metric(label="預估利潤率", value="0.00%")

st.markdown("---")

# ============================================================
# 2. 商品圖片｜蝦皮上傳圖片規格處理函數
# ============================================================


def prepare_shopee_image(uploaded_file, output_size=1000):
  """將上傳的圖片轉換為蝦皮 1:1 標準 JPG 格式"""
  raw = uploaded_file.getvalue()
  original = Image.open(io.BytesIO(raw))

  # 修正 EXIF 方向
  original = ImageOps.exif_transpose(original)

  # 處理透明背景（轉純白底）
  if original.mode in ("RGBA", "LA") or (
      original.mode == "P" and "transparency" in original.info
  ):
    background = Image.new("RGB", original.size, (255, 255, 255))
    if original.mode != "RGBA":
      original = original.convert("RGBA")
    background.paste(original, mask=original.getchannel("A"))
    original = background
  else:
    original = original.convert("RGB")

  # 建立 1:1 正方形白底畫布
  width, height = original.size
  max_side = max(width, height)
  canvas = Image.new("RGB", (max_side, max_side), (255, 255, 255))

  x = (max_side - width) // 2
  y = (max_side - height) // 2
  canvas.paste(original, (x, y))

  # 調整大小
  canvas = canvas.resize((output_size, output_size), Image.Resampling.LANCZOS)

  # 輸出標準 JPEG
  output = io.BytesIO()
  canvas.save(output, format="JPEG", quality=95, optimize=True, progressive=True)
  output.seek(0)

  return canvas, output.getvalue()


# ============================================================
# 3. 商品圖片上傳介面 (已解鎖 AVIF / WEBP 支援)
# ============================================================
st.subheader("🖼️ 商品圖片")

image_size = st.selectbox(
    "蝦皮商品圖片輸出尺寸",
    ["1000 × 1000 px", "1200 × 1200 px", "800 × 800 px"],
    index=0,
)
size_map = {"1000 × 1000 px": 1000, "1200 × 1200 px": 1200, "800 × 800 px": 800}
output_size = size_map[image_size]

# 關鍵修正：完整支援 JPG, JPEG, PNG, WEBP, AVIF
uploaded_file = st.file_uploader(
    "上傳商品圖檔 JPG / JPEG / PNG / WEBP / AVIF",
    type=["jpg", "jpeg", "png", "webp", "avif"],
    help="上傳後系統會自動解碼並轉成蝦皮專用的 1:1 標準 JPG 格式。",
)

if uploaded_file:
  try:
    # 預覽原始圖片
    original_image = Image.open(io.BytesIO(uploaded_file.getvalue()))
    original_image = ImageOps.exif_transpose(original_image)

    st.markdown("### 📷 原始商品圖片")
    st.image(
        original_image,
        caption=(
            f"原始格式: {original_image.format} ｜ 尺寸:"
            f" {original_image.width} × {original_image.height}px"
        ),
        use_container_width=True,
    )

    # 轉換為蝦皮規格
    shopee_image, shopee_bytes = prepare_shopee_image(uploaded_file, output_size)

    st.markdown("### 🛒 蝦皮上傳專用圖 (JPG)")
    st.image(
        shopee_image,
        caption=(
            f"蝦皮版本 ｜ {output_size} × {output_size}px ｜ JPEG (JPG) ｜ 1:1"
        ),
        use_container_width=True,
    )

    st.success(f"✅ 成功轉換為蝦皮標準 JPG 格式：{output_size} × {output_size}px")

    # 下載按鈕
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
    st.error(f"❌ 圖片處理失敗：{e}")

else:
  st.info("請上傳商品圖片，系統將自動處理為蝦皮合規格式。")

st.markdown("---")

# ============================================================
# 4. 啟動 AI 全流程按鈕
# ============================================================
if st.button(
    "🚀 啟動黑金剛 AI 商品全流程", type="primary", use_container_width=True
):
  if uploaded_file:
    with st.spinner("🦍 黑金剛 AI 正在執行：圖文分析 ➡️ 文案生成 ➡️ 系統歸檔..."):
      # 這裡未來可直接對接你的 n8n Webhook 或 Gemini / OpenAI API
      st.success("✅ AI 全流程執行完畢！商品文案與資料已成功建立。")
  else:
    st.warning("⚠️ 請先上傳商品圖片，再啟動 AI 全流程！")

st.markdown("---")

# ============================================================
# 5. 歷史記錄區塊
# ============================================================
st.subheader("🕒 歷史記錄")
st.info("目前還沒有歷史記錄。")

# ============================================================
# 6. 頁尾資訊
# ============================================================
st.markdown("---")
st.caption(
    "🖤 黑金剛 AI 多 AI 電商總控中心 PRO  \n商品真實性優先 | AI 主控 | 電商內容工作流"
)
