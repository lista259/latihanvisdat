# %%
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
st.set_page_config(
    page_title="Netflix Content Dashboard",
    page_icon="🎬",
    layout="wide"
)

# %%
# Custom CSS untuk tema Gelap/Merah ala Netflix
st.markdown("""
<style>
.stApp {
background-color: #0e0e0e;
color: white;
}
h1, h2, h3 {
color: #E50914 !important; /* Netflix Red */
}
</style>
""", unsafe_allow_html=True)
st.title("🎬 Netflix Content Strategy Dashboard")
st.markdown("Analisis distribusi konten, tren rilis, dan demografi penonton.")

# %%
@st.cache_data
def generate_netflix_data(rows=1000):
    np.random.seed(42)

    types = np.random.choice(['Movie', 'TV Show'], rows, p=[0.7, 0.3])

    years = np.random.choice(
        range(2010, 2024),
        rows,
        p=[0.02, 0.03, 0.05, 0.05, 0.05, 0.05,
           0.08, 0.08, 0.10, 0.10, 0.12, 0.12, 0.10, 0.05]
    )

    countries = np.random.choice(
        ['United States', 'India', 'United Kingdom', 'Japan', 'South Korea', 'Canada', 'France'],
        rows
    )

    ratings = np.random.choice(
        ['TV-MA', 'TV-14', 'TV-PG', 'R', 'PG-13', 'TV-Y7', 'TV-Y'],
        rows
    )

    duration = np.random.randint(60, 180, rows)

    df = pd.DataFrame({
        'type': types,
        'release_year': years,
        'country': countries,
        'rating': ratings,
        'duration': duration,
        'added_date': pd.date_range(start='2015-01-01', periods=rows)
    })

    return df

# %%
# Load Data
df = generate_netflix_data()

# %%
# Sidebar Filter
st.sidebar.header("Filter Konten")
selected_type = st.sidebar.multiselect("Pilih Tipe:", df['type'].unique(),
default=df['type'].unique())
selected_country = st.sidebar.multiselect("Pilih Negara:", df['country'].unique(),
default=df['country'].unique())

# %%
# Terapkan Filter
filtered_df = df[
(df['type'].isin(selected_type)) &
(df['country'].isin(selected_country))
]

# %%
# Tampilkan Metrik Utama (KPI)
col1, col2, col3 = st.columns(3)
col1.metric("Total Judul", f"{len(filtered_df)}")
col2.metric("Dominasi Tipe", filtered_df['type'].mode()[0])
col3.metric("Tahun Terbanyak", filtered_df['release_year'].mode()[0])
st.divider()

# %%
row1_col1, row1_col2 = st.columns([1, 2])

with row1_col1:
    st.subheader("Distribusi: Movie vs TV Show")

    # Persiapan Data
    type_counts = filtered_df['type'].value_counts()

    # Plot Matplotlib (Pie Chart)
    fig1, ax1 = plt.subplots(figsize=(6, 6))

    ax1.pie(
        type_counts,
        labels=type_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#E50914', '#221f1f'],
        textprops={'color': "white"}
    )

    # Transparan background agar menyatu dengan tema dark mode
    fig1.patch.set_alpha(0)

    st.pyplot(fig1)


# %%
with row1_col2:
    st.subheader("Top 5 Negara Penghasil Konten")

    # Persiapan Data
    country_counts = filtered_df['country'].value_counts().head(5)

    # Plot Bar Chart
    fig2 = plt.figure(figsize=(10, 5))
    sns.barplot(
        x=country_counts.values,
        y=country_counts.index,
        palette="Reds_r"
    )

    plt.xlabel("Jumlah Konten")
    plt.title("Negara Kontributor Terbesar")
    plt.grid(axis='x', linestyle='--', alpha=0.3)

    st.pyplot(fig2)


# %%
# Layout Bawah: Trend Line & Heatmap
st.divider()

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Tren Rilis Konten per Tahun")

    # Persiapan Data: Group by Year & Type
    trend_data = (
        filtered_df
        .groupby(['release_year', 'type'])
        .size()
        .reset_index(name='count')
    )

    # Plot Line Chart
    fig3 = plt.figure(figsize=(10, 5))
    sns.lineplot(
        data=trend_data,
        x='release_year',
        y='count',
        hue='type',
        palette=['#E50914', '#ffffff'],
        linewidth=2.5
    )

    plt.title("Pertumbuhan Konten (2010 - 2023)")
    plt.ylabel("Jumlah Judul Baru")
    plt.grid(True, alpha=0.2)

    st.pyplot(fig3)

    st.info(
        "Insight: Lonjakan konten biasanya terjadi setelah tahun 2016 "
        "seiring ekspansi global Netflix."
    )

with row2_col2:
    st.subheader("Distribusi Rating Usia")

    # Plot Count Plot
    fig4 = plt.figure(figsize=(10, 5))

    # Mengurutkan rating agar rapi
    order_rating = filtered_df['rating'].value_counts().index

    sns.countplot(
        data=filtered_df,
        y='rating',
        order=order_rating,
        palette="dark:red"
    )

    plt.title("Jumlah Konten berdasarkan Rating")

    st.pyplot(fig4)

    st.info(
        "Insight: Rating TV-MA (dewasa) mendominasi, "
        "menunjukkan fokus Netflix pada audiens matang."
    )


# %%
# ==========================================
# 4. TABEL DATA (DETAIL)
# ==========================================
st.divider()
st.subheader("Explore Raw Data")

with st.expander("Klik untuk melihat tabel data lengkap"):
    st.dataframe(filtered_df)


# %%



