# ⚡ 黑金鋼 AI 商業自動化總控台 PRO (v8.0)

專為行動裝置與平板設計的「一站式」AI 商業自動化 SaaS 系統。透過平板相簿多選上傳商品相片，結合 Gemini 進行多圖智慧辨識、自動生成跨平台行銷文案，並內建買家極速導購前台與歷史紀錄自動歸檔功能。

## 🌟 核心功能特色
1. **平板相簿多圖選取**：完美支援平板與手機相簿原生介面，可單選或多選多角度商品相片。
2. **AI 智慧辨識填空**：一鍵呼叫 Gemini API 分析多張相片，自動填入商品名稱、建議分類、售價與核心賣點。
3. **跨平台行銷套組生成**：自動產出蝦皮 SEO 賣場文案、Threads 爆款引流貼文與短影音旁白腳本。
4. **歷史紀錄自動歸檔**：系統自動將每次生成的結果以 JSON 格式儲存於本機 `data/history/`，支援隨時載入歷史資料。
5. **買家極速導購前台**：獨立前台展示頁面，一鍵直達分潤連結。

---

## 🛠️ 技術堆疊 (Tech Stack)
- **UI 介面**：Streamlit
- **AI 模型**：Google Gemini (`gemini-1.5-flash`)
- **影像處理**：Pillow (PIL)
- **資料儲存**：Local JSON Persistent Storage (`data/history/`)

---

## 📦 安裝與部署指南

### 1. 建立相依套件檔 (`requirements.txt`)
確保你的專案根目錄包含 `requirements.txt`：
```text
streamlit
google-generativeai
pillow
