import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load dataset
all_data = pd.read_csv("data/all_data.csv")

# Menampilkan logo di sidebar
st.sidebar.image("dashboard/tampilan_hasil/Asset_3.png", caption="Baby Fashion Shop", width=250)

# Konversi kolom tanggal ke format datetime
all_data["order_purchase_timestamp"] = pd.to_datetime(all_data["order_purchase_timestamp"])

# Sidebar untuk filter tanggal
st.sidebar.header("Filter Rentang Waktu")
start_date = st.sidebar.date_input("Tanggal Mulai", all_data["order_purchase_timestamp"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", all_data["order_purchase_timestamp"].max())

if start_date > end_date:
    st.sidebar.error("Tanggal akhir harus lebih besar dari tanggal mulai!")

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = all_data[(all_data["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
                         (all_data["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

st.title("Dashboard Analisis Penjualan")

# **1. Analisis Penjualan Tertinggi Berdasarkan Kategori Produk**
st.subheader("Penjualan Tertinggi Berdasarkan Kategori Produk")

sum_order_items_df = filtered_data.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "total_sales"})
sum_order_items_df = sum_order_items_df.sort_values(by="total_sales", ascending=False)

top_10_categories = sum_order_items_df.head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x="total_sales", y="product_category_name_english", data=top_10_categories, hue="product_category_name_english", palette="viridis", legend=False)
plt.title("Top 10 Kategori Produk dengan Penjualan Tertinggi", fontsize=14)
plt.xlabel("Jumlah Produk Terjual")
plt.ylabel("Kategori Produk")
st.pyplot(plt)

# **2. Analisis Wilayah dengan Pelanggan Terbanyak**
st.subheader("Top 10 Wilayah Yang Paling Banyak Pelanggannya")

top_regions = filtered_data.groupby("customer_state")["customer_unique_id"].nunique().reset_index()
top_regions = top_regions.sort_values(by="customer_unique_id", ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x="customer_unique_id", y="customer_state", data=top_regions.head(10), hue="customer_state", palette="viridis", legend=False)
plt.title("Top 10 Wilayah dengan Jumlah Pelanggan Terbanyak", fontsize=14)
plt.xlabel("Jumlah Pelanggan Unik")
plt.ylabel("Wilayah")
st.pyplot(plt)

# **3. Analisis Metode Pembayaran Terpopuler**
st.subheader("Metode Pembayaran Yang Banyak Digunakan Oleh Pelanggan")

payment_counts = filtered_data["payment_type"].value_counts().reset_index()
payment_counts.columns = ["payment_type", "total_transactions"]

plt.figure(figsize=(10, 5))
sns.barplot(x="total_transactions", y="payment_type", data=payment_counts, hue="payment_type", palette="viridis", legend=False)
plt.title("Metode Pembayaran Paling Banyak Digunakan", fontsize=14)
plt.xlabel("Jumlah Transaksi")
plt.ylabel("Metode Pembayaran")
st.pyplot(plt)

# **4. Analisis Rating Pelanggan**
st.subheader("Tingkat Kepuasan Pelanggan Terhadap Pelayanan/Produk")

review_scores = filtered_data['review_score'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(x=review_scores.index, y=review_scores.values, hue=review_scores.index, palette="viridis", legend=False)
plt.title("Rating oleh Pelanggan untuk Pelayanan", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Jumlah")
st.pyplot(plt)

# **5. RFM Analysis**
st.subheader("RFM Analysis")

# Hitung RFM berdasarkan data yang telah difilter
rfm = filtered_data.groupby("customer_unique_id").agg({
    "order_purchase_timestamp": lambda x: (all_data["order_purchase_timestamp"].max() - x.max()).days,  # Recency
    "order_id": "count",  # Frequency
    "payment_value": "sum"  # Monetary
}).reset_index()

rfm.columns = ["customer_unique_id", "Recency", "Frequency", "Monetary"]

# Segmentasi berdasarkan nilai RFM
rfm["Segment"] = "High"  # Default "hight"
rfm.loc[(rfm["Recency"] <= rfm["Recency"].quantile(0.33)) & 
        (rfm["Frequency"] >= rfm["Frequency"].quantile(0.67)) & 
        (rfm["Monetary"] >= rfm["Monetary"].quantile(0.67)), "Segment"] = "Mid"
rfm.loc[(rfm["Recency"] >= rfm["Recency"].quantile(0.67)) & 
        (rfm["Frequency"] <= rfm["Frequency"].quantile(0.33)) & 
        (rfm["Monetary"] <= rfm["Monetary"].quantile(0.33)), "Segment"] = "Low"

# Hitung jumlah pelanggan per segmen
rfm_counts = rfm["Segment"].value_counts()

# Tampilkan pie chart
st.subheader("Proporsi Segmen Pelanggan")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(rfm_counts, labels=rfm_counts.index, autopct="%1.1f%%", 
       colors=sns.color_palette("coolwarm", len(rfm_counts)))
ax.set_title("Proporsi Segmen Pelanggan")
st.pyplot(fig)

# **Kesimpulan**
st.subheader("Kesimpulan")
st.write("""
- Penjualan produk paling tinggi berdasarkan kategori produk yaitu bed_bath_table.
- Wilayah dengan pelanggan terbanyak adalah SP.
- Metode pembayaran yang paling sering digunakan adalah credit card.
- Pelanggan umumnya memberikan rating tinggi terhadap pelayanan dan produk.
- Segment "High" berisi pelanggan yang baru-baru ini sering berbelanja dan menghabiskan banyak uang, sedangkan segment "Low" berisi pelanggan yang jarang berbelanja dan menghabiskan sedikit uang. Segment "Mid" berada di tengah-tengah, menunjukkan perilaku yang tidak terlalu ekstrem dalam hal Recency, Frequency, dan Monetary.
""")

st.caption('---')
st.caption('&copy; Muazah Al Adawiyah | Laskar AI 2025')
