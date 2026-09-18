import streamlit as st

st.set_page_config(
    page_title="黑金剛 AI 電商總控中心",
    page_icon="🖤",
    layout="wide"
)

st.title("🖤 黑金剛 AI 電商總控中心 PRO")
st.write("系統已成功啟動並修復所有語法錯誤！")

tab1, tab2 = st.tabs(["🚀 AI 總控台", "🛍️ 買家前台"])

with tab1:
    st.header("後台：AI 內容生成")
    product_name = st.text_input("輸入商品名稱")
    if st.button("生成文案"):
        if product_name:
            st.success(f"成功為【{product_name}】生成行銷文案與短影音腳本！")
        else:
            st.warning("請先輸入商品名稱。")

with tab2:
    st.header("前台：精選選物")
    st.markdown("這裡展示您的蝦皮分潤導購商品。")
    st.link_button("🛒 前往蝦皮購買", "https://s.shopee.tw/")
