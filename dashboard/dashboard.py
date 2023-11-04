import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.title('e-Commerce Report in Brazil from 2016-2018')

#Making method for Visualization in Streamlit
#Annual Report from 2016 to 2018
def IncomefromOrder(df):
    monthly_order_df=df.resample(rule='M',on='order_purchase_timestamp').agg({
    'order_id':'nunique',
    'price':'sum'})
    monthly_order_df.index = monthly_order_df.index.strftime('%Y-%m')
    monthly_order_df=monthly_order_df.reset_index()
    monthly_order_df=monthly_order_df.rename(columns={
        'order_id':'order_purchase',
        'price':'revenue'
        }) 
    return monthly_order_df

def highestrevenue(df):
    product_price=df.groupby(['product_category_name']).agg({
    'price':'sum',
    'freight_value':'sum'
    }).sort_values(by='price',ascending=False).reset_index()
    return product_price

def bycitydf(df):
    by_citydf=df.groupby(by='customer_city').customer_id.nunique().reset_index()
    by_citydf.rename(columns={
        'customer_id':'customer_count'
        },inplace=True)
    by_citydf = by_citydf.sort_values(by='customer_count',ascending=False).head()
    return by_citydf

def bypayment(df):
    customer_card=df.groupby(by='payment_type').customer_id.nunique().sort_values(ascending=False).reset_index()
    return customer_card

#Import Data
all_df = pd.read_csv(r'C:\Users\USER\Documents\DataScience\Dicoding\Latihan\Project\Dashboard\all_data.csv')
#Implementing Data
datetime_columns = ["order_purchase_timestamp", "order_delivered_carrier_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    start, enddate = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
#Variable for filtering dataFrame
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start)) & 
                (all_df["order_purchase_timestamp"] <= str(enddate))]

#Calling method with new Variabel
revenuedf=IncomefromOrder(main_df)
highdf=highestrevenue(main_df)
citydf=bycitydf(main_df)
paymentdf=bypayment(main_df)

#Plot Revenue
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = revenuedf.order_purchase.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(revenuedf.revenue.sum(), "$", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    revenuedf["order_purchase_timestamp"],
    revenuedf["order_purchase"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15,rotation = 90)
 
st.pyplot(fig)


#Plot Best and Worst Product
st.subheader("Best & Worst Performing Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="price", y="product_category_name", data=highdf.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="price", y="product_category_name", data=highdf.sort_values(by="price", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

# Plot the biggest order city
st.subheader("Customer Demographics")

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="customer_city",
    data=citydf.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)

ax.set_title("Number of Customer by City", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Plot the payment
st.subheader("Payment Method")

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_id", 
    y="payment_type",
    data=paymentdf.sort_values(by="customer_id", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by Payment", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)