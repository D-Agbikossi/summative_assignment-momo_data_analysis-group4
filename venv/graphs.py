import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# Setup connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="momo_database",
    auth_plugin='mysql_native_password'
)

# Read data from database
query = "SELECT sms_data, amount, category FROM momo_transactions WHERE amount IS NOT NULL"
df = pd.read_sql_query(query, conn)

# Close connection
conn.close()

# Convert "sms_data" to datetime format
df['sms_data'] = pd.to_datetime(df['sms_data'])

# sort data by date
df = df.sort_values(by='sms_data')

# Aggregate data
summary_df = df.groupby("category")["amount"].sum().reset_index()

# Sort by total amount
summary_df = summary_df.sort_values(by="amount", ascending=False)

# Define category colors
category_colors = {
    "Incoming money": "green",
    "Payment to Code Holder": "red",
    "Transfer to Mobile Numbers": "blue",
    "Bank Deposits": "orange",
    "Airtime Bill Payments": "purple",
    "Cash Power Bill Payments": "brown",
    "Transaction Initiated by Third Parties": "pink",
    "Withdrawals from Agents": "black",
    "Bank Transfers": "yellow",
    "Internet and Voice Bundle Purchases": "cyan"
}

# Create a scatter plot
plt.figure(figsize=[12, 6])
for category, color in category_colors.items():
    subset = df[df['category'] == category]
    plt.scatter(subset.sms_data, subset.amount, label=category, color=color, alpha=0.7)

# Labels and titles
plt.xlabel("Date")
plt.ylabel("Transaction Amount (RWF)")
plt.title("Mobile Money Transactions Categorised over Time")

# Rotate axe
plt.xticks(rotation=45)

# Legend
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))

# Show graph
plt.show()

# Plotting a bar chart
plt.figure(figsize = (12, 6))
sns.barplot(x="amount", y="category", data=summary, palette=category_colors)

# Labels and title
plt.xlabel("Total Transaction Amount (RWF)")
plt.ylabel("Transaction Category")
plt.title("Total Mobile Money Transaction by Category")

# Show plot
plt.show()