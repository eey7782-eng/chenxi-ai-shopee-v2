# =====================================================================
# Z世代極速選物與導購網頁 (app.py)
# 專為手機瀏覽、年輕人社群流量（Threads/Shorts）打造的極簡導購前台
# =====================================================================

import streamlit as st

# 設定網頁版面 (手機優先)
st.set_page_config(
    page_title="黑金剛嚴選 ｜ 質感好物所",
    page_icon="🔥",
    layout="centered"
)

# 頂部極簡視覺
st.markdown("<h2 style='text-align: center;'>🔥 黑金剛嚴選 ｜ 質感好物所</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>老實說真心話開箱，避雷省錢，只推真正好用的神物！</p>", unsafe_allow_html=True)
st.markdown("---")

# 模擬年輕人熱愛的爆款選品資料庫
trending_products = [
    {
        "title": "【果果能量】蛋白質威化餅 / 健工聯名新口味",
        "price": "NT$ 259",
        "tag": "#健身必備 #嘴饞救星",
        "desc": "口感超酥脆又不會太甜，減脂期解饞的神級好物，完全不踩雷！",
        "link": "https://s.shopee.tw/your_affiliate_link_1"  # 替換成你的蝦皮分潤連結
    },
    {
        "title": "【Snoopy 史努比】復古寬鬆純棉短T恤 (多色)",
        "price": "NT$ 399",
        "tag": "#OOTD穿搭 #質感衣著",
        "desc": "磅數很夠、版型超挺不悶熱，日常隨性穿搭或情侶裝都好看。",
        "link": "https://s.shopee.tw/your_affiliate_link_2"  # 替換成你的蝦皮分潤連結
    },
    {
        "title": "【日常防護】極輕量自動三折防風傘 (抗UV)",
        "price": "NT$ 199",
        "tag": "#雨具推薦 #包包必備",
        "desc": "輕到幾乎感覺不到重量，晴雨兩用，質感霧面手感超好。",
        "link": "https://s.shopee.tw/your_affiliate_link_3"  # 替換成你的蝦皮分潤連結
    }
]

# 迴圈渲染商品卡片
for item in trending_products:
    st.subheader(item["title"])
    st.caption(item["tag"])
    st.write(f"💰 **特惠價：{item['price']}**")
    st.write(item["desc"])
    
    # 手機上點了就直接跳轉到你的蝦皮分潤連結
    st.link_button("🛒 點擊前往蝦皮搶購 (拿優惠)", item["link"], use_container_width=True)
    st.markdown("---")

# 頁尾資訊
st.markdown(
    "<p style='text-align: center; color: silver; font-size: 12px;'>本站所有商品皆為嚴選推薦，透過指定連結購買將獲得微薄分潤支持創作，謝謝妳/你！</p>", 
    unsafe_allow_html=True
)
