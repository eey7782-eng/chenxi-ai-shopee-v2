import streamlit as st
import os

# 頁面基本設定
st.set_page_config(page_title="媽祖田休閒農場", page_icon="🌱", layout="centered")

# 頁面主標題與簡介
st.markdown("<h1 style='text-align: center; color: #2c7a4b;'>🌱 媽祖田休閒農場</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.05rem;'>賞花 / 採果 / 烤肉 / 泡茶 / 咖啡 / 放山雞 / 卡拉OK (用餐採預約制)</p>", unsafe_allow_html=True)

st.divider()

# 營業與地址資訊卡片
st.markdown("### 📍 營業資訊與地址")
st.info(
    "**地址**：新北市土城區龍泉路72之1號\n\n"
    "**時間**：早上 8:00 ～ 下午 5 點 (星期一休園)"
)

# 快速撥號與導航按鈕區
st.markdown("### 📞 快速預約與導航")
col1, col2 = st.columns(2)
with col1:
    st.link_button("📞 市話預約", "tel:0222671679", use_container_width=True)
with col2:
    st.link_button("🗺️ Google 導航", "https://maps.google.com/?q=新北市土城區龍泉路72之1號", use_container_width=True)

st.markdown("### 📱 負責人手機")
col3, col4 = st.columns(2)
with col3:
    st.link_button("廖宗明 0919-775437", "tel:0919775437", use_container_width=True)
with col4:
    st.link_button("游鳳嬌 0919-315384", "tel:0919315384", use_container_width=True)

st.divider()

# 📸 農場實景相簿區
st.markdown("### 📸 農場風光與特色餐點")

# 這裡會自動檢查你資料夾裡的圖片檔 (假設圖片命名為 1.jpg 到 7.jpg，或你想用的檔名)
# 只要把照片檔跟 app.py 放在同一個資料夾，它就會自動秀出來！
image_files = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg"]

found_images = [img for img in image_files if os.path.exists(img)]

if found_images:
    for img in found_images:
        st.image(img, use_container_width=True)
else:
    st.warning("⚠️ 目前資料夾中還沒有找到圖片檔案。只要把照片（例如命名為 1.jpg、2.jpg...）放進跟 app.py 相同的資料夾，照片就會自動顯示在這裡喔！")
