# Reflection
# 1. The decision I found most uncertain was filling a missing
#    quantity with the average. Before deciding, I would want to
#    know the typical quantity sold for the same product.
#
# 2. I reviewed my comments and explained why I dropped rows
#    missing order IDs or dates and removed quantities of 9,999.
#
# 3. I was surprised that revenue ranged from -3,268 to 59,994
#    before removing placeholders. This matters because
#    negative revenue can represent real returns, while placeholder values can distort the results.

import pandas as pd

# Exercise 1: Inspect the data
df = pd.read_csv("data/messy_sales.csv")

df.info()
print(df.isnull().sum())
# Data quality issues:
# 1. Order ID has 31 missing values, and Order Date has 25.
# 2. Quantity Sold has 94 missing values.
# 3. Customer ID has 362 missing values.
# 4. Unit Price is stored as text instead of a numeric type.

# Exercise 2: Standardize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")
print(df.columns.tolist())

# Exercise 3: Handle missing values
print("Shape before dropping rows:", df.shape)

# Drop rows without an order ID or order date because both are essential.
df = df.dropna(subset=["order_id", "order_date"])

# Fill missing quantities with the mean to keep those orders.
df["quantity_sold"] = df["quantity_sold"].fillna(
    df["quantity_sold"].mean()
)

print("Shape after dropping rows:", df.shape)
print(df[["order_id", "order_date", "quantity_sold"]].isnull().sum())

# Exercise 4: Fix data types
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
print("Dates converted to NaT:", df["order_date"].isna().sum())

df["unit_price"] = (
    df["unit_price"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

df["quantity_sold"] = df["quantity_sold"].astype(int)

df["revenue"] = (df["unit_price"] * df["quantity_sold"]).round(2)

print(df.dtypes)

# Exercise 5: Check for duplicate rows
print("Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)

# Exercise 6: Describe the data
print(df.describe())
# The minimum revenue is -3268. This could represent a customer return,
# so we keep negative revenue values.
# The maximum revenue is 59994, which is unusually high and may be
# affected by placeholder quantities rather than real orders.

# Remove quantity 9999 because it is a placeholder, not a real order.
df = df[df["quantity_sold"] != 9999]

print("Shape after removing placeholder quantities:", df.shape)

# Exercise 7: Save and reload the cleaned data
df.to_csv("data/clean_sales.csv", index=False)

# Reload normally and check the types.
reloaded_df = pd.read_csv("data/clean_sales.csv")
print("Reloaded without parsing dates:")
reloaded_df.info()

# Reload again, this time interpreting order_date as a date.
reloaded_dates_df = pd.read_csv(
    "data/clean_sales.csv", parse_dates=["order_date"]
)
print("Reloaded with dates parsed:")
reloaded_dates_df.info()