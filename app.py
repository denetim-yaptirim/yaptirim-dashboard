import streamlit as st
import pandas as pd
import re

# ✅ Sayfa ayarları — ilk satırda olmalı
st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# ✅ Sağdaki kutucuk: PythonAnywhere bağlantısı ve yenileme butonu
with st.sidebar:
    st.markdown("""
    <div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; font-size: 14px;">
    <b>🔁 Güncel Mail Verisini Getir</b><br><br>
    1. <a href="https://www.pythonanywhere.com/user/Denetim/files/home/Denetim/yaptirim-dashboard/" target="_blank">PythonAnywhere'e Git</a><br>
    2. Giriş yapmanız istenirse aşağıdaki bilgileri kullanın:<br>
    <code>Kullanıcı Adı:</code> <b>Denetim</b><br>
    <code>Şifre:</code> <b>xQPE&6E@9-T*#?d</b><br><br>
    3. <code>cek_yaptirim_mailleri.py</code> dosyasına tıklayın<br>
    4. Sağ üstten <b>▶ Run this file</b> butonuna basın<br>
    5. Geri dönüp aşağıdaki butona tıklayın ⬇
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔁 Verileri Yenile"):
        st.rerun()

# ✅ CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

# ✅ Sayfa başlığı
st.title("📑 Yaptırım Haber Arşivi")

# ✅ Anahtar kelime arama
keyword = st.text_input("🔍 Anahtar kelime ile ara (örnek: iran, rusya, petrol):")

# ✅ Vurgulama fonksiyonu
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

# ✅ Arama varsa filtreli göster
if keyword:
    filtered_df = df[df['body'].str.contains(keyword, case=False, na=False)]
    st.write(f"🔎 {len(filtered_df)} sonuç bulundu.")

    for _, row in filtered_df.iterrows():
        with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
            st.markdown(highlight_keyword(row['body'], keyword), unsafe_allow_html=True)

# ✅ Arama yoksa tüm mailleri sırala
else:
    st.write(f"📋 Toplam {len(df)} mail gösteriliyor:")
    for _, row in df.iterrows():
        with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
            st.markdown(row['body'])
