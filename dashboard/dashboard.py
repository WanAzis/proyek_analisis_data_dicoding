import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from babel.numbers import format_currency


# Helper functions
def create_sum_order_items_df(df):
    sum_order_items_df = all_df.groupby("product_category_name_english").product_id.count().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_monthly_orders_2018_df(df):
    monthly_orders_df = all_df.resample('M', on='order_purchase_timestamp').agg({
        'order_id': 'nunique',
        'price': 'sum'
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%B-%Y') 
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)

    monthly_orders_2018_df = monthly_orders_df[monthly_orders_df['order_purchase_timestamp'].str.contains('2018')]

    return monthly_orders_2018_df

def create_customer_geolocation_df(customers_df,geolocation_df):
    customers_geo_df = pd.merge(customers_df, geolocation_df, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')
    geometry = [Point(xy) for xy in zip(customers_geo_df.geolocation_lng, customers_geo_df.geolocation_lat)]
    customers_geo_df = gpd.GeoDataFrame(customers_geo_df, crs="EPSG:4326", geometry=geometry)

    return customers_geo_df

# Load cleaned data
all_df = pd.read_csv("./dashboard/all_data.csv")
# customers_df = pd.read_csv("./data/customers_dataset.csv")
# geolocation_df = pd.read_csv("./data/geolocation_dataset.csv")

all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# # Menyiapkan berbagai dataframe
monthly_orders_2018_df = create_monthly_orders_2018_df(all_df)
sum_order_items_df = create_sum_order_items_df(all_df)
# customers_geo_df = create_customer_geolocation_df(customers_df,geolocation_df)

st.title('E-Commerce Dashboard 💲')
st.subheader('Monthly Orders in 2018')

# Performa penjualan
st.text('Number of Orders per Month (2018)')
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(
    monthly_orders_2018_df["order_purchase_timestamp"],
    monthly_orders_2018_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)

st.text('Total Revenue per Month in 2018 (AUD)')
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(
    monthly_orders_2018_df["order_purchase_timestamp"],
    monthly_orders_2018_df["revenue"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)

# Performa produk
st.text('Best and Worst Performing Product by Number of Sales')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="product_id", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

# Persebaran customer
st.text("Persebaran customer")
# st.map(customers_geo_df)

st.image("./data/persebaran_pelanggan.png")

st.markdown(
    """
    Map/peta persebaran customer e-commerce ditampilkan dalam bentuk gambar  
    dan tidak diproses secara langsung karena workload yang sangat berat
    """
)

st.caption('Copyright (c) Azis 2023')