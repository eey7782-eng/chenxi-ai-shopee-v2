import streamlit as st
import streamlit.components.v1 as components

# 設定頁面配置，採用寬螢幕模式以呈現精美網頁質感
st.set_page_config(
    page_title="山間悠活露營區 - 露營、咖啡、美食、歡樂、放鬆",
    page_icon="⛺",
    layout="wide"
)

# 隱藏 Streamlit 預設的上方 Header 與 Footer，打造純粹的全螢幕質感
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
            background-color: #f4f6f0;
        }
    </style>
""", unsafe_allow_html=True,)

# 精準對應設計圖的 HTML/CSS 網頁架構
html_code = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>山間悠活露營區</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #f4f6f0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #2c3e2d;
            overflow-x: hidden;
        }

        /* 頂部導覽列 */
        .navbar {
            background-color: #193124;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 40px;
            color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .nav-logo img {
            height: 42px;
            width: auto;
        }
        .nav-logo-text {
            display: flex;
            flex-direction: column;
        }
        .nav-logo-text span.title {
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 1px;
            color: #ffffff;
            line-height: 1.2;
        }
        .nav-logo-text span.subtitle {
            font-size: 11px;
            color: #b8cbb8;
            letter-spacing: 2px;
        }
        .nav-links {
            display: flex;
            gap: 25px;
            align-items: center;
        }
        .nav-links a {
            color: #d1dcd4;
            text-decoration: none;
            font-size: 15px;
            transition: color 0.3s;
        }
        .nav-links a:hover, .nav-links a.active {
            color: #ffffff;
        }
        .nav-links a.active {
            border-bottom: 2px solid #85a382;
            padding-bottom: 3px;
        }
        .btn-booking {
            background-color: #2e5a42 !important;
            color: white !important;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
            border: 1px solid #4a7c59;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Hero 主視覺區 */
        .hero {
            position: relative;
            width: 100%;
            height: 480px;
            background-image: url('https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: flex-end;
            justify-content: flex-end;
            padding: 40px;
        }
        .hero-sign {
            background: rgba(45, 33, 22, 0.9);
            color: #fdfbf7;
            padding: 20px 30px;
            border-radius: 6px;
            border: 2px dashed #d4b28c;
            text-align: center;
            transform: rotate(2deg);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            max-width: 360px;
        }
        .hero-sign h2 {
            font-size: 22px;
            margin-bottom: 6px;
            letter-spacing: 1px;
        }
        .hero-sign p {
            font-size: 15px;
            color: #e2d9cd;
        }

        /* 網格卡片區 */
        .container {
            max-width: 1320px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 22px;
        }
        .card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06);
            transition: transform 0.3s;
            position: relative;
        }
        .card:hover {
            transform: translateY(-4px);
        }
        .card-img-wrap {
            position: relative;
            height: 200px;
        }
        .card-img-wrap img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .card-badge {
            position: absolute;
            top: 14px;
            left: 14px;
            background-color: #193124;
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 15px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card-content {
            padding: 16px 18px;
        }
        .card-content p {
            font-size: 14px;
            color: #4a5d4e;
            line-height: 1.5;
        }

        /* 右下角手寫質感標語卡片 */
        .promo-card {
            background: #fffdf9;
            border: 2px dashed #85a382;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 30px;
            text-align: center;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04);
            position: relative;
        }
        .promo-card h3 {
            font-size: 24px;
            color: #193124;
            line-height: 1.6;
            font-family: serif;
        }
        .promo-card::after {
            content: "🌿";
            position: absolute;
            bottom: 15px;
            left: 20px;
            font-size: 22px;
        }

        /* 底部 Footer */
        .footer {
            background-color: #193124;
            color: white;
            padding: 25px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 50px;
        }
        .footer-icons {
            display: flex;
            gap: 40px;
            align-items: center;
        }
        .footer-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 13px;
            gap: 6px;
            color: #b8cbb8;
        }
        .footer-item span.icon {
            font-size: 20px;
        }
        .footer-banner {
            background-color: #2e5a42;
            padding: 12px 24px;
            border-radius: 6px;
            border: 1px dashed #d4b28c;
            color: #fff;
            font-weight: bold;
            font-size: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }

        @media (max-width: 1100px) {
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>

    <!-- 頂部導覽列 -->
    <div class="navbar">
        <div class="nav-logo">
            <span style="font-size: 32px;">⛺</span>
            <div class="nav-logo-text">
                <span class="title">山間悠活露營區</span>
                <span class="subtitle">露營 ‧ 咖啡 ‧ 美食 ‧ 歡樂 ‧ 放鬆</span>
            </div>
        </div>
        <div class="nav-links">
            <a href="#" class="active">首頁</a>
            <a href="#">設施介紹</a>
            <a href="#">園區介紹</a>
            <a href="#">最新消息</a>
            <a href="#">交通資訊</a>
            <a href="#">聯絡我們</a>
            <a href="#" class="btn-booking">📅 立即預約</a>
        </div>
    </div>

    <!-- Hero 主視覺 -->
    <div class="hero">
        <div class="hero-sign">
            <h2>大自然 × 美食 × 歡樂</h2>
            <p>給你最放鬆的度假時光 ♡</p>
        </div>
    </div>

    <!-- 六大核心與網格卡片區 (共 8 格排版) -->
    <div class="container">
        <div class="grid">
            <!-- 1. 露營區 -->
            <div class="card">
                <div class="card-img-wrap">
                    <img src="https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=600&q=80" alt="露營區">
                    <div class="card-badge">⛺ 露營區</div>
                </div>
                <div class="card-content">
                    <p>寬敞舒適的營位，讓您與大自然零距離。</p>
                </div>
            </div>

            <!-- 2. 咖啡廳 -->
            <div class="card">
                <div class="card-img-wrap">
                    <img src="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=600&q=80" alt="咖啡廳">
                    <div class="card-badge">☕ 咖啡廳</div>
                </div>
                <div class="card-content">
                    <p>香醇咖啡、手作甜點，享受悠閒時光。</p>
                </div>
            </div>

            <!-- 3. 烤肉區 -->
            <div class="card">
                <div class="card-img-wrap">
                    <img src="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=600&q=80" alt="烤肉區">
                    <div class="card-badge">🥩 烤肉區</div>
                </div>
                <div class="card-content">
                    <p>新鮮食材，歡樂烤肉，與親朋好友共享美味。</p>
                </div>
            </div>

            <!-- 4. 卡拉OK -->
            <div class="card">
                <div class="card-img-wrap">
                    <img src="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=600&q=80" alt="卡拉OK">
                    <div class="card-badge">🎤 卡拉OK</div>
                </div>
                <div class="card-content">
                    <p>歡唱無限，盡情放鬆，讓快樂加倍！</p>
                </div>
            </div>

            <!-- 5. 泡茶區 -->
            <div class="card">
                <div class="card-img-wrap">
                    <img src="https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80" alt="泡茶區">
                    <div class="card-badge">🫖 泡茶區</div>
                </div>
                <div class="card-content">
                    <p>品茗聊天，放鬆身心，感受茶香的寧靜。</p>
                </div>
            </div>

            <!-- 6. 放山雞 -->
            <div class="card">
                <div class="card-img-wrap">
                    <img src="https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?auto=format&fit=crop&w=600&q=80" alt="放山雞">
                    <div class="card-badge">🐓 放山雞</div>
                </div>
                <div class="card-content">
                    <p>嚴選放山雞，新鮮美味，健康無憂。</p>
                </div>
            </div>

            <!-- 7. 果園區 -->
            <div class="card">
                <div class="card-img-wrap">
                    <img src="https://images.unsplash.com/photo-1610397646682-f4a471fcffde?auto=format&fit=crop&w=600&q=80" alt="果園區">
                    <div class="card-badge">🍎 果園區</div>
                </div>
                <div class="card-content">
                    <p>季節水果，現採現吃，體驗自然的甘甜。</p>
                </div>
            </div>

            <!-- 8. 右下角手寫質感標語卡片 -->
            <div class="promo-card">
                <h3>🌿 遠離城市喧囂<br>來這裡，<br>遇見更好的自己 ♡</h3>
            </div>
        </div>
    </div>

    <!-- 底部 Footer 資訊列 -->
    <div class="footer">
        <div class="footer-icons">
            <div class="footer-item"><span class="icon">⛺</span><span>露營</span></div>
            <div class="footer-item"><span class="icon">☕</span><span>咖啡</span></div>
            <div class="footer-item"><span class="icon">🥩</span><span>烤肉</span></div>
            <div class="footer-item"><span class="icon">🎤</span><span>卡拉OK</span></div>
            <div class="footer-item"><span class="icon">🫖</span><span>泡茶</span></div>
            <div class="footer-item"><span class="icon">🐓</span><span>放山雞</span></div>
            <div class="footer-item"><span class="icon">🍎</span><span>果園</span></div>
        </div>
        <div class="footer-banner">
            ✨ 歡迎預約，一起創造美好回憶！
        </div>
    </div>

</body>
</html>
"""

# 在 Streamlit 中完美渲染該 HTML/CSS 版面（設定精準高度 1320px 確保完美呈現）
components.html(html_code, height=1320, scrolling=False)
