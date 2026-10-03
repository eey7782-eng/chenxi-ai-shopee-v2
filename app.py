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
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
            background-color: #f4f6f0;
        }
    </style>
""", unsafe_allow_html=True)

# 完美還原設計圖的自定義 HTML/CSS 網頁架構（已優化響應式與高度自適應）
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
            flex-wrap: wrap;
            gap: 15px;
        }
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .nav-logo span {
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 1px;
            color: #ffffff;
        }
        .nav-links {
            display: flex;
            gap: 25px;
            align-items: center;
            flex-wrap: wrap;
        }
        .nav-links a {
            color: #d1dcd4;
            text-decoration: none;
            font-size: 15px;
            transition: color 0.3s;
        }
        .nav-links a:hover, .nav-links a.active {
            color: #ffffff;
            border-bottom: 2px solid #85a382;
            padding-bottom: 3px;
        }
        .btn-booking {
            background-color: #2e5a42 !important;
            color: white !important;
            padding: 8px 18px;
            border-radius: 6px;
            font-weight: bold;
            border: 1px solid #4a7c59;
        }

        /* Hero 主視覺區 */
        .hero {
            position: relative;
            width: 100%;
            height: 480px;
            background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: flex-end;
            justify-content: flex-end;
            padding: 40px;
        }
        .hero-sign {
            background: rgba(40, 30, 20, 0.9);
            color: #fdfbf7;
            padding: 22px 32px;
            border-radius: 8px;
            border: 2px dashed #d4b28c;
            text-align: center;
            transform: rotate(1.5deg);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            max-width: 400px;
        }
        .hero-sign h2 {
            font-size: 24px;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        .hero-sign p {
            font-size: 15px;
            color: #e2d9cd;
        }

        /* 網格卡片區 */
        .container {
            max-width: 1300px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
        }
        .card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        .card-img-wrap {
            position: relative;
            height: 210px;
        }
        .card-img-wrap img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .card-badge {
            position: absolute;
            top: 15px;
            left: 15px;
            background-color: #193124;
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 15px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .card-content {
            padding: 20px;
        }
        .card-content p {
            font-size: 14px;
            color: #4a5d4e;
            line-height: 1.6;
        }

        /* 特別手寫宣傳卡片 */
        .promo-card {
            background: #fffdf9;
            border: 2px dashed #85a382;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 30px;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        }
        .promo-card h3 {
            font-size: 24px;
            color: #193124;
            line-height: 1.6;
            font-family: serif;
        }

        /* 底部 Footer */
        .footer {
            background-color: #193124;
            color: white;
            padding: 30px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 60px;
            flex-wrap: wrap;
            gap: 20px;
        }
        .footer-icons {
            display: flex;
            gap: 25px;
            flex-wrap: wrap;
        }
        .footer-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 13px;
            gap: 4px;
            color: #b8cbb8;
        }
        .footer-banner {
            background-color: #2e5a42;
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px dashed #d4b28c;
            color: #fff;
            font-weight: bold;
            font-size: 15px;
        }

        /* 響應式調整 */
        @media (max-width: 1024px) {
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 600px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .hero {
                height: 380px;
                padding: 20px;
                justify-content: center;
                align-items: center;
            }
            .hero-sign {
                transform: rotate(0deg);
            }
            .navbar {
                padding: 12px 20px;
                justify-content: center;
            }
            .footer {
                justify-content: center;
                text-align: center;
            }
        }
    </style>
</head>
<body>

    <!-- 頂部導覽列 -->
    <div class="navbar">
        <div class="nav-logo">
            <span>⛰️ 山間悠活露營區</span>
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

    <!-- 六大核心與網格卡片區 -->
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
            <div class="footer-item">⛺ <span>露營</span></div>
            <div class="footer-item">☕ <span>咖啡</span></div>
            <div class="footer-item">🥩 <span>烤肉</span></div>
            <div class="footer-item">🎤 <span>卡拉OK</span></div>
            <div class="footer-item">🫖 <span>泡茶</span></div>
            <div class="footer-item">🐓 <span>放山雞</span></div>
            <div class="footer-item">🍎 <span>果園</span></div>
        </div>
        <div class="footer-banner">
            ✨ 歡迎預約，一起創造美好回憶！
        </div>
    </div>

</body>
</html>
"""

# 在 Streamlit 中完美渲染該 HTML/CSS 版面（稍微增加高度確保容納所有內容）
components.html(html_code, height=1420, scrolling=False)
