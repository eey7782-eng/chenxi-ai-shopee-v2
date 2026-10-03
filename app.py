import streamlit as st

# 設定頁面配置，採用寬螢幕模式以呈現精美網頁質感
st.set_page_config(
    page_title="山間悠活露營區 - 露營·咖啡·美食·歡樂·放鬆",
    page_icon="⛺",
    layout="wide"
)

# 自定義高質感森林系樣式，完美還原設計圖
st.markdown("""
<style>
    /* 隱藏 Streamlit 預設上方 Header 與 Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }

    /* 整體背景與字體設定 */
    .stApp {
        background-color: #f7f9f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* 頂部導覽列 */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #16261f;
        padding: 15px 40px;
        color: white;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .nav-logo-text h1 {
        font-size: 1.6rem;
        margin: 0;
        color: #ffffff;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .nav-logo-text p {
        font-size: 0.75rem;
        margin: 0;
        color: #a3c1ad;
        letter-spacing: 2px;
    }
    .nav-links {
        display: flex;
        gap: 30px;
        align-items: center;
    }
    .nav-links a {
        color: #d1dcd5;
        text-decoration: none;
        font-size: 0.95rem;
        transition: color 0.3s;
    }
    .nav-links a:hover {
        color: #ffffff;
    }
    .nav-btn {
        background-color: #1e4620;
        color: white !important;
        padding: 8px 20px;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #326237;
        transition: background 0.3s;
    }
    .nav-btn:hover {
        background-color: #26592a;
    }

    /* Hero 主視覺區 */
    .hero-section {
        position: relative;
        width: 100%;
        height: 520px;
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 60px;
    }
    .hero-signboard {
        background: rgba(82, 54, 38, 0.92);
        border: 4px dashed #d4a373;
        padding: 30px 40px;
        border-radius: 12px;
        color: #fff;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        max-width: 420px;
        transform: rotate(2deg);
    }
    .hero-signboard h2 {
        font-size: 2rem;
        margin: 0 0 10px 0;
        color: #faedcd;
        font-family: serif;
    }
    .hero-signboard p {
        font-size: 1.15rem;
        margin: 0;
        color: #e9edc9;
    }

    /* 內容網格區塊 */
    .content-wrapper {
        max-width: 1300px;
        margin: 40px auto;
        padding: 0 20px;
    }
    
    /* 卡片設計 */
    .card-box {
        position: relative;
        border-radius: 14px;
        overflow: hidden;
        height: 270px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .card-box:hover {
        transform: translateY(-5px);
    }
    .card-bg {
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        position: absolute;
        top: 0;
        left: 0;
        filter: brightness(0.85);
    }
    .card-title-badge {
        position: absolute;
        top: 18px;
        left: 50%;
        transform: translateX(-50%);
        background: #16261f;
        border: 2px solid #52796f;
        color: white;
        padding: 6px 22px;
        border-radius: 30px;
        font-size: 1.2rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        white-space: nowrap;
    }
    .card-desc-box {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(transparent, rgba(15, 28, 22, 0.9));
        padding: 20px 20px 15px 20px;
        color: white;
    }
    .card-desc-box p {
        margin: 0;
        font-size: 1rem;
        color: #f1f1f1;
        font-weight: 500;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }

    /* 右下角標語卡片 */
    .quote-card {
        background-color: #ffffff;
        border-radius: 14px;
        height: 270px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border: 2px dashed #b7b7a4;
        margin-bottom: 25px;
    }
    .quote-card h3 {
        font-family: serif;
        color: #2d3748;
        font-size: 1.6rem;
        line-height: 1.5;
        margin: 0;
    }

    /* 底部 Footer 區 */
    .footer-section {
        background-color: #16261f;
        color: white;
        padding: 40px 20px;
        margin-top: 50px;
    }
    .footer-content {
        max-width: 1300px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }
    .footer-icons {
        display: flex;
        gap: 40px;
        align-items: center;
        flex-wrap: wrap;
    }
    .footer-icon-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        font-size: 0.9rem;
        color: #a3c1ad;
    }
    .footer-icon-item span {
        font-size: 1.5rem;
    }
    .footer-banner {
        background: #326237;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: bold;
        color: #faedcd;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# 1. 頂部導覽列
st.markdown("""
<div class="nav-container">
    <div class="nav-brand">
        <span style="font-size: 2.2rem;">⛺</span>
        <div class="nav-logo-text">
            <h1>山間悠活露營區</h1>
            <p>露營 · 咖啡 · 美食 · 歡樂 · 放鬆</p>
        </div>
    </div>
    <div class="nav-links">
        <a href="#home">首頁</a>
        <a href="#facilities">設施介紹</a>
        <a href="#about">園區介紹</a>
        <a href="#news">最新消息</a>
        <a href="#transport">交通資訊</a>
        <a href="#contact">聯絡我們</a>
        <a href="#booking" class="nav-btn">立即預約</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. 主視覺 Hero 區
st.markdown("""
<div class="hero-section" id="home">
    <div class="hero-signboard">
        <h2>大自然 × 美食 × 歡樂</h2>
        <p>給你最輕鬆的度假時光 ♡</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. 六大核心功能網格排版
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# 第一列 (4 張卡片)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card-box">
        <div class="card-bg" style="background-image: url('https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=600&q=80');"></div>
        <div class="card-title-badge">⛺ 露營區</div>
        <div class="card-desc-box">
            <p>寬敞舒適的營位，讓您與大自然零距離。</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card-box">
        <div class="card-bg" style="background-image: url('https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=600&q=80');"></div>
        <div class="card-title-badge">☕ 咖啡廳</div>
        <div class="card-desc-box">
            <p>香醇咖啡·手作甜點，享受悠閒時光。</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card-box">
        <div class="card-bg" style="background-image: url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80');"></div>
        <div class="card-title-badge">🥩 烤肉區</div>
        <div class="card-desc-box">
            <p>新鮮食材·歡樂烤肉，與親朋好友共享美味。</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card-box">
        <div class="card-bg" style="background-image: url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=600&q=80');"></div>
        <div class="card-title-badge">🎤 卡拉OK</div>
        <div class="card-desc-box">
            <p>歡唱無限·盡情放鬆，讓快樂加倍！</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 第二列 (3 張卡片 + 1 個右下角標語卡片)
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown("""
    <div class="card-box">
        <div class="card-bg" style="background-image: url('https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80');"></div>
        <div class="card-title-badge">🫖 泡茶區</div>
        <div class="card-desc-box">
            <p>品茗聊天·放鬆身心，感受茶香的寧靜。</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="card-box">
        <div class="card-bg" style="background-image: url('https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?auto=format&fit=crop&w=600&q=80');"></div>
        <div class="card-title-badge">🐓 放山雞</div>
        <div class="card-desc-box">
            <p>嚴選放山雞，新鮮美味·健康無憂。</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown("""
    <div class="card-box">
        <div class="card-bg" style="background-image: url('https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?auto=format&fit=crop&w=600&q=80');"></div>
        <div class="card-title-badge">🍎 果園區</div>
        <div class="card-desc-box">
            <p>季節水果·現採現吃，體驗自然的甘甜。</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown("""
    <div class="quote-card">
        <h3>遠離城市喧囂<br>來這裡，<br>遇見更好的自己 🤍</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 4. 底部 Footer
st.markdown("""
<div class="footer-section" id="booking">
    <div class="footer-content">
        <div class="footer-icons">
            <div class="footer-icon-item">
                <span>⛺</span>
                <div>露營</div>
            </div>
            <div class="footer-icon-item">
                <span>☕</span>
                <div>咖啡</div>
            </div>
            <div class="footer-icon-item">
                <span>🥩</span>
                <div>烤肉</div>
            </div>
            <div class="footer-icon-item">
                <span>🎤</span>
                <div>卡拉OK</div>
            </div>
            <div class="footer-icon-item">
                <span>🫖</span>
                <div>泡茶</div>
            </div>
            <div class="footer-icon-item">
                <span>🐓</span>
                <div>放山雞</div>
            </div>
            <div class="footer-icon-item">
                <span>🍎</span>
                <div>果園</div>
            </div>
        </div>
        <div class="footer-banner">
            ✨ 歡迎預約 · 一起創造美好回憶！
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
