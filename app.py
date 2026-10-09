import streamlit as st
import pandas as pd

# 頁面配置
st.set_page_config(
    page_title="辰曦 AI 蝦皮選品與短影音變現系統 Pro",
    page_icon="🚀",
    layout="wide"
)

# 初始化產品資料狀態
if "products" not in st.session_state:
    st.session_state.products = []

# 側邊欄導航
st.sidebar.title("🚀 辰曦 AI 系統選單")
menu = st.sidebar.selectbox(
    "選擇功能模組",
    [
        "📊 商品數據匯入與總覽", 
        "🔥 AI 爆款分析 (Top 20)", 
        "⏳ AI 商品生命週期", 
        "🛡️ AI 風險分析", 
        "🎬 21組黑金剛 4.0 提示詞生成器"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("系統狀態：正常運作 (2026 政策避險版)")

# ==========================
# 1. 商品數據匯入與總覽
# ==========================
if menu == "📊 商品數據匯入與總覽":
    st.title("📊 蝦皮聯盟與公司商品數據管理")
    st.write("上傳 Excel 或 CSV 檔案，快速匯入選品資料庫進行自動化評分與分析。")

    uploaded_file = st.file_uploader("上傳 Excel 或 CSV 檔案", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # 轉為字典清單存入 session_state
        st.session_state.products = df.to_dict(orient="records")
        st.success(f"成功匯入 {len(st.session_state.products)} 筆商品資料！")

    if len(st.session_state.products) > 0:
        st.subheader("📋 目前資料庫商品清單")
        st.dataframe(pd.DataFrame(st.session_state.products))
    else:
        st.warning("目前資料庫沒有商品，請先上傳檔案或使用下方測試數據。")
        
        if st.button("載入範例測試數據"):
            st.session_state.products = [
                {"name": "冰感無刷掛腰空調", "monthly_sales": 6500, "commission": 12, "rating": 4.8, "reviews": 320, "ai_score": 95},
                {"name": "大容量真空保溫杯", "monthly_sales": 2200, "commission": 8, "rating": 4.6, "reviews": 150, "ai_score": 85},
                {"name": "網紅多功能料理鍋", "monthly_sales": 1200, "commission": 4, "rating": 4.3, "reviews": 80, "ai_score": 72},
                {"name": "氣墊減壓運動鞋", "monthly_sales": 250, "commission": 3, "rating": 4.1, "reviews": 45, "ai_score": 60},
            ]
            st.rerun()

# ==========================
# 2. AI 爆款分析
# ==========================
elif menu == "🔥 AI 爆款分析 (Top 20)":
    st.title("🔥 AI 爆款潛力分析")
    
    if len(st.session_state.products) == 0:
        st.warning("目前沒有商品資料，請先至第一頁匯入或載入範例。")
    else:
        ranking = sorted(
            st.session_state.products,
            key=lambda x: (x.get("ai_score", 0), x["monthly_sales"], x["rating"]),
            reverse=True
        )
        
        for index, product in enumerate(ranking[:20], start=1):
            with st.expander(f"TOP {index} | {product['name']} (AI 分數: {product.get('ai_score', 0)})"):
                col1, col2, col3 = st.columns(3)
                col1.metric("月銷量", f"{product['monthly_sales']} 件")
                col2.metric("商品評分", f"⭐ {product['rating']}")
                col3.metric("評論數", f"{product['reviews']} 則")
                
                score = product.get("ai_score", 0)
                if score >= 90:
                    st.success("爆款等級：★★★★★ (強力主推)")
                elif score >= 80:
                    st.info("爆款等級：★★★★ (具備潛力)")
                else:
                    st.warning("爆款等級：★★★ (一般觀察)")

# ==========================
# 3. AI 商品生命週期
# ==========================
elif menu == "⏳ AI 商品生命週期":
    st.title("⏳ AI 商品生命週期分析")
    
    if len(st.session_state.products) == 0:
        st.warning("目前沒有商品資料。")
    else:
        for product in st.session_state.products:
            sales = product["monthly_sales"]
            if sales >= 5000:
                stage, color = "成長期 (Scaling)", "🟢"
            elif sales >= 1000:
                stage, color = "成熟期 (Mature)", "🔵"
            elif sales >= 300:
                stage, color = "測試期 (Testing)", "🟡"
            else:
                stage, color = "導入期 (Intro)", "🔴"
                
            st.markdown(f"**{color} {product['name']}**")
            st.text(f"月銷量：{sales} | 生命週期階段：{stage}")
            st.markdown("---")

# ==========================
# 4. AI 風險分析
# ==========================
elif menu == "🛡️ AI 風險分析":
    st.title("🛡️ 蝦皮違規與選品風險評估")
    
    if len(st.session_state.products) == 0:
        st.warning("目前沒有商品資料。")
    else:
        for product in st.session_state.products:
            risk = []
            if product.get("rating", 5.0) < 4.5:
                risk.append("評分偏低 (< 4.5)")
            if product.get("reviews", 500) < 100:
                risk.append("評論不足 (< 100)")
            if product.get("commission", 10) < 5:
                risk.append("分潤偏低 (< 5%)")
            if product.get("monthly_sales", 1000) < 300:
                risk.append("市場需求偏低 (< 300)")
                
            with st.container():
                st.subheader(f"商品：{product['name']}")
                if len(risk) == 0:
                    st.success("風險評估：低風險 (優質選品)")
                else:
                    st.error("風險警示：")
                    for item in risk:
                        st.markdown(f"- ⚠️ {item}")
                st.markdown("---")

# ==========================
# 5. 21組黑金剛 4.0 提示詞生成器
# ==========================
elif menu == "🎬 21組黑金剛 4.0 提示詞生成器":
    st.title("🎬 即夢 AI 4.0 ─ 21組黑金剛提示詞生成器")
    st.write("一鍵套用 21 組高階避雷與防封協議，自動組合您的分身與商品。")

    col_a, col_b = st.columns(2)
    with col_a:
        img1_name = st.text_input("人物分身代號 (例如 @Image1)", "@Image1")
    with col_b:
        product_name = st.text_input("商品名稱/代號 (例如 @Image2 冰感掛腰空調)", "@Image2 冰感無刷掛腰空調")

    protocol_choice = st.selectbox(
        "選擇戰術協議",
        [
            "1. V7 (OMNI-SHIELD) 萬用平衡型",
            "2. GHOST-MINI 量子衝量型",
            "3. The Ghost Protocol 無痕微調型",
            "4. DEEP-WASH 暴力洗白型",
            "5. V9 神經擾動版 (防 AI 掃描)",
            "6. GHOST-CAM 手機隨手拍",
            "7. VFR-PROTO 時間變速型",
            "8. LOBSTER-EAT 暴力咬碎/吞嚥協議 (食品專用)",
            "9. GHOST-SHADOW 空間光影連動",
            "10. LOBSTER-ELITE 精品/重量感協議 (高客單專用)",
            "11. SKY-SHIELD 動作閉環與標籤鎖定 (旋轉不變形)",
            "12. TIKTOK-KING 流量鉤子協議 (前 3 秒黃金鉤子)",
            "13. OMEGA-MAX: 2.0 終極台灣在地化整合版"
        ]
    )

    # 根據選擇動態產生對應的 Prompt
    if "V7" in protocol_choice:
        generated_prompt = f"8k raw, {img1_name} x {product_name}. 9:16. [BIO]: CapillaryReaction(pale-to-pink), SkinIndentation:35%, Physical pores. [LIGHT]: Tiangong Aesthetic Flow, LightRefraction, 15% film grain, HandheldShake:1.2Hz. [SYNC]: High-fidelity facial muscle tension, Exaggerated labial movement. [BEYOND]: No VFX, InvisibleMetadataMask, Bypass 2026 Detection."
    elif "GHOST-MINI" in protocol_choice:
        generated_prompt = f"8k raw, {img1_name} x {product_name}, 9:16. Non-Linear-Motion-Logic. [BIO]: CapillaryReaction, SkinIndentation:35%. [FX]: Tiangong Flow, Refraction, Grain-Noise:25%, Jitter:1.24Hz. [BYPASS]: Dithering, Asymmetric-Muscle, Metadata-Mask."
    elif "LOBSTER-EAT" in protocol_choice:
        generated_prompt = f"8k raw, {img1_name} physically biting and eating {product_name}. 9:16. [LOGIC]: Realistic chewing motion, liquid surface tension, crumbs falling. [BIO]: CapillaryReaction, Saliva-texture, Lip-indentation. [BYPASS]: 20% film grain, handheld shaky, No-VFX, Bypass 2026 detection."
    elif "OMEGA-MAX" in protocol_choice:
        generated_prompt = f"[PROMPT]: {img1_name} as a professional Taiwanese creator enthusiastically presenting {product_name}. 8k raw photo, photorealistic skin pores, organic micro-blemishes, messy hair, zero-beautification. 15% digital film grain, handheld camera shake, Bypass 2026 Detection, InvisibleMetadataMask. Extreme texture on {product_name}, hyper-legible labels, realistic gravitational weight. Exaggerated facial muscle, elastic lip-sync, laryngeal movement, friendly Taiwanese vibe expressions. 9:16, cinematic, high-bitrate simulation."
    else:
        generated_prompt = f"[PROMPT]: 8k raw cine-photo, {img1_name} presenting {product_name}, 9:16. [MOTION]: Non-Linear-Motion, HandheldJitter:1.24Hz. [BIO]: CapillaryPulse, SkinIndentation:35%. [SHIELD]: InvisibleMetadataMask, Bypass-2026-Scan, Scrub-AI-Signatures."

    st.subheader("✨ 生成的即夢 4.0 戰術提示詞")
    st.code(generated_prompt, language="text")

    if st.button("📋 複製提示詞至剪貼簿"):
        st.toast("提示詞已就緒，請直接貼至即夢 AI 4.0！", icon="✅")
