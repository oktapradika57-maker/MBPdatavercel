import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Kurva S", layout="wide")

st.title("📊 Dashboard Analisa Kurva S Proyek")
st.markdown("""
Aplikasi ini membantu memvisualisasikan progres proyek. 
Pastikan file Excel Anda memiliki kolom: **'Tanggal', 'Rencana_Mingguan', 'Aktual_Mingguan'**.
""")

# 1. Widget Upload File
uploaded_file = st.file_uploader("Unggah file Excel (Format .xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Membaca data
    df = pd.read_excel(uploaded_file)
    
    # Konversi tanggal
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df = df.sort_values('Tanggal')

    # 2. Perhitungan Kumulatif (Jika data input masih mingguan)
    df['Rencana_Kumulatif'] = df['Rencana_Mingguan'].cumsum()
    df['Aktual_Kumulatif'] = df['Aktual_Mingguan'].cumsum()

    # Tampilkan Data
    with st.expander("Lihat Data yang Diproses"):
        st.dataframe(df)

    # 3. Visualisasi Kurva S dengan Matplotlib
    st.subheader("Grafik Kurva S")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(df['Tanggal'], df['Rencana_Kumulatif'], 
            label='Rencana (Plan)', color='blue', linestyle='--', marker='o')
    ax.plot(df['Tanggal'], df['Aktual_Kumulatif'], 
            label='Aktual (Actual)', color='red', marker='o')
    
    # Pengaturan Styling Grafik
    ax.set_title('Progres Kumulatif Proyek', fontsize=16)
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Progres (%)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot(fig)

    # 4. Analisis Deviasi
    st.subheader("Analisis Deviasi (Aktual - Rencana)")
    df['Deviasi'] = df['Aktual_Kumulatif'] - df['Rencana_Kumulatif']
    
    # Warna berdasarkan positif/negatif
    st.bar_chart(df.set_index('Tanggal')['Deviasi'])
    
    # Summary
    selisih_akhir = df['Deviasi'].iloc[-1]
    if selisih_akhir >= 0:
        st.success(f"Status Proyek: Ahead of Schedule (Deviasi: {selisih_akhir:.2f}%)")
    else:
        st.error(f"Status Proyek: Delay (Deviasi: {selisih_akhir:.2f}%)")

else:
    st.info("Silakan unggah file Excel untuk memulai analisis.")
    st.write("Contoh format data Excel yang diperlukan:")
    contoh = pd.DataFrame({
        'Tanggal': ['2026-01-01', '2026-01-08'],
        'Rencana_Mingguan': [10, 10],
        'Aktual_Mingguan': [8, 12]
    })
    st.table(contoh)
