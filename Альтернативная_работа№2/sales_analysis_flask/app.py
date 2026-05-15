import pandas as pd
import os
from flask import Flask, render_template, request

app = Flask(__name__)

file_path = "data/sales_data_sample.csv"


if not os.path.exists(file_path):
    raise FileNotFoundError("CSV файл не найден")


df = pd.read_csv(file_path, encoding="latin1")


df = df.fillna("Unknown")


quantity_col = "QUANTITYORDERED"
price_col = "PRICEEACH"
product_col = "PRODUCTCODE"
category_col = "PRODUCTLINE"
city_col = "CITY"


df["total_price"] = df[quantity_col] * df[price_col]


@app.route("/")
def index():
    city_filter = request.args.get("city")

    filtered_df = df


    if city_filter:
        filtered_df = df[df[city_col].str.contains(city_filter, case=False, na=False)]


    total_orders = len(filtered_df)
    total_revenue = filtered_df["total_price"].sum()

    top_product = filtered_df.groupby(product_col)[quantity_col].sum().idxmax()

    top_category = filtered_df.groupby(category_col)["total_price"].sum().idxmax()

    top_city = filtered_df[city_col].value_counts().idxmax()


    category_table = filtered_df.groupby(category_col)["total_price"].sum().reset_index()

    return render_template(
        "index.html",
        total_orders=total_orders,
        total_revenue=round(total_revenue, 2),
        top_product=top_product,
        top_category=top_category,
        top_city=top_city,
        table=filtered_df.to_html(classes="table", index=False),
        category_table=category_table.to_html(classes="table", index=False)
    )


if __name__ == "__main__":
    app.run(debug=True)