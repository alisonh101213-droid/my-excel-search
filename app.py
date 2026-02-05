import streamlit as st
import pandas as pd

# 1. 網頁頁面設定
st.set_page_config(page_title="料號查詢系統", layout="wide")

# 2. 自定義 CSS (還原你的 Canva 藍色風格)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    /* 卡片設計 */
    .st-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 10px solid #1E90FF; /* 主色調藍色 */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    /* 料號標籤 (左上角) */
    .part-number {
        color: #1E90FF;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 5px;
        display: block;
    }
    .content-label {
        color: #555;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 物料查詢系統")

# 3. 側邊欄：上傳檔案
st.sidebar.header("設定")
uploaded_file = st.sidebar.file_uploader("請上傳 Excel 檔案", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # 搜尋框
    search_term = st.text_input("🔍 請輸入料號進行搜尋", "")

    if search_term:
        # 這裡假設你的 Excel 欄位名稱叫 '料號'，請根據實際情況修改
        if '料號' in df.columns:
            results = df[df['料號'].astype(str).str.contains(search_term, case=False)]
            
            if not results.empty:
                st.write(f"找到 {len(results)} 筆結果：")
                
                # 4. 以「一格一格」的卡片形式呈現
                for index, row in results.iterrows():
                    with st.container():
                        # 使用 HTML 語法套用 CSS
                        card_content = f"""
                        <div class="st-card">
                            <span class="part-number">ID: {row['料號']}</span>
                            <hr style="margin: 10px 0;">
                        """
                        # 自動抓取除了「料號」以外的所有欄位資訊
                        for col in df.columns:
                            if col != '料號':
                                card_content += f'<p class="content-label"><b>{col}:</b> {row[col]}</p>'
                        
                        card_content += "</div>"
                        st.markdown(card_content, unsafe_allow_html=True)
            else:
                st.warning("找不到相符的料號。")
        else:
            st.error("Excel 檔案中找不到名為『料號』的欄位，請檢查欄位名稱。")
    else:
        st.info("請在上方輸入料號開始搜尋。")
else:
    st.info("請先從左側上傳 Excel 檔案。")
