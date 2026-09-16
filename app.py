import streamlit as st
import datetime

# 設定網頁版面
st.set_page_config(
    page_title="黑金剛 AI 電商總控中心 PRO - 自動選品", 
    page_icon="🦍", 
    layout="centered"
)

st.title("🦍 黑金剛 AI 電商總控中心 PRO")
st.caption("蝦皮自動選品與 AI 智慧行銷工作流")

# 建立分頁介面 (模擬截圖中的功能切換)
tab1, tab2, tab3 = st.tabs(["🔍 蝦皮自動選品", "📜 自動選品紀錄", "🎬 AI 混剪短影音"])

# ============================================================
# 分頁 1：蝦皮自動選品 (對應圖 1 & 圖 2)
# ============================================================
with tab1:
    st.subheader("🛒 蝦皮自動選品工具")
    
    keyword = st.text_input("搜尋關鍵字", value="果果能量", placeholder="輸入想推廣的商品關鍵字...")
    
    col1, col2 = st.columns(2)
    with col1:
        start_item = st.number_input("從第幾件開始", min_value=1, value=1)
    with col2:
        max_items = st.number_input("預計查看 (最多200件)", min_value=1, max_value=200, value=200)
    
    st.markdown("##### ⚙️ 進階篩選條件")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        min_commission = st.number_input("最低分潤率 (%)", value=3.0)
        min_sales = st.number_input("最低月銷量 (件)", value=30)
    with col_f2:
        max_promo_people = st.number_input("最高推廣人數", value=150)
        price_range = st.slider("售價範圍 (NT$)", 0, 100000, (150, 100000))

    st.info(f"📌 預計將查看第 {start_item} ～ {start_item + max_items - 1} 件商品 (共 {max_items} 件)")

    if st.button("🚀 開始選品", type="primary", use_container_width=True):
        with st.spinner(f"🦍正在自動掃描蝦皮關鍵字「{keyword}」的聯盟商品..."):
            # 這裡未來可串接 n8n 或蝦皮聯盟 API 爬蟲
            st.success(f"✅ 掃描完成！找到 36 件符合條件的商品。")
            
            # 模擬呈現搜尋結果 (對應圖 5)
            st.markdown("### 📦 選品結果清單")
            
            sample_products = [
                {"name": "蛋白質威化餅 健工聯名新口味 Protein Wafer", "price": 259, "commission": 7, "promo": 149, "sales": 798},
                {"name": "水解乳清蛋白 多口味清蛋白飲 (500g/包)", "price": 1189, "commission": 7, "promo": 129, "sales": 401},
                {"name": "果果堅果 乳清蛋白 隨身包", "price": 489, "commission": 3, "promo": 150, "sales": 345},
            ]
            
            for idx, p in enumerate(sample_products, 1):
                with st.container():
                    st.markdown(f"**{idx}. {p['name']}**")
                    st.caption(f"💰 售價: ${p['price']} | 📈 分潤: {p['commission']}% | 👥 推廣人數: {p['promo']} | 📦 月銷量: {p['sales']}")
                    
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        if st.button("📋 複製", key=f"copy_{idx}"):
                            st.toast(f"已複製 {p['name']} 資訊！")
                    with b2:
                        if st.button("🎬 AI 混剪", key=f"video_{idx}"):
                            st.toast(f"已將 {p['name']} 送入 AI 短影音引擎！")
                    with b3:
                        if st.button("⭐ 收藏", key=f"fav_{idx}"):
                            st.toast(f"已加入商品收藏！")
                    st.markdown("---")

# ============================================================
# 分頁 2：自動選品紀錄 (對應圖 4)
# ============================================================
with tab2:
    st.subheader("📜 自動選品歷史紀錄")
    
    history_data = [
        {"keyword": "果果能量", "status": "掃描完成", "found": 36, "total": 200, "time": "2026-09-16 21:25", "cond": "分潤率 ≥ 3%、推廣人數 ≤ 150、月銷量 ≥ 30"},
        {"keyword": "蝦皮直營", "status": "掃描完成", "found": 2, "total": 200, "time": "2026-09-16 21:16", "cond": "分潤率 ≥ 3%、推廣人數 ≤ 150、月銷量 ≥ 30"},
        {"keyword": "便器", "status": "已停止", "found": 33, "total": 67, "time": "2026-09-15 21:47", "cond": "分潤率 ≥ 3%、推廣人數 ≤ 100、月銷量 ≥ 30"}
    ]

    for h in history_data:
        with st.container():
            col_h1, col_h2 = st.columns([3, 1])
            with col_h1:
                st.markdown(f"#### 🔍 {h['keyword']} <span style='color:green; font-size:14px;'>[{h['status']}]</span>", unsafe_allow_html=True)
                st.write(f"找到 **{h['found']}** 件符合 · 共掃描 {h['total']} 件")
                st.caption(f"條件：{h['cond']}")
                st.caption(f"掃描時間：{h['time']}")
            with col_h2:
                if st.button("查看", key=f"view_{h['keyword']}_{h['time']}"):
                    st.info(f"正在載入 {h['keyword']} 的歷史選品結果...")
            st.markdown("---")

# ============================================================
# 分頁 3：AI 混剪短影音 (對應圖 3)
# ============================================================
with tab3:
    st.subheader("🎬 AI 混剪短影音引擎")
    st.markdown("只要加入圖片、影片和商品資訊，AI 就能幫你自動混剪出適合 TikTok / YouTube Shorts / Reels 的短影音。")
    
    if st.button("✨ 立即建立 AI 混剪任務", type="primary", use_container_width=True):
        st.success("🚀 AI 短影音混剪工作流已啟動！")

# 頁尾
st.markdown("---")
st.caption("🖤 黑金剛 AI 多 AI 電商總控中心 PRO  \n商品真實性優先 | AI 主控 | 電商內容工作流")
