# ============================================================
# 黑金剛 AI 電商總控中心 PRO - 蝦皮上傳與自動化模式 (app.py)
# ============================================================

from pathlib import Path
import streamlit as st

# 設定網頁版面
st.set_page_config(
    page_title="黑金剛 AI 電商總控中心 PRO", page_icon="🦍", layout="centered"
)

st.title("🦍 黑金剛 AI 電商總控中心 PRO")
st.caption("商品真實性優先 | AI 主控 | 蝦皮自動化上架工作流")

# ============================================================
# 1. 預估利潤率計算區塊
# ============================================================
st.markdown("### 💰 預估利潤率計算")
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
# 2. 蝦皮上傳模式｜改用「商品網址 / 圖片連結 / 文字」輸入（避開手機上傳限制）
# ============================================================
st.subheader("🛒 蝦皮商品資訊模式")

shopee_input_mode = st.radio(
    "選擇輸入方式", ["貼上蝦皮商品網址 / 圖片網址", "手動輸入商品資料"], index=0
)

product_name = ""
product_image_url = ""
product_description = ""

if shopee_input_mode == "貼上蝦皮商品網址 / 圖片網址":
  product_image_url = st.text_input(
      "🔗 貼上商品圖片網址 (Image URL)",
      placeholder="請貼上圖片網址（例如從瀏覽器複製的圖片連結）",
  )
  product_name = st.text_input("📦 商品名稱 / 關鍵字", placeholder="例如：史努比寬鬆短T恤")
  
  if product_image_url:
    st.image(product_image_url, caption="預覽商品圖片", use_container_width=True)

else:
  product_name = st.text_input("📦 商品名稱", placeholder="例如：史努比寬鬆短T恤")
  product_description = st.text_area("📝 商品規格/特色描述", placeholder="請輸入材質、尺寸、顏色等特點...")

st.markdown("---")

# ============================================================
# 3. 啟動黑金剛 AI 商品全流程
# ============================================================
if st.button(
    "🚀 啟動黑金剛 AI 商品全流程", type="primary", use_container_width=True
):
  if product_name:
    with st.spinner("🦍 黑金剛 AI 正在執行：商品解析 ➡️ 行銷文案生成 ➡️ 系統歸檔..."):
      # 這裡可以直接對接你的 n8n 或 AI 模型
      st.success(f"✅ 成功為【{product_name}】生成蝦皮聯盟行銷與上架內容！")
      
      with st.expander("✨ AI 生成的蝦皮推廣文案預覽", expanded=True):
        st.markdown(f"**【爆款推薦】{product_name}**")
        st.markdown("🔥 質感超好、舒適透氣，粉絲強力推薦必備款！")
        st.markdown("🛒 立即搶購：[請在此填入你的蝦皮分潤短連結]")
        st.markdown("#蝦皮購物 #好物推薦 #穿搭必備 #聯盟行銷")
  else:
    st.warning("⚠️ 請先輸入商品名稱或相關資訊，再啟動 AI 全流程！")

st.markdown("---")

# ============================================================
# 4. 歷史記錄區塊
# ============================================================
st.subheader("🕒 歷史記錄")
st.info("目前還沒有歷史記錄。")

# ============================================================
# 5. 頁尾資訊
# ============================================================
st.markdown("---")
st.caption(
    "🖤 黑金剛 AI 多 AI 電商總控中心 PRO  \n商品真實性優先 | AI 主控 | 電商內容工作流"
)
