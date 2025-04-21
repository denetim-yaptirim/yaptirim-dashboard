import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

st.title("📑 Yaptırım Haber Arşivi")

# Anahtar kelime arama
keyword = st.text_input("🔍 Anahtar kelime ile ara (örnek: iran, rusya, petrol):")

# Kelimeyi vurgulayan fonksiyon
def highlight_keyword(text, keyword):
    if not keyword:
        return text
    highlighted = re.sub(
        f"({re.escape(keyword)})",
        r'<span style="background-color: yellow; font-weight: bold;">\1</span>',
        text,
        flags=re.IGNORECASE
    )
    return highlighted
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# ✅ YENİLEME BUTONU KUTUSU (SAĞDAKİ KÜÇÜK ALANDA)
with st.sidebar:
    st.markdown("""
    <div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; font-size: 14px;">
    <b>🔁 Güncel Mail Verisini Getir</b><br><br>
    1. <a href="https://www.pythonanywhere.com/user/Denetim/files/home/Denetim/yaptirim-dashboard/" target="_blank">PythonAnywhere'e Git</a><br>
    2. <code>cek_yaptirim_mailleri.py</code> dosyasına tıkla<br>
    3. Sağ üstten <b>▶ Run this file</b> butonuna bas<br>
    4. Geri dön, aşağıdaki butona bas ⬇
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔁 Verileri Yenile"):
        st.rerun()

# 📄 CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

st.title("📑 Yaptırım Haber Arşivi")

# Arama varsa filtrele ve göster
if keyword:
    filtered_df = df[df['body'].str.contains(keyword, case=False, na=False)]
    st.write(f"🔎 {len(filtered_df)} sonuç bulundu.")

    for _, row in filtered_df.iterrows():
        with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
            st.markdown(highlight_keyword(row['body'], keyword), unsafe_allow_html=True)

# Arama yoksa tüm mailleri sırala
else:
    st.write(f"📋 Toplam {len(df)} mail gösteriliyor:")
    for _, row in df.iterrows():
        with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
            st.markdown(row['body'])
