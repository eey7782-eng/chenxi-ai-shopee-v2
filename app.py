import streamlit as st

# 設定頁面配置
st.set_page_config(
    page_title="山林漫活休閒露營區",
    page_icon="🌲",
    layout="centered"
)

# 主標題
st.markdown("### 🌲 歡迎來到【山林漫活休閒露營區】")

# 副標題說明
st.markdown(
    "離塵不離城，結合自然果園、在地美食與放鬆休閒的世外桃源！"
)

# 營區主視覺圖片
st.image(
    "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=1000&q=80",
    use_container_width=True
)

# 亮點介紹標題
st.markdown("### ✨ 營區亮點介紹")

# 亮點 1
with st.container(border=True):
    st.markdown("##### ☕ 悠閒咖啡與泡茶")
    st.markdown("手沖咖啡與高山茶席，享受慢活時光。")

# 亮點 2
with st.container(border=True):
    st.markdown("##### 🎤 歡樂烤肉與卡拉OK")
    st.markdown("和親朋好友一起開心歡唱、大快朵頤。")

# 亮點 3
with st.container(border=True):
    st.markdown("##### 🍎 自然果園與放山雞")
    st.markdown("體驗果園採果樂趣，品嚐在地美味放山雞。")
