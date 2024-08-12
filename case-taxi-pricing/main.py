from sqlalchemy import create_engine
from faker import Faker
import random
import pandas as pd
import geopy
import time
from pprint import pprint
import sqlite3

fake = Faker("pt_BR")
db_name = "corridas.db"
engine = create_engine("sqlite:///" + db_name)
num_records = 500
preco_km = 2

data = {
    "corrida_inicio": [
        fake.date_time_between(start_date="-5w", end_date="now")
        for _ in range(num_records)
    ],
    "destino": [fake.street_address() for _ in range(num_records)],
    "trafego": [random.randint(1, 5) for _ in range(num_records)],
    "km": [random.randint(1, 12) for _ in range(num_records)],
}

data["preco"] = [
    preco_km * km * (trafego / 2) for km, trafego in zip(data["km"], data["trafego"])
]

df = pd.DataFrame(data)
df.describe()

df.to_sql("corridas", engine, index=False, if_exists="replace")

db_connect = sqlite3.connect(db_name)

db = db_connect.cursor()
db.execute("SELECT * FROM corridas LIMIT 20")

for row in db.fetchall():
    print(row)

db_connect.close()
