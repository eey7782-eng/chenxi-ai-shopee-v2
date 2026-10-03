import streamlit as st

# 設定網頁基本標題與寬度
st.set_page_config(
    page_title="山林漫活休閒露營區",
    page_icon="🏕️",
    layout="wide"
)

# 側邊欄導覽列
st.sidebar.title("🏕️ 營區導覽選單")
menu = st.sidebar.选择營區專區 if False else st.sidebar.radio(
    "選擇瀏覽頁面",
    ["🏠 營區首頁", "☕ 咖啡廳與品茗", "🍖 烤肉與卡拉OK", "🐔 放山雞與果園生態", "📅 線上預約登記"]
)

# 聯絡資訊側邊欄固定顯示
st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 聯絡我們")
st.sidebar.markdown("**營區名稱**：山林漫活休閒露營區")
st.sidebar.markdown("**聯絡電話**：0912-345-678")
st.sidebar.markdown("**Line ID**：campsite123")
st.sidebar.markdown("**營區地址**：台灣某某市山林路一段 88 號")

# 1. 首頁
if menu == "🏠 營區首頁":
    st.title("🌲 歡迎來到【山林漫活休閒露營區】")
    st.subheader("離塵不離城，結合自然果園、在地美食與放鬆休閒的世外桃源！")
    
    st.image("https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    st.markdown("### ✨ 營區亮點介紹")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("☕ **悠閒咖啡與泡茶**\n\n手沖咖啡與高山茶席，享受慢活時光。")
    with col2:
        st.info("🎤 **歡樂烤肉與卡拉OK**\n\n專業烤肉設備與獨立歡唱包廂。")
    with col3:
        st.info("🐔 **天然放山雞與果園**\n\n產地到餐桌，品嚐美味放山雞與採果樂。")

# 2. 咖啡廳與品茗
elif menu == "☕ 咖啡廳與品茗":
    st.title("☕ 咖啡廳 & 泡茶區")
    st.write("在山林環繞的環境中，品嚐一杯香濃咖啡，或是和親朋好友一同泡茶談心。")
    
    tab1, tab2 = st.tabs(["☕ 山林咖啡廳", "🍵 景觀泡茶區"])
    
    with tab1:
        st.subheader("手作咖啡與下午茶")
        st.write("- 提供手沖特調咖啡、季節水果鬆餅、特製輕食。")
        st.write("- 營業時間：上午 09:00 - 下午 18:00")
    
    with tab2:
        st.subheader("景觀泡茶雅座")
        st.write("- 提供精選茶葉與茶具租借服務。")
        st.write("- 適合家庭、好友圍坐品茗，欣賞山景與果園風光。")

# 3. 烤肉與卡拉OK
elif menu == "🍖 烤肉與卡拉OK":
    st.title("🍖 烤肉區 & 🎤 卡拉OK區")
    st.write("盡情享受歡樂的聚會時光，大口吃肉、盡情高歌！")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 露天烤肉區")
        st.write("- 提供寬敞的烤肉爐位與桌椅。")
        st.write("- 可代訂新鮮烤肉食材組合包（需提前 3 天預訂），或自行攜帶食材。")
    with col2:
        st.subheader("🎶 卡拉OK歡唱包廂")
        st.write("- 獨立包廂設計，音響設備齊全。")
        st.write("- 歡唱不受干擾，盡情展現歌喉。")

# 4. 放山雞與果園生態
elif menu == "🐔 放山雞與果園生態":
    st.title("🐔 放山雞產地直銷 & 🌳 豐富果園區")
    st.write("體驗真實的農村生態，品嚐最天然的在地好味道！")
    
    st.markdown("### 🐓 自養放山雞料理")
    st.write("我們的放山雞在山林間自由奔跑、吃天然穀物長大，肉質扎實鮮甜！")
    st.write("- **招牌推薦**：桶仔雞、放山雞香菇雞湯（需提前預約現做）。")
    
    st.markdown("### 🍊 季節果園區")
    st.write("園區種植多樣季節水果，隨時節開放遊客入園體驗採果樂趣，讓大小朋友都能親近大自然。")

# 5. 線上預約登記
elif menu == "📅 線上預約登記":
    st.title("📅 營區設施與露營線上預約")
    st.write("請填寫以下表單進行預約，我們收到後會盡快與您確認！")
    
    with st.form("booking_form"):
        name = st.text_input("您的姓名")
        phone = st.text_input("聯絡電話")
        date = st.date_input("預計造訪日期")
        
        services = st.multiselect(
            "選擇您想預約的項目（可複選）",
            ["露營營位", "咖啡廳座位", "烤肉區場地 + 食材", "卡拉OK包廂", "放山雞料理預訂", "果園採果體驗"]
        )
        
        note = st.text_area("備註或特殊需求（例如：放山雞需要幾隻、人數等）")
        
        submitted = st.form_submit_button("送出預約")
        
        if submitted:
            if name and phone:
                st.success(f"🎉 感謝 {name}！您的預約資料已送出。我們將會透過電話 ({phone}) 與您聯繫確認細節！")
            else:
                st.warning("⚠️ 請填寫「您的姓名」與「聯絡電話」以便我們與您聯繫。")
