

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re

# Create an empty DataFrame to store restaurant details
restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Rating', 'Cuisine', 'Average Cost for Two', 'City', 'Address', 'Latitude', 'Longitude'])

def extract_latitude_longitude(href_value):
    # Split the href_value based on "1&destination="
    split_values = href_value.split("1&destination=")

    # Check if the split operation resulted in two parts
    if len(split_values) == 2:
        # Further split the second part based on ","
        coordinates = split_values[1].split(",")

        # Check if the second split resulted in two parts
        if len(coordinates) == 2:
            latitude, longitude = coordinates
            return latitude, longitude

def extract_city(address):
    # Use a regular expression to extract the city name
    match = re.search(r'(\w+)$', address)
    if match:
        return match.group(1)
    return None

driver = webdriver.Edge()

url = "https://www.zomato.com/india"
driver.get(url)

# Wait for the page to load (you can adjust the sleep time based on your needs)
time.sleep(5)

# Find all the restaurant links using the appropriate XPath
cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

# Create a list to store the href values
hrefs = []

# Iterate through the found links and extract href attributes
for city, city_1 in zip(cities, cities_1):
    link_0 = city.get_attribute('href')
    link_1 = city_1.get_attribute('href')
    hrefs.extend([link_0, link_1])

# Open each link in the browser
for link in hrefs:
    driver.get(link)
    print(link)
    
    try:
        # Check if "Dining Out" element is present
        dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')
        
        # If present, click it and do something on the page, e.g., scrape data
        dining_out_element.click()
        time.sleep(5)

        for i in range(10, 13):
            for j in range(1, 4):
                # Scrape restaurant details
                rest_name_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/h4') 
                rest_name = rest_name_element.text

                rating_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/div/div/div/div/div/div[1]')
                rating = rating_element.text    

                cuisine_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[1]')
                cuisine = cuisine_element.text

                cost_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[2]')
                cost = cost_element.text

                location_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[3]/div[1]/p')
                location = location_element.text

                city = extract_city(location) 

                restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
                rest_href = restaurant_in.get_attribute('href')
                driver.get(rest_href)

                # Find address elements
                latitude_longitude_element = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/section[3]/div[1]/section/a')
                href_value = latitude_longitude_element.get_attribute('href')

                latitude, longitude = extract_latitude_longitude(href_value)
                driver.back()
                time.sleep(5)


                # Append the details to the DataFrame after each iteration
                restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
                    'Restaurant Name': [rest_name],
                    'Rating': [rating],
                    'Cuisine': [cuisine],
                    'Average Cost for Two': [cost],
                    'City': [city],
                    'Address': [location],
                    'Latitude': [latitude],
                    'Longitude': [longitude],
                })], ignore_index=True)

                # Save the DataFrame to a CSV file inside the nested loop
                restaurant_df.to_csv('restaurant_details.csv', index=False)

                print('Restaurant_details:', rest_name)
                print('Rating:', rating)
                print('Cuisine:', cuisine)
                print('Average Cost for Two:', cost)
                print('Location:', location)
                print('City:', city)
                print('Latitude:', latitude)
                print('Longitude:', longitude)
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------')

    except NoSuchElementException:
        print('Dining Out element not found on this page. Skipping...')

# Save the DataFrame to a CSV file after the outer loop
restaurant_df.to_csv('restaurant_details.csv', index=False)

# Display the final DataFrame with restaurant details
print(restaurant_df)

# Close the browser
driver.quit()



# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import re
# from tqdm import tqdm
# from multiprocessing import Pool

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Rating', 'Cuisine', 'Average Cost for Two', 'City', 'Address', 'Latitude', 'Longitude'])

# def extract_latitude_longitude(href_value):
#     # Split the href_value based on "1&destination="
#     split_values = href_value.split("1&destination=")

#     # Check if the split operation resulted in two parts
#     if len(split_values) == 2:
#         # Further split the second part based on ","
#         coordinates = split_values[1].split(",")

#         # Check if the second split resulted in two parts
#         if len(coordinates) == 2:
#             latitude, longitude = coordinates
#             return latitude, longitude

# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None

# def scrape_restaurant(link):
#     try:
#         driver = webdriver.Edge()
#         driver.get(link)

#         # Check if "Dining Out" element is present
#         dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')

#         # If present, click it and do something on the page, e.g., scrape data
#         dining_out_element.click()
#         time.sleep(5)

#         for i in range(10, 13):
#             for j in range(1, 4):
#                 # Scrape restaurant details
#                 rest_name_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/h4') 
#                 rest_name = rest_name_element.text

#                 rating_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/div/div/div/div/div/div[1]')
#                 rating = rating_element.text    

#                 cuisine_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[1]')
#                 cuisine = cuisine_element.text

#                 cost_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[2]')
#                 cost = cost_element.text

#                 location_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[3]/div[1]/p')
#                 location = location_element.text

#                 city = extract_city(location) 

#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)

#                 # Find address elements
#                 latitude_longitude_element = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/section[3]/div[1]/section/a')
#                 href_value = latitude_longitude_element.get_attribute('href')

#                 latitude, longitude = extract_latitude_longitude(href_value)
#                 driver.back()
#                 time.sleep(5)

#                 # Append the details to the DataFrame after each iteration
#                 restaurant_df.loc[len(restaurant_df)] = [rest_name, rating, cuisine, cost, city, location, latitude, longitude]

#     except NoSuchElementException:
#         print(f'Dining Out element not found on {link}. Skipping...')

#     finally:
#         driver.quit()

# def main():
#     driver = webdriver.Edge()

#     url = "https://www.zomato.com/india"
#     driver.get(url)

#     # Wait for the page to load (you can adjust the sleep time based on your needs)
#     time.sleep(5)

#     # Find all the restaurant links using the appropriate XPath
#     cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
#     cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

#     # Create a list to store the href values
#     hrefs = []

#     # Iterate through the found links and extract href attributes
#     for city, city_1 in zip(cities, cities_1):
#         link_0 = city.get_attribute('href')
#         link_1 = city_1.get_attribute('href')
#         hrefs.extend([link_0, link_1])

#     # Close the initial browser
#     driver.quit()

#     # Use multiprocessing to parallelize scraping
#     with Pool() as pool:
#         # Use tqdm for progress bars
#         for _ in tqdm(pool.imap_unordered(scrape_restaurant, hrefs), total=len(hrefs)):
#             pass

#     # Save the DataFrame to a CSV file after the outer loop
#     restaurant_df.to_csv('restaurant_details.csv', index=False)

#     # Display the final DataFrame with restaurant details
#     print(restaurant_df)

# if __name__ == "__main__":
#     main()




# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import re
# from tqdm import tqdm
# from multiprocessing import Pool
# from multiprocessing import Lock

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Rating', 'Cuisine', 'Average Cost for Two', 'City', 'Address', 'Latitude', 'Longitude'])

# # Create a lock to ensure thread-safe file writing
# csv_lock = Lock()

# def extract_latitude_longitude(href_value):
#     # Split the href_value based on "1&destination="
#     split_values = href_value.split("1&destination=")

#     # Check if the split operation resulted in two parts
#     if len(split_values) == 2:
#         # Further split the second part based on ","
#         coordinates = split_values[1].split(",")

#         # Check if the second split resulted in two parts
#         if len(coordinates) == 2:
#             latitude, longitude = coordinates
#             return latitude, longitude

# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None

# def scrape_restaurant(link):
#     try:
#         driver = webdriver.Edge()
#         driver.get(link)

#         # Check if "Dining Out" element is present
#         dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')

#         # If present, click it and do something on the page, e.g., scrape data
#         dining_out_element.click()
#         time.sleep(5)

#         for i in range(10, 13):
#             for j in range(1, 4):
#                 # Scrape restaurant details
#                 rest_name_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/h4') 
#                 rest_name = rest_name_element.text

#                 rating_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/div/div/div/div/div/div[1]')
#                 rating = rating_element.text    

#                 cuisine_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[1]')
#                 cuisine = cuisine_element.text

#                 cost_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[2]')
#                 cost = cost_element.text

#                 location_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[3]/div[1]/p')
#                 location = location_element.text

#                 city = extract_city(location) 

#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)

#                 # Find address elements
#                 latitude_longitude_element = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/section[3]/div[1]/section/a')
#                 href_value = latitude_longitude_element.get_attribute('href')

#                 latitude, longitude = extract_latitude_longitude(href_value)
#                 driver.back()
#                 time.sleep(5)

#                 # Append the details to the DataFrame after each iteration
#                 with csv_lock:
#                     restaurant_df.loc[len(restaurant_df)] = [rest_name, rating, cuisine, cost, city, location, latitude, longitude]
#                     # Save the DataFrame to a CSV file inside the loop
#                     restaurant_df.to_csv('restaurant_details.csv', index=False)

#     except NoSuchElementException:
#         print(f'Dining Out element not found on {link}. Skipping...')

#     finally:
#         driver.quit()

# def main():
#     driver = webdriver.Edge()

#     url = "https://www.zomato.com/india"
#     driver.get(url)

#     # Wait for the page to load (you can adjust the sleep time based on your needs)
#     time.sleep(5)

#     # Find all the restaurant links using the appropriate XPath
#     cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
#     cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

#     # Create a list to store the href values
#     hrefs = []

#     # Iterate through the found links and extract href attributes
#     for city, city_1 in zip(cities, cities_1):
#         link_0 = city.get_attribute('href')
#         link_1 = city_1.get_attribute('href')
#         hrefs.extend([link_0, link_1])

#     # Close the initial browser
#     driver.quit()

#     # Use multiprocessing to parallelize scraping
#     with Pool() as pool:
#         # Use tqdm for progress bars
#         for _ in tqdm(pool.imap_unordered(scrape_restaurant, hrefs), total=len(hrefs)):
#             pass

# if __name__ == "__main__":
#     main()
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re

# Create an empty DataFrame to store restaurant details
restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Rating', 'Cuisine', 'Average Cost for Two', 'City', 'Address', 'Latitude', 'Longitude'])

def extract_latitude_longitude(href_value):
    # Split the href_value based on "1&destination="
    split_values = href_value.split("1&destination=")

    # Check if the split operation resulted in two parts
    if len(split_values) == 2:
        # Further split the second part based on ","
        coordinates = split_values[1].split(",")

        # Check if the second split resulted in two parts
        if len(coordinates) == 2:
            latitude, longitude = coordinates
            return latitude, longitude

def extract_city(address):
    # Use a regular expression to extract the city name
    match = re.search(r'(\w+)$', address)
    if match:
        return match.group(1)
    return None

driver = webdriver.Edge()

url = "https://www.zomato.com/india"
driver.get(url)

# Wait for the page to load (you can adjust the sleep time based on your needs)
time.sleep(5)

# Find all the restaurant links using the appropriate XPath
cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

# Create a list to store the href values
hrefs = []

# Iterate through the found links and extract href attributes
for city, city_1 in zip(cities, cities_1):
    link_0 = city.get_attribute('href')
    link_1 = city_1.get_attribute('href')
    hrefs.extend([link_0, link_1])

# Open each link in the browser
for link in hrefs:
    driver.get(link)
    print(link)
    
    try:
        # Check if "Dining Out" element is present
        dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')
        
        # If present, click it and do something on the page, e.g., scrape data
        dining_out_element.click()
        time.sleep(5)

        for i in range(10, 111):
            for j in range(1, 4):                                    
                # Scrape restaurant details
                rest_name_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/h4') 
                rest_name = rest_name_element.text

                rating_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[1]/div/div/div/div/div/div[1]')
                rating = rating_element.text    

                cuisine_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[1]')
                cuisine = cuisine_element.text

                cost_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[2]/p[2]')
                cost = cost_element.text

                location_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[3]/div[1]/p')
                location = location_element.text

                city = extract_city(location) 

                restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
                rest_href = restaurant_in.get_attribute('href')
                driver.get(rest_href)

                # Find address elements
                latitude_longitude_element = driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/section[3]/div[1]/section/a')
                href_value = latitude_longitude_element.get_attribute('href')

                latitude, longitude = extract_latitude_longitude(href_value)
                driver.back()
                time.sleep(5)


                # Append the details to the DataFrame after each iteration
                restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
                    'Restaurant Name': [rest_name],
                    'Rating': [rating],
                    'Cuisine': [cuisine],
                    'Average Cost for Two': [cost],
                    'City': [city],
                    'Address': [location],
                    'Latitude': [latitude],
                    'Longitude': [longitude],
                })], ignore_index=True)

                # Save the DataFrame to a CSV file inside the nested loop
                restaurant_df.to_csv('restaurant_details.csv', index=False)

                print('Restaurant_details:', rest_name)
                print('Rating:', rating)
                print('Cuisine:', cuisine)
                print('Average Cost for Two:', cost)
                print('Location:', location)
                print('City:', city)
                print('Latitude:', latitude)
                print('Longitude:', longitude)
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------')

    except NoSuchElementException:
        print('Dining Out element not found on this page. Skipping...')

# Save the DataFrame to a CSV file after the outer loop
restaurant_df.to_csv('restaurant_details.csv', index=False)

# Display the final DataFrame with restaurant details
print(restaurant_df)

# Close the browser
driver.quit()