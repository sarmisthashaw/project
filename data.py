import sqlite3
import pandas as pd

# read csv data
df = pd.read_csv("restaurant_data.csv", encoding='latin1')

# data cleanup
df.columns = df.columns.str.strip()

# create/connect to SQLite3 database
connection = sqlite3.connect('restaurant_database.db')

# Specify column names for the SQLite table


column_mapping = {
    'restaurant_name': 'The Nawaabs',
    'city': 'Agra',
    'latitude': 27.1619194000 ,
    'longitude': 78.0375562000,
    'ratings': 4.3
}

# Load datafile to SQLite3 with specified column names
df.rename(columns=column_mapping, inplace=True)
df.to_sql("restaurants_data", connection, if_exists='replace', index=False)

# close connection
connection.close()





# read csv data
# df = pd.read_csv("zomato.csv", encoding='latin1')
# df = pd.read_csv("order_data.csv", encoding='latin1')
df = pd.read_csv("restaurant.csv", encoding='latin1')


# data cleanup
df.columns = df.columns.str.strip()

# create/connect to SQLite3 database
connection = sqlite3.connect('restaurant_database.db')

# load datafile to SQLite3
# df.to_sql("restaurants_items", connection, if_exists='replace', index=False) 
df.to_sql("restaurants", connection, if_exists='replace', index=False) 

# close connection
connection.close()









