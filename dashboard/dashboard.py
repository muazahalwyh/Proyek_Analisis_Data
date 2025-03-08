import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

all_data = pd.read_csv("data/all_data.csv")

st.title(" Dashboard Analisis Penjualan")

# ** 1. Analisis Penjualan Tertinggi Berdasarkan Kategori Produk**
st.subheader("Penjualan Tertinggi Berdasarkan Kategori Produk")

sum_order_items_df = all_data.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "total_sales"})
sum_order_items_df = sum_order_items_df.sort_values(by="total_sales", ascending=False)

top_10_categories = sum_order_items_df.head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x="total_sales", y="product_category_name_english", data=top_10_categories, hue="product_category_name_english", palette="viridis", legend=False)

plt.title("Top 10 Kategori Produk dengan Penjualan Tertinggi", fontsize=14)
plt.xlabel("Jumlah Produk Terjual")
plt.ylabel("Kategori Produk")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(plt)

# ** 2. Analisis Penjualan Tertinggi Berdasarkan Kategori Produk**
st.subheader("Top 10 Wilayah Yang Paling Banyak Pelanggannya")

top_regions = all_data.groupby("customer_state")["customer_unique_id"].nunique().reset_index()
top_regions = top_regions.sort_values(by="customer_unique_id", ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x="customer_unique_id", y="customer_state", data=top_regions.head(10), hue="customer_state", palette="viridis", legend=False)

plt.title("Top 10 Wilayah dengan Jumlah Pelanggan Terbanyak", fontsize=14)
plt.xlabel("Jumlah Pelanggan Unik")
plt.ylabel("Wilayah")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(plt)

st.subheader("Metode Pembayaran Yang Banyak Di Gunakan Oleh Pelanggan")

payment_counts = all_data["payment_type"].value_counts().reset_index()
payment_counts.columns = ["payment_type", "total_transactions"]

plt.figure(figsize=(10, 5))
sns.barplot(x="total_transactions", y="payment_type", data=payment_counts, hue="payment_type", palette="viridis", legend=False)

plt.title("Metode Pembayaran Paling Banyak Digunakan", fontsize=14)
plt.xlabel("Jumlah Transaksi")
plt.ylabel("Metode Pembayaran")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(plt)

st.subheader("Tingkat Kepuasan Pelanggan Terhadap Pelayanan/Produk")

review_scores = all_data['review_score'].value_counts().sort_values(ascending=False)

most_common_score = review_scores.idxmax()

sns.set(style="darkgrid")

plt.figure(figsize=(10, 5))
sns.barplot(x=review_scores.index, y=review_scores.values, hue=review_scores.index, palette="viridis", legend=False)

plt.title("Rating by customers for service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
st.pyplot(plt)

st.subheader(" Kesimpulan ")
st.write("""
- Penjualan produk paling tinggi berdasarkan kategori produk yaitu bed_bath_table dengan jumlah produk terjual sebanyak 12000. Diikuti oleh health_beauty dan sports_leisure. Untuk penjualan produk Terendah yaitu auto dengan jumlah produk terjual sebanyak 4000.
- Berdasarkan wilayah yang memiliki pelanggan terbanyak yaitu wilayah sp dengan jumlah 40000 dan urutan 3 dari bawah yaitu wilayah DF, ES, dan GO. Dan Metode pembayaran paling populer berdasarkan hasil visualisasi tersebut menunjukkan bahwa umumnya metode seperti credit card atau boleto (di Brasil) lebih sering digunakan.
- Kepuasan pelanggan terhadap suatu pelayanan atau produk yang dimiliki bisa di lihat dari rating pelanggan tersebut yang menunjukkan bahwa angka 5 memiliki perhitungan jumlah data terbanyak dari rating lainnya, yang mengartikan bahwa pelanggan sangat puas dengan pelayanan yang telah diberikan. 
""")