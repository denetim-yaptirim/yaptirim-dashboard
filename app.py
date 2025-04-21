import streamlit as st
import pandas as pd

st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

st.title("📑 Yaptırım Haber Arşivi")

# Anahtar kelime arama
keyword = st.text_input("🔍 Anahtar kelime ile ara (örnek: iran, rusya, petrol):")

if keyword:
    results = df[df['body'].str.contains(keyword, case=False, na=False)]
    st.write(f"🔎 {len(results)} sonuç bulundu.")
    st.dataframe(results)
else:
    st.write("📋 Son 10 mail:")
    st.dataframe(df.tail(10))
