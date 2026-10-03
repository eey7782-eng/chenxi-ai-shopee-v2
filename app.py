import streamlit as st

# 設定頁面配置，採用寬螢幕模式以呈現精美網頁質感
st.set_page_config(
    page_title="山間悠活露營區 - 露營・咖啡・美食・歡樂・放鬆",
    page_icon="⛺",
    layout="wide"
)

# 自定義 CSS 樣式，精準打造高質感綠意森林系網頁外觀
st.markdown("""
    <style>
    /* 隱藏 Streamlit 預設的上方 Header 與 Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f7f9f6;
    }
    
    /* 頂部導覽列 */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #1f3a2c;
        padding: 15px 40px;
        color: white;
        border-bottom: 3px solid #2e5a42;
    }
    .nav-logo {
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .nav-links a {
        color: #ffffff;
        text-decoration: none;
        margin: 0 15px;
        font-size: 16px;
    }
    .nav-btn {
        background-color: #27ae60;
        color: white;
        padding: 8px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
    }
    
    /* 主視覺 Banner 區 */
    .hero-section {
        position: relative;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .hero-img {
        width: 100%;
        max-height: 500px;
        object-fit: cover;
        border-radius: 0 0 15px 15px;
    }
    
    /* 卡片樣式 */
    .feature-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .card-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
    }
    .card-content {
        padding: 20px;
    }
    .card-title {
        font-size: 20px;
        font-weight: bold;
        color: #1f3a2c;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 14px;
        color: #666;
        line-height: 1.5;
    }
    
    /* 口號卡片 */
    .quote-card {
        background: #ffffff;
        border: 2px dashed #a8c3b0;
        border-radius: 12px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 40px;
        color: #2e5a42;
    }
    
    /* 底部導覽列 */
    .footer-bar {
        background-color: #1f3a2c;
        color: white;
        padding: 25px 40px;
        margin-top: 40px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 4px solid #27ae60;
    }
    .footer-item {
        text-align: center;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 頂部導覽列 Navbar
st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">⛰️ 山間悠活露營區</div>
        <div class="nav-links">
            <a href="#">首頁</a>
            <a href="#">設施介紹</a>
            <a href="#">園區介紹</a>
            <a href="#">最新消息</a>
            <a href="#">交通資訊</a>
            <a href="#">聯絡我們</a>
        </div>
        <div>
            <a href="#" class="nav-btn">📅 立即預約</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. 主視覺大圖 Banner 區 (使用設計圖對應的 AI 風格視覺)
st.markdown("""
    <div style="position: relative; width: 100%; margin-bottom: 30px;">
        <img src="https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1600&q=80" style="width: 100%; height: 480px; object-fit: cover; filter: brightness(0.9);">
        <div style="position: absolute; bottom: 35px; right: 45px; background: rgba(31, 58, 44, 0.85); padding: 18px 30px; border-radius: 10px; border-left: 5px solid #27ae60; color: white;">
            <h2 style="margin: 0; font-size: 26px; font-weight: bold;">大自然 × 美市 × 歡樂</h2>
            <p style="margin: 5px 0 0 0; font-size: 16px; color: #d4edda;">給你最放鬆的度假時光 🍃</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 3. 七大特色網格區 (Grid Layout)
# 第一行：露營區、咖啡廳、烤肉區、卡拉OK
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=600&q=80" class="card-img">
            <div class="card-content">
                <div class="card-title">⛺ 露營區</div>
                <div class="card-desc">寬敞舒適的營位，讓您與大自然零距離[span_1](start_span)[span_1](end_span)。</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=600&q=80" class="card-img">
            <div class="card-content">
                <div class="card-title">☕ 咖啡廳</div>
                <div class="card-desc">香醇咖啡、手作甜點，享受悠閒時光[span_2](start_span)[span_2](end_span)。</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=600&q=80" class="card-img">
            <div class="card-content">
                <div class="card-title">🥩 烤肉區</div>
                <div class="card-desc">新鮮食材、歡樂烤肉，與親朋好友共享美味[span_3](start_span)[span_3](end_span)。</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=600&q=80" class="card-img">
            <div class="card-content">
                <div class="card-title">🎤 卡拉OK</div>
                <div class="card-desc">歡唱無限、盡情放鬆，讓快樂加倍！[span_4](start_span)[span_4](end_span)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# 第二行：泡茶區、放山雞、果園區、品牌精神看板
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80" class="card-img">
            <div class="card-content">
                <div class="card-title">🍵 泡茶區</div>
                <div class="card-desc">品茗聊天、放鬆身心，感受茶香的寧靜[span_5](start_span)[span_5](end_span)。</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1548550023-2bdb8c5be188?auto=format&fit=crop&w=600&q=80" class="card-img">
            <div class="card-content">
                <div class="card-title">🐔 放山雞</div>
                <div class="card-desc">嚴選放山雞，新鮮美味、健康無憂[span_6](start_span)[span_6](end_span)。</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown("""
        <div class="feature-card">
            <img src="https://images.unsplash.com/photo-1610348725531-843dff563e2c?auto=format&fit=crop&w=600&q=80" class="card-img">
            <div class="card-content">
                <div class="card-title">🍊 果園區</div>
                <div class="card-desc">季節水果、現採現吃，體驗自然的甘甜[span_7](start_span)[span_7](end_span)。</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown("""
        <div class="quote-card">
            <h3 style="color: #1f3a2c; margin-bottom: 10px; font-weight: bold;">遠離城市喧囂</h3>
            <p style="color: #4f6f52; font-size: 15px; line-height: 1.6;">來這裡，<br>遇見更好的自己 💚</p>
        </div>
    """, unsafe_allow_html=True)

# 4. 底部特色功能列 Footer
st.markdown("""
    <div class="footer-bar">
        <div class="footer-item">⛺ 露營區</div>
        <div style="color: #4e7c60;">|</div>
        <div class="footer-item">☕ 咖啡廳</div>
        <div style="color: #4e7c60;">|</div>
        <div class="footer-item">🥩 烤肉區</div>
        <div style="color: #4e7c60;">|</div>
        <div class="footer-item">🎤 卡拉OK</div>
        <div style="color: #4e7c60;">|</div>
        <div class="footer-item">🍵 泡茶區</div>
        <div style="color: #4e7c60;">|</div>
        <div class="footer-item">🐔 放山雞</div>
        <div style="color: #4e7c60;">|</div>
        <div class="footer-item">🍊 果園</div>
        <div style="background-color: #27ae60; padding: 10px 20px; border-radius: 8px; font-weight: bold; color: white;">
            ✨ 歡迎預約，一起創造美好回憶！[span_8](start_span)[span_8](end_span)
        </div>
    </div>
""", unsafe_allow_html=True)
