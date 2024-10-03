import pandas as pd
import sqlite3
from datetime import datetime
import glob
import os

# Extract
csv_files = glob.glob(os.path.join("./", "*.csv"))

if not csv_files:
    raise FileNotFoundError("Aucun fichier CSV trouvé dans le répertoire spécifié.")

latest_csv_file = max(csv_files, key=os.path.getmtime)
print(f"Le dernier fichier CSV créé est: {latest_csv_file}")

date_str = latest_csv_file.replace("retail_", "").replace(".csv", "")
csv_file = 'retail_15_01_2022.csv'
df = pd.read_csv(csv_file)
print("Extraction completed!")

# Transform
df.rename(columns={'description': 'name'}, inplace=True)
df["transaction_date"] = datetime.strptime(csv_file.replace("retail_", "").replace(".csv", ""), "%d_%m_%Y")
print("Transformation completed!")

# Load
conn = sqlite3.connect('retail.db')

existing_ids_query = "SELECT id FROM transactions"
existing_ids = pd.read_sql(existing_ids_query, conn)['id'].tolist()

df_new = df[~df['id'].isin(existing_ids)]
if not df_new.empty:
    df_new.to_sql('transactions', conn, if_exists='append', index=False)
    print(f"Inserted {len(df_new)} new records.")
else:
    print("No new records to insert.")

conn.commit()
conn.close()

print("Data loaded successfully!")