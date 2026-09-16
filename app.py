# =====================================================================
# Z世代蝦皮自動化行銷系統 (app.py - 前台導購 + 後台 AI 影片腳本引擎)
# =====================================================================

import streamlit as st

# 設定網頁版面 (手機優先)
st.set_page_config(
    page_title="🔥 黑金剛極速選物與 AI 引擎",
    page_icon="🛍️",
    layout="centered"
)

# 側邊欄切換身份
st.sidebar.title("🛠️ 系統選單")
app_mode = st.sidebar.radio("選擇模式", ["🛍️ 前台：買家極速選物店", "🤖 後台：AI 影片與腳本產生器"])

# =====================================================================
# 模式 A：前台・買家極速選物店 (手機點擊直達商品頁)
# =====================================================================
if app_mode == "🛍️ 前台：買家極速選物店":
    st.markdown("<h2 style='text-align: center; margin-bottom: 0px;'>🔥 質感好物所</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>滑到都是好東西，無腦直達，閉眼入不踩雷</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 爆款選品清單 (記得將 link 換成你從蝦皮聯盟後台取得的【單一商品專屬分潤連結】)
    products = [
        {
            "title": "【果果能量】蛋白質威化餅 / 健工聯名新口味",
            "price": "NT$ 259",
            "tag": "#健身必備 #嘴饞救星",
            "desc": "超酥脆不甜膩，減脂期解饞神物！",
            "image": "https://images.unsplash.com/photo-1622484219566-3b3203673b22?w=600&q=80",
            "link": "https://s.shopee.tw/your_affiliate_link_1"
        },
        {
            "title": "【Snoopy 史努比】復古寬鬆純棉短T恤",
            "price": "NT$ 399",
            "tag": "#OOTD穿搭 #質感衣著",
            "desc": "磅數很夠、版型超挺不悶熱。",
            "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&q=80",
            "link": "https://s.shopee.tw/your_affiliate_link_2"
        },
        {
            "title": "【日常防護】極輕量自動三折防風傘",
            "price": "NT$ 199",
            "tag": "#雨具推薦 #包包必備",
            "desc": "輕到幾乎無感，晴雨兩用霧面手感。",
            "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&q=80",
            "link": "https://s.shopee.tw/your_affiliate_link_3"
        }
    ]

    # 用卡片式排版渲染
    for item in products:
        with st.container():
            st.image(item["image"], use_container_width=True)
            st.markdown(f"**{item['title']}**")
            st.caption(f"{item['tag']}  |  💰 **{item['price']}**")
            st.write(item["desc"])
            
            # 買家點擊按鈕直接開啟蝦皮 App 或商品頁
            st.link_button("🛒 立即前往蝦皮搶購", item["link"], use_container_width=True)
            st.markdown("---")

    st.markdown(
        "<p style='text-align: center; color: silver; font-size: 12px;'>本站所有商品皆為嚴選推薦，透過指定連結購買將獲得微薄分潤，謝謝支持！</p>", 
        unsafe_allow_html=True
    )

# =====================================================================
# 模式 B：後台・AI 影片與爆款腳本產生器
# =====================================================================
elif app_mode == "🤖 後台：AI 影片與腳本產生器":
    st.title("🤖 Z世代短影音與腳本產生器")
    st.caption("輸入想推廣的商品，一鍵產出 Threads 文案與 30 秒 Reels/Shorts 影片腳本！")
    st.markdown("---")

    # 輸入區
    product_name = st.text_input("輸入商品名稱或賣點：", placeholder="例如：磁吸行動電源、超顯瘦牛仔褲")
    tone = st.selectbox("選擇短影音風格：", ["🔥 真心實話/微毒舌避雷", "✨ 質感生活/氛圍感開箱", "💸 瘋狂省錢/高CP值推薦"])

    if st.button("🚀 一鍵生成 AI 影音行銷素材", use_container_width=True):
        if product_name:
            st.success("🎉 AI 內容生成完畢！可以直接複製使用：")
            
            # 模擬 AI 產出的結果
            st.markdown("### 📱 Threads / IG 爆款圖文")
            st.info(
                f"最近被這款 **{product_name}** 燒到不行🔥\n"
                f"老實說一開始還半信半疑，結果收到實品直接驚艷... 真的不是業配，真心推給跟我一樣有這困擾的人！\n\n"
                f"👇 傳送門幫大家放在這邊，自己去看：\n"
                f"(放你的蝦皮分潤連結)"
            )

            st.markdown("### 🎬 30秒短影音黃金分鏡腳本 (Reels / Shorts / TikTok)")
            st.warning(
                f"**[0-3秒] 痛點抓眼球**：「如果你還在盲目買 {product_name}，真的會這支影片救你一命...」\n\n"
                f"**[3-20秒] 真心開箱亮點**：畫面帶到商品特寫，語氣輕快：「重點是它...（帶入 {product_name} 的核心優勢），質感完全不輸大牌！」\n\n"
                f"**[20-30秒] 強力導購結語**：「真心覺得這價格很可以，傳送門就在我主頁或留言區，自己去搶！」"
            )
            
            st.markdown("---")
            st.info("💡 **下一步小提示**：你可以把上面的腳本拿去搭配手機配音，或是串接自動化剪輯工具（如 CapCut），就能快速大量產出短影音去吸流量囉！")
        else:
            st.warning("請先輸入商品名稱喔！")
