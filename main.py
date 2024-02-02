# # main.py
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# import sqlite3

# # app = FastAPI()

# # def get_db():
# #     db = sqlite3.connect("restaurant_database.db")
# #     return db

# # @app.get("/top_restaurant/{city_name}")
# # def read_top_restaurants(city_name: str):
# #     db = get_db()
# #     cursor = db.cursor()

# #     # Fetch the top 5 restaurants in the specified city
# #     # cursor.execute(f"SELECT order_items FROM restaurants_orders WHERE city = '{city_name}' order by votes desc LIMIT 5")
# #     cursor.execute(f"SELECT * FROM restaurants where city = '{city_name}' order by ratings desc limit 1")

# #     top_restaurants = cursor.fetchall()

# #     db.close()

# #     if not top_restaurants:
# #         raise HTTPException(status_code=404, detail="not found")

# #     return JSONResponse(content={"top_restaurants": top_restaurants})

# # main.py
# app = FastAPI()

# def get_db():
#     db = sqlite3.connect("restaurant_database.db")
#     return db

# @app.get("/top_ordered_food/{city_name}")
# def read_top_restaurants_food_order(city_name: str):
#     db = get_db()
#     cursor = db.cursor()

#     # Fetch the top 5 restaurants in the specified city
#     # cursor.execute(f"SELECT order_items FROM restaurants_orders WHERE city = '{city_name}' order by votes desc LIMIT 5")
#     cursor.execute(f"SELECT order_items FROM restaurants_orders where city = '{city_name}' order by votes desc limit 5")

#     top_restaurants_food_order = cursor.fetchall()

#     db.close()

#     if not top_restaurants_food_order:
#         raise HTTPException(status_code=404, detail="not found")

#     return JSONResponse(content={"top_restaurants_food_order": top_restaurants_food_order})

import requests
from bs4 import BeautifulSoup
url = 'https://www.zomato.com/agra/the-nawaabs-tajganj/order'
data = requests.get(url)
# s = BeautifulSoup(data)
# s.find('div',{'class':'sc-bke1zw-1 bcVYKA'})
print(data)