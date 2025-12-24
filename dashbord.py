import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv", delimiter=";")
    hour_df = pd.read_csv("hour.csv", delimiter=";")
    
    # Tambahkan dayfirst=True agar Python tahu formatnya Hari/Bulan/Tahun
    day_df['dteday'] = pd.to_datetime(day_df['dteday'], dayfirst=True)
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], dayfirst=True)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# --- SIDEBAR ---
st.sidebar.header("Filter Data")
# Filter Rentang Waktu
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

try:
    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
except ValueError:
    st.error("Pilih rentang waktu yang valid (Mulai - Selesai)")
    st.stop()

# Filter data berdasarkan input sidebar
main_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & 
                 (day_df["dteday"] <= pd.to_datetime(end_date))]

# --- MAIN PAGE ---
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown(f"Menampilkan data dari **{start_date}** hingga **{end_date}**")

# Metrik Sederhana
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Total Rental", value=main_df['cnt'].sum())
with col_m2:
    st.metric("Rata-rata Rental", value=round(main_df['cnt'].mean()))
with col_m3:
    st.metric("Total Casual", value=main_df['casual'].sum())

st.divider()

# Layout Visualisasi
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan")
    fig, ax = plt.subplots()
    sns.barplot(data=main_df, x='weathersit', y='cnt', palette='viridis', ax=ax)
    ax.set_xlabel("Kondisi Cuaca (1: Cerah, 2: Mendung, 3: Hujan)")
    ax.set_ylabel("Rata-rata Sewa")
    st.pyplot(fig)
    st.info("**Insight:** Penyewaan memuncak saat cuaca cerah (1) dan turun drastis saat cuaca buruk.")

with col2:
    st.subheader("Pola Jam: Hari Kerja vs Libur")
    # Menggunakan data jam yang difilter juga
    hour_filtered = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & 
                            (hour_df["dteday"] <= pd.to_datetime(end_date))]
    fig, ax = plt.subplots()
    sns.lineplot(data=hour_filtered, x='hr', y='cnt', hue='workingday', ax=ax)
    ax.set_xticks(range(0, 24, 3))
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Sewa")
    st.pyplot(fig)
    st.info("**Insight:** Hari kerja (1) memuncak pada jam sibuk (08:00 & 17:00).")

# Analisis Lanjutan: Manual Clustering
st.divider()
st.subheader("Segmentasi Intensitas Permintaan (Manual Clustering)")
main_df['rental_category'] = pd.cut(main_df['cnt'], bins=[0, 2000, 5000, 10000], labels=['Low', 'Medium', 'High'])

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=main_df, x='temp', y='cnt', hue='rental_category', palette='rocket', ax=ax)
ax.set_title("Hubungan Suhu dan Jumlah Sewa Berdasarkan Kategori")
st.pyplot(fig)


st.caption("Copyright (c) Ilma Sari 2024")
