import streamlit as st
import glob
import os

# 1. 頁面基本設定
st.set_page_config(page_title="媽祖田休閒農場", page_icon="🌱", layout="centered")

# 2. 頁面主標題與簡介
st.markdown("<h1 style='text-align: center; color: #2c7a4b;'>🌱 媽祖田休閒農場</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.05rem;'>賞花 / 採果 / 烤肉 / 泡茶 / 咖啡 / 放山雞 / 卡拉OK (用餐採預約制)</p>", unsafe_allow_html=True)

st.divider()

# 3. 營業與地址資訊卡片
st.markdown("### 📍 營業資訊與地址")
st.info(
    "**地址**：新北市土城區龍泉路72之1號\n\n"
    "**時間**：早上 8:00 ～ 下午 5 點 (星期一休園)"
)

# 4. 快速撥號與導航按鈕區
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

# 5. 📸 農場實景相簿區（自動搜尋同資料夾內的圖片）
st.markdown("### 📸 農場風光與特色餐點")

image_extensions = ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG"]
found_images = []
for ext in image_extensions:
    found_images.extend(glob.glob(ext))

# 排序以確保圖片順序穩定
found_images = sorted(list(set(found_images)))

if found_images:
    st.success(f"成功找到並載入 {len(found_images)} 張圖片！")
    for img_path in found_images:
        st.image(img_path, caption=f"相片：{img_path}", use_container_width=True)
else:
    st.error("⚠️ 畫面找不到圖片！請確認照片檔案有沒有跟 app.py 放在同一個資料夾／GitHub 專案裡面喔！")
