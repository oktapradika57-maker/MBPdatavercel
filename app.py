import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Kurva S", layout="wide")
st.title("📊 Dashboard Analisa Kurva S Proyek")

uploaded_file = st.file_uploader("Unggah file Excel (Format .xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Menampilkan daftar kolom agar Anda bisa memeriksa nama yang benar
    st.write("Kolom yang terdeteksi di file Anda:", df.columns.tolist())
    
    if st.button("Mulai Analisa"):
        try:
            # Pastikan nama kolom di bawah ini sama persis dengan yang ada di list kolom di atas
            # Jika di Excel Anda namanya 'Date', ganti 'Tanggal' menjadi 'Date'
            col_date = 'Tanggal' 
            col_plan = 'Rencana_Mingguan'
            col_actual = 'Aktual_Mingguan'
            
            df[col_date] = pd.to_datetime(df[col_date])
            df = df.sort_values(col_date)

            df['Rencana_Kumulatif'] = df[col_plan].cumsum()
            df['Aktual_Kumulatif'] = df[col_actual].cumsum()

            # Visualisasi
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df[col_date], df['Rencana_Kumulatif'], label='Rencana', color='blue', linestyle='--')
            ax.plot(df[col_date], df['Aktual_Kumulatif'], label='Aktual', color='red')
            ax.legend()
            st.pyplot(fig)

        except KeyError as e:
            st.error(f"Error: Kolom {e} tidak ditemukan di file Excel Anda. Pastikan nama kolom sesuai dengan yang tertulis di daftar atas.")
