import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ========================== KONFIGURASI DASHBOARD ==========================
st.set_page_config(layout="wide") #Set layout menjadi lebar
st.title("📊 Dashboard Analisis Peminjaman Sepeda")
st.write("Dashboard ini menyajikan analisis pola peminjaman sepeda berdasarkan musim dan jam dalam sehari.")

# ========================== MEMUAT DATASET ==========================
# Mengunduh dataset harian dan per jam
url_day = "https://raw.githubusercontent.com/zarifaayyasy/BikeSharing/refs/heads/main/Data/day.csv"
url_hour = "https://raw.githubusercontent.com/zarifaayyasy/BikeSharing/refs/heads/main/Data/hour.csv"

df_day = pd.read_csv(url_day, parse_dates=["dteday"])
df_hour = pd.read_csv(url_hour)

# Mapping musim agar lebih mudah dipahami
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df_day["season"] = df_day["season"].map(season_labels)
df_hour["season"] = df_hour["season"].map(season_labels)

# ========================== FILTER INTERAKTIF ==========================
st.sidebar.header("🔎 Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim", ["All"] + list(season_labels.values()))
selected_hour = st.sidebar.slider("Pilih Rentang Jam", 0, 23, (0, 23))

# Filter dataset berdasarkan input pengguna
if selected_season != "All":
    df_day_filtered = df_day[df_day["season"] == selected_season]
    df_hour_filtered = df_hour[df_hour["season"] == selected_season]
else:
    df_day_filtered = df_day
    df_hour_filtered = df_hour

df_hour_filtered = df_hour_filtered[(df_hour_filtered["hr"] >= selected_hour[0]) & (df_hour_filtered["hr"] <= selected_hour[1])]

# ========================== ANALISIS MUSIM ==========================
st.header("📅 Analisis Berdasarkan Musim")
seasonal_rentals = df_day_filtered.groupby("season")["cnt"].sum().reset_index()
seasonal_rentals = seasonal_rentals.set_index("season").reindex(season_labels.values()).reset_index()

fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=seasonal_rentals, x="season", y="cnt", palette="Blues", ax=ax1)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Peminjaman Sepeda")
ax1.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
ax1.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig1)

# ========================== ANALISIS JAM ==========================
st.header("⏰ Analisis Berdasarkan Waktu dalam Sehari")
avg_rentals_hour = df_hour_filtered.groupby("hr")["cnt"].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=avg_rentals_hour, x="hr", y="cnt", marker="o", color="b", linewidth=2, ax=ax2)
ax2.set_xticks(range(0, 24))
ax2.set_xlabel("Jam dalam Sehari")
ax2.set_ylabel("Rata-rata Peminjaman Sepeda")
ax2.set_title("Pola Peminjaman Sepeda dalam Sehari")
ax2.grid(True)
st.pyplot(fig2)
