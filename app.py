# =====================================================================
# Z世代蝦皮自動化行銷系統 (app.py - A+B 完整合集)
# 功能：後台 AI 爆款腳本產生器 + 前台 極速導購選物網頁
# =====================================================================

import streamlit as st

# 設定網頁版面 (手機優先)
st.set_page_config(
    page_title="黑金剛極速選物與 AI 引擎",
    page_icon="🔥",
    layout="centered"
)

# 側邊欄切換身份
st.sidebar.title("🛠️ 系統選單")
app_mode = st.sidebar.radio("選擇模式", ["🛍️ 前台：買家極速選物店", "🤖 後台：AI 爆款與腳本產生器"])

# =====================================================================
# 模式 A：前台・買家極速選物店
# =====================================================================
if app_mode == "🛍️ 前台：買家極速選物店":
    st.markdown("<h2 style='text-align: center;'>🔥 黑金剛嚴選 ｜ 質感好物所</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>老實說真心話開箱，避雷省錢，只推真正好用的神物！</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 模擬爆款選品清單
    trending_products = [
        {
            "title": "【果果能量】蛋白質威化餅 / 健工聯名新口味",
            "price": "NT$ 259",
            "tag": "#健身必備 #嘴饞救星",
            "desc": "口感超酥脆又不會太甜，減脂期解饞的神級好物，完全不踩雷！",
            "link": "https://s.shopee.tw/your_affiliate_link_1"  # 你的分潤連結
        },
        {
            "title": "【Snoopy 史努比】復古寬鬆純棉短T恤 (多色)",
            "price": "NT$ 399",
            "tag": "#OOTD穿搭 #質感衣著",
            "desc": "磅數很夠、版型超挺不悶熱，日常隨性穿搭或情侶裝都好看。",
            "link": "https://s.shopee.tw/your_affiliate_link_2"  # 你的分潤連結
        },
        {
            "title": "【日常防護】極輕量自動三折防風傘 (抗UV)",
            "price": "NT$ 199",
            "tag": "#雨具推薦 #包包必備",
            "desc": "輕到幾乎感覺不到重量，晴雨兩用，質感霧面手感超好。",
            "link": "https://s.shopee.tw/your_affiliate_link_3"  # 你的分潤連結
        }
    ]

    for item in trending_products:
        st.subheader(item["title"])
        st.caption(item["tag"])
        st.write(f"💰 **特惠價：{item['price']}**")
        st.write(item["desc"])
        st.link_button("🛒 點擊前往蝦皮搶購 (拿優惠)", item["link"], use_container_width=True)
        st.markdown("---")

    st.markdown(
        "<p style='text-align: center; color: silver; font-size: 12px;'>本站所有商品皆為嚴選推薦，透過指定連結購買將獲得微薄分潤支持創作，謝謝妳/你！</p>", 
        unsafe_allow_html=True
    )

# =====================================================================
# 模式 B：後台・AI 爆款與腳本產生器
# =====================================================================
elif app_mode == "🤖 後台：AI 爆款與腳本產生器":
    st.title("🤖 Z世代短影音腳本與選品產生器")
    st.caption("輸入想推廣的商品，一鍵生成 Threads 貼文與 Reels/Shorts 30秒黃金腳本！")
    st.markdown("---")

    # 輸入區
    product_name = st.text_input("輸入商品名稱或賣點：", placeholder="例如：磁吸行動電源、超顯瘦牛仔褲")
    tone = st.selectbox("選擇短影音/文案風格：", ["🔥 真心實話/微毒舌風格", "✨ 質感生活/氛圍感風格", "💸 瘋狂省錢/高CP值風格"])

    if st.button("🚀 一鍵生成 AI 行銷素材", use_container_width=True):
        if product_name:
            st.success("🎉 生成完畢！可以直接複製拿去發佈：")
            
            # 模擬 AI 產出的結果
            st.markdown("### 📱 Threads / IG 爆款貼文")
            st.info(f"最近被這款 **{product_name}** 燒到不行🔥\n老實說一開始還半信半疑，結果收到實品直接驚艷... 真的不是業配，真心推給跟我一樣有這困擾的人！\n\n👇 傳送門幫大家放在這邊，自己去看：\n(放你的蝦皮分潤連結)")

            st.markdown("### 🎬 30秒短影音黃金腳本 (Reels / Shorts)")
            st.warning(
                f"**[0-3秒] 痛點開場**：「如果你還在盲目買 {product_name}，真的會哭死... 這篇看完幫你避雷！」\n\n"
                f"**[3-20秒] 真心開箱**：展示商品特寫，語氣輕快：「重點是它...（帶入 {product_name} 的核心優勢），質感完全不輸大牌！」\n\n"
                f"**[20-30秒] 結尾引導**：「真心覺得這價格很可以，傳送門就在我主頁或留言區，自己去搶！」"
            )
        else:
            st.warning("請先輸入商品名稱喔！")
