import streamlit as st

# 設定網頁標題與寬度
st.set_page_config(
    page_title="山林漫活休閒露營區",
    page_icon="🏕️",
    layout="wide"
)

# ── 側邊欄導覽列（點擊不同選項，右側畫面會立刻切換進去） ──
st.sidebar.title("🏕️ 營區導覽選單")
menu = st.sidebar.radio(
    "請選擇瀏覽分頁：",
    [
        "🏠 營區首頁", 
        "☕ 咖啡廳與品茗區", 
        "🍖 烤肉與卡拉OK", 
        "🐔 放山雞與果園生態", 
        "📅 線上預約與聯絡"
    ]
)

# ── 聯絡資訊固定在側邊欄下方 ──
st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 營區快速資訊")
st.sidebar.markdown("**電話**：0912-345-678")
st.sidebar.markdown("**Line**：@campsite123")
st.sidebar.markdown("**地址**：台灣某某市山林路一段 88 號")


# ==========================================
# 1. 營區首頁
# ==========================================
if menu == "🏠 營區首頁":
    st.title("🌲 歡迎來到【山林漫活休閒露營區】")
    st.subheader("離塵不離城，結合自然果園、在地美食與放鬆休閒的世外桃源！")
    
    st.image("https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    st.markdown("### ✨ 點擊下方按鈕快速了解各區特色：")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👉 探索咖啡與泡茶區"):
            st.info("請從左側選單切換至【☕ 咖啡廳與品茗區】")
    with col2:
        if st.button("👉 查看烤肉與唱歌"):
            st.info("請從左側選單切換至【🍖 烤肉與卡拉OK】")
    with col3:
        if st.button("👉 了解放山雞與果園"):
            st.info("請從左側選單切換至【🐔 放山雞與果園生態】")


# ==========================================
# 2. 咖啡廳與品茗區
# ==========================================
elif menu == "☕ 咖啡廳與品茗區":
    st.title("☕ 咖啡廳 & 景觀泡茶區")
    st.write("在群山環繞的環境中，享受悠閒的午後時光。")
    
    # 點進去之後的分頁籤 (Tabs)
    tab1, tab2 = st.tabs(["☕ 山林手作咖啡廳", "🍵 景觀泡茶雅座"])
    
    with tab1:
        st.subheader("手作咖啡與下午茶")
        st.write("我們提供自家特調手沖咖啡、季節限定水果鬆餅與輕食。")
        st.image("https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80", width=500)
        st.markdown("- **營業時間**：每日 09:00 - 18:00")
        st.markdown("- **特色**：使用高海拔在地豆，搭配無敵山景窗位。")
        
    with tab2:
        st.subheader("景觀泡茶區")
        st.write("提供完整的茶具組與台灣高山茶葉租借，最適合家族、好友圍坐聊天。")
        st.image("https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=80", width=500)
        st.markdown("- **消費方式**：以桌計費，含茶具與熱水供應。")


# ==========================================
# 3. 烤肉與卡拉OK
# ==========================================
elif menu == "🍖 烤肉與卡拉OK":
    st.title("🍖 露天烤肉區 & 🎤 歡樂卡拉OK")
    st.write("大口吃肉、盡情歡唱，打造最熱鬧的夜晚！")
    
    tab1, tab2 = st.tabs(["🔥 烤肉區介紹", "🎶 卡拉OK包廂"])
    
    with tab1:
        st.subheader("戶外烤肉同樂區")
        st.write("寬敞的半戶外烤肉場地，不怕風吹雨打。")
        st.markdown("- **裝備**：提供烤爐、桌椅、夾子等基本設備。")
        st.markdown("- **食材**：可代訂「澎湃烤肉食材組合包」（需於 3 天前預訂），也可自行攜帶喜愛的食材。")
        
    with tab2:
        st.subheader("獨立卡拉OK歡唱包廂")
        st.write("專業音響設備、舒適沙發包廂，讓你在大自然中盡情高歌。")
        st.markdown("- **收費方式**：以小時計算或包場制，需提前預約。")


# ==========================================
# 4. 放山雞與果園生態
# ==========================================
elif menu == "🐔 放山雞與果園生態":
    st.title("🐔 自養放山雞料理 & 🌳 季節果園區")
    st.write("吃得健康、玩得開心，體驗最天然的農村樂趣。")
    
    st.markdown("### 🐓 招牌放山雞料理")
    st.write("我們的放山雞在山林間自由奔跑、吃天然穀物長大，肉質鮮甜扎實！")
    st.markdown("- **桶仔雞**：皮脆肉多汁，香氣四溢（需提前預約現烤）。")
    st.markdown("- **放山雞香菇湯**：暖胃又滋補的在地好味道。")
    
    st.markdown("---")
    
    st.markdown("### 🍊 季節果園採果樂")
    st.write("園區內種植多種季節水果（如柑橘、四季果等），隨時節開放遊客入園體驗親手採果的樂趣！")


# ==========================================
# 5. 線上預約與聯絡
# ==========================================
elif menu == "📅 線上預約與聯絡":
    st.title("📅 線上預約登記表單")
    st.write("想要來露營、喝咖啡、訂放山雞或預約卡拉OK嗎？請填寫以下表單：")
    
    with st.form("booking_page_form"):
        name = st.text_input("您的姓名")
        phone = st.text_input("聯絡電話")
        date = st.date_input("預計造訪日期")
        
        choices = st.multiselect(
            "選擇您想預約的項目（可複選）",
            ["露營營位", "咖啡廳座位", "烤肉場地 + 食材", "卡拉OK包廂", "放山雞料理（桶仔雞/雞湯）", "果園採果體驗"]
        )
        
        message = st.text_area("其他特殊需求或備註（例如：放山雞數量、人數等）")
        
        submit_btn = st.form_submit_button("送出預約申請")
        
        if submit_btn:
            if name and phone:
                st.success(f"🎉 感謝 {name}！您的預約已成功送出。我們將會盡快撥打電話 ({phone}) 與您確認細節！")
            else:
                st.warning("⚠️ 請務必填寫「您的姓名」與「聯絡電話」，以便我們與您聯繫。")
                
    st.markdown("---")
    st.subheader("📍 聯絡資訊與交通方式")
    st.write("- **地址**：台灣某某市山林路一段 88 號")
    st.write("- **聯絡電話**：0912-345-678")
    st.write("- **Line 官方帳號**：@campsite123")
