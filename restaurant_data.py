import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import re

csv_filename = "restaurant_data_1.csv"
csv_lock = Lock()  # Lock to ensure thread-safe writing to the CSV file

def extract_city(address):
    # Use a regular expression to extract the city name
    match = re.search(r'(\w+)$', address)
    if match:
        return match.group(1)
    return None

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

def scrape_data(url):
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(5)

    # Find restaurant elements
    restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
    restaurant_name = [ele.text for ele in restaurant_elements]

    # Create an empty list to store the scraped data
    data = []

    # Iterate over all restaurants
    for restaurant_element in range(176):  
        try:
            # Re-find the restaurant elements before clicking
            restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
            restaurant_name = [ele.text for ele in restaurant_elements]
            
            # Click on the restaurant element to go to its page
            restaurant_elements[restaurant_element].click()
            time.sleep(5)

            # Re-find restaurant name after clicking
            restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

            # Find address elements
            address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
            addresses = [element.text for element in address_elements]

            # Extract city from the address
            city = extract_city(addresses[0]) if addresses else None
            
            # Find the element with the specified xpath
            element = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/section[3]/div[1]/section/a') 

            # Extract the href attribute value
            href_value = element.get_attribute('href')

            # Extract latitude and longitude
            latitude, longitude = extract_latitude_longitude(href_value)

            # Find rating elements
            rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
            ratings = [element.text for element in rating_elements]

            # Combine the scraped data into a dictionary
            data_dict = {
                'Restaurant_Name': restaurant_name[restaurant_element], 
                'City': city,
                'Latitude': latitude,
                'Longitude': longitude,
                'Rating': ratings[restaurant_element] if restaurant_element < len(ratings) else None,
            }

            # Append the dictionary to the data list
            data.append(data_dict)

            # Write the dictionary to the CSV file
            with csv_lock:
                write_to_csv(data_dict)

        except (NoSuchElementException, IndexError) as e:
            print(f"Error scraping data for restaurant {restaurant_element + 1}: {e}")

        finally:
            # Go back to the main page
            driver.back()
            time.sleep(5)

    # Close the browser
    driver.quit()

    return data

def write_to_csv(data_dict):
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Restaurant_Name', 'City', 'Latitude', 'Longitude', 'Rating'])
        writer.writerow(data_dict)

if __name__ == "__main__":
    urls = [
        r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Hyderabad - Zomato.html",

        r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
    ]

    # Create an empty list to store the scraped data
    scraped_data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(scrape_data, urls))
        for result in results:
            scraped_data.extend(result)

    print(f"Scraped data saved to {csv_filename}")































#####################################################################  CORRECT CODE    ##########################################################################################
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from concurrent.futures import ThreadPoolExecutor
# from threading import Lock

# csv_filename = "restaurant_data.csv"
# csv_lock = Lock()  # Lock to ensure thread-safe writing to the CSV file

# def scrape_data(url):
#     driver = webdriver.Edge()
#     driver.get(url)
#     time.sleep(5)

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]

#     # Create an empty list to store the scraped data
#     data = []

#     # Iterate over all restaurants
#     for restaurant_element in range(2):  
#         try:
#             # Re-find the restaurant elements before clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#             restaurant_name = [ele.text for ele in restaurant_elements]
            
#             # Click on the restaurant element to go to its page
#             restaurant_elements[restaurant_element].click()
#             time.sleep(5)

#             # Re-find restaurant name after clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#             # Find address elements
#             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#             addresses = [element.text for element in address_elements]

#             # Find rating elements
#             rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
#             ratings = [element.text for element in rating_elements]
            

#             # Combine the scraped data into a dictionary
#             data_dict = {
#                 'Restaurant_Name': restaurant_name[restaurant_element], 
#                 'Address': addresses[0] if addresses else None,  
#                 'Rating': ratings[restaurant_element] if restaurant_element < len(ratings) else None,
#             }

#             # Append the dictionary to the data list
#             data.append(data_dict)

#             # Write the dictionary to the CSV file
#             with csv_lock:
#                 write_to_csv(data_dict)

#         except (NoSuchElementException, IndexError) as e:
#             print(f"Error scraping data for restaurant {restaurant_element + 1}: {e}")

#         finally:
#             # Go back to the main page
#             driver.back()
#             time.sleep(5)

#     # Close the browser
#     driver.quit()

#     return data

# def write_to_csv(data_dict):
#     with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['Restaurant_Name', 'Address', 'Rating'])
#         writer.writerow(data_dict)

# if __name__ == "__main__":
#     urls = [
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
#     ]

#     # Create an empty list to store the scraped data
#     scraped_data = []

#     with ThreadPoolExecutor(max_workers=5) as executor:
#         results = list(executor.map(scrape_data, urls))
#         for result in results:
#             scraped_data.extend(result)

#     print(f"Scraped data saved to {csv_filename}")

########################################################### correct code but need to  do simultaneous insertion of  data ######################################################
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from concurrent.futures import ThreadPoolExecutor

# csv_filename = "restaurant_data.csv"

# def scrape_data(url):
#     driver = webdriver.Edge()
#     driver.get(url)
#     time.sleep(5)

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]

#     # Create an empty list to store the scraped data
#     data = []

#     # Iterate over all restaurants
#     for restaurant_element in range(2):  
#         try:
#             # Re-find the restaurant elements before clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#             restaurant_name = [ele.text for ele in restaurant_elements]
            
#             # Click on the restaurant element to go to its page
#             restaurant_elements[restaurant_element].click()
#             time.sleep(5)

#             # Re-find restaurant name after clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#             # Find address elements
#             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#             addresses = [element.text for element in address_elements]

#             # Find rating elements
#             rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
#             ratings = [element.text for element in rating_elements]
            

#             # Combine the scraped data into a dictionary
#             data_dict = {
#                 'Restaurant_Name': restaurant_name[restaurant_element], 
#                 'Address': addresses[0] if addresses else None,  
#                 'Rating': ratings[restaurant_element] if restaurant_element < len(ratings) else None,
#             }

#             # Append the dictionary to the data list
#             data.append(data_dict)

#         except (NoSuchElementException, IndexError) as e:
#             print(f"Error scraping data for restaurant {restaurant_element + 1}: {e}")

#         finally:
#             # Go back to the main page
#             driver.back()
#             time.sleep(5)

#     # Close the browser
#     driver.quit()

#     return data

# def write_to_csv(data):
#     with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['Restaurant_Name', 'Address', 'Rating'])
#         for data_dict in data:
#             writer.writerow(data_dict)

# if __name__ == "__main__":
#     urls = [
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html",
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html",
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
#     ]

#     # Create an empty list to store the scraped data
#     scraped_data = []

#     with ThreadPoolExecutor(max_workers=5) as executor:
#         results = list(executor.map(scrape_data, urls))
#         for result in results:
#             scraped_data.extend(result)

#     # Write all scraped data to the CSV file
#     write_to_csv(scraped_data)

#     print(f"Scraped data saved to {csv_filename}")
































































##Anvesh###################################
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from concurrent.futures import ThreadPoolExecutor

# csv_filename = "restaurant_data.csv"

# def scrape_data(url):
#     driver = webdriver.Edge()
#     driver.get(url)
#     time.sleep(5)

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]

#     # Create an empty list to store the scraped data
#     data = []

#     # Iterate over all restaurants
#     for restaurant_element in range(len(restaurant_name)):  
#         try:
#             # Re-find the restaurant elements before clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#             restaurant_name = [ele.text for ele in restaurant_elements]
            
#             # Click on the restaurant element to go to its page
#             restaurant_elements[restaurant_element].click()
#             time.sleep(5)

#             # Re-find restaurant name after clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#             # Find address elements
#             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#             addresses = [element.text for element in address_elements]

#             # Find rating elements
#             rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
#             ratings = [element.text for element in rating_elements]

#             # Combine the scraped data into a dictionary
#             data_dict = {
#                 'Restaurant_Name': restaurant_name[restaurant_element], 
#                 'Address': addresses[0] if addresses else None,  
#                 'Rating': ratings[restaurant_element] if restaurant_element < len(ratings) else None,
#             }

#             # Append the dictionary to the data list
#             data.append(data_dict)

#             # Append the data to the CSV file
#             with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
#                 writer = csv.DictWriter(file, fieldnames=['Restaurant_Name', 'Address', 'Rating'])
#                 writer.writerow(data_dict)

#         except (NoSuchElementException, IndexError) as e:
#             print(f"Error scraping data for restaurant {restaurant_element + 1}: {e}")

#         finally:
#             # Go back to the main page
#             driver.back()
#             time.sleep(5)

#     # Close the browser
#     driver.quit()

#     return data

# if __name__ == "__main__":
#     urls = [
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html",
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html",
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
#     ]

#     # Create an empty list to store the scraped data
#     scraped_data = []

#     with ThreadPoolExecutor(max_workers=5) as executor:
#         results = list(executor.map(scrape_data, urls))
#         for result in results:
#             scraped_data.extend(result)

#     print(f"Scraped data saved to {csv_filename}")
































































###### SEMI FINAL
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from concurrent.futures import ThreadPoolExecutor

# def scrape_data(url):
#     driver = webdriver.Edge()
#     driver.get(url)
#     time.sleep(5)

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]
 

#     # Create an empty list to store the scraped data
#     data = []

#     # Iterate over all restaurants
#     for restaurant_element in range(3):  # len(restaurant_name)
#         try:
#             # Re-find the restaurant elements before clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#             restaurant_name = [ele.text for ele in restaurant_elements]
#             # Click on the restaurant element to go to its page
#             restaurant_elements[restaurant_element].click()
#             time.sleep(5)

#             # Re-find restaurant name after clicking
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#             # Find address elements
#             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#             addresses = [element.text for element in address_elements]

#             # Find rating elements
#             rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
#             ratings = [element.text for element in rating_elements]

#             # Combine the scraped data into a dictionary
#             data_dict = {
#                 'Restaurant_Name': restaurant_name[restaurant_element], # if restaurant_element < len(restaurant_name) else None,
#                 'Address': addresses[0] if addresses else None,  
#                 'Rating': ratings[restaurant_element] if restaurant_element < len(ratings) else None,
#             }

#             # Append the dictionary to the data list
#             data.append(data_dict)

#         except (NoSuchElementException, IndexError) as e:
#             print(f"Error scraping data for restaurant {restaurant_element + 1}: {e}")

#         finally:
#             # Go back to the main page
#             driver.back()
#             time.sleep(5)

#     # Close the browser
#     driver.quit()

#     return data

# if __name__ == "__main__":
#     urls = [
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html",
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html",
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
#     ]

#     # Create an empty list to store the scraped data
#     scraped_data = []

#     with ThreadPoolExecutor(max_workers=5) as executor:
#         results = list(executor.map(scrape_data, urls))
#         for result in results:
#             scraped_data.extend(result)

#     # Convert the data to CSV
#     csv_filename = "restaurant_data.csv"
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['Restaurant_Name', 'Address', 'Rating'])
#         writer.writeheader()
#         writer.writerows(scraped_data)

#     print(f"Scraped data saved to {csv_filename}")











































# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Edge()
# urls = [
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html",
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html",
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Delhi NCR - Zomato.html",
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Hyderabad - Zomato.html",
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
# ]

# # Create an empty list to store the scraped data
# scraped_data = []

# for url in urls:
#     driver.get(url)
#     time.sleep(5)  # Adjust the waiting time if neededdriver.get(url)

# # Wait for the elements to load
# time.sleep(2)

# # Find restaurant elements
# restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 
# restaurant_name = [ele.text for ele in restaurant_elements]

# # Create an empty list to store the scraped data
# data = []

# # Iterate over all restaurants
# for restaurant_element in range(3):
#     # Re-find the restaurant elements before clicking
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')



#     price_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hez2tp-0 sc-ertOQY ZHcaD"]')
#     prices = [element.text.replace('₹', '') for element in price_elements]

#     food_item_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hez2tp-0 sc-ertOQY bNvMmg"]')
#     food_items = [element.text for element in food_item_elements]



#     # Click on the restaurant element to go to its page
#     restaurant_elements[restaurant_element].click()
#     time.sleep(5)

#     # Find address elements
#     address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#     addresses = [element.text for element in address_elements]
    
#     dineout_rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
#     dineout_ratings = [element.text for element in dineout_rating_elements]

#     dineout_rating_count_elements = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[1]/div[2]/div[1]')
#     dineout_rating_counts = [element.text for element in dineout_rating_count_elements]

#     delivery_rating_elements = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[3]/div[1]/div/div/div[1]')
#     delivery_ratings = [element.text for element in delivery_rating_elements]

#     delivery_rating_count_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-8 kEgyiI"]')
#     delivery_rating_counts = [element.text for element in delivery_rating_count_elements]


#     # Combine the scraped data into a dictionary
#     data_dict = {
#         'Restaurant_Name': restaurant_name[restaurant_element] if restaurant_element < len(restaurant_name) else None,
#         'Address': addresses[0] if addresses else None,  # Assuming only one address is expected
#         'Food_Item': food_items[restaurant_element],
#         'Price': prices[restaurant_element],
#         'Rating': dineout_ratings,
#         'Dineout_Rating_Count': dineout_rating_counts[restaurant_element] if restaurant_element < len(dineout_rating_counts) else None,
#         'Delivery_Rating': delivery_ratings[restaurant_element] if restaurant_element < len(delivery_ratings) else None,
#         'Rating_Count': delivery_rating_counts


#     }

#     # Append the dictionary to the data list
#     data.append(data_dict)

#     # Go back to the main page
#     driver.back()
#     time.sleep(5)

# # Close the browser
# driver.quit()

# # Convert the data to CSV
# csv_filename = "restaurant_data.csv"
# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=['Restaurant_Name', 'Address','Food_Item','Price','Rating','Dineout_Rating_Count','Delivery_Rating','Rating_Count'])
#     writer.writeheader()
#     writer.writerows(data)

# print(f"Scraped data saved to {csv_filename}")











#################################################################################      Rough         #########################################################################################################3



# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Edge()
# url = r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Checkout Best Food Places To Eat In Agra _ Zomato.html"
# driver.get(url)

# # Wait for the elements to load
# time.sleep(2)

#     # Find restaurant elements
# restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-lffWgi flnmvC"]')
# restaurant_name = [ele.text for ele in restaurant_elements]

# addresses = []
#     # Iterate over all restaurants
# for restaurant_element in range(3):
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-lffWgi flnmvC"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]
#         # Get the restaurant name
#     current_restaurant_name = restaurant_name[restaurant_element]


#     # price_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hez2tp-0 sc-fGSyRc dMkcNo"]')
#     # prices = [element.text.replace('₹', '') for element in price_elements]

#     # food_item_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hez2tp-0 sc-fGSyRc eWQqcH"]')
#     # food_items = [element.text for element in food_item_elements]

#     # time_taken_elements = driver.find_elements(by=By.CLASS_NAME, value='min-basic-info-right')
#     # avg_time_taken = [element.text for element in time_taken_elements]


#         # Click on the restaurant element to go to its page
#     restaurant_elements[restaurant_element].click()
#     time.sleep(5)

#     # address_element = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#     # address = [element.text for element in address_element]
#     # addresses.extend(address)
#     # print(address)


#     dineout_rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
#     dineout_ratings = [element.text for element in dineout_rating_elements]

#     # dineout_rating_count_elements = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[1]/div[2]/div[1]')
#     # dineout_rating_counts = [element.text for element in dineout_rating_count_elements]

#     # delivery_rating_elements = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[3]/div[1]/div/div/div[1]')
#     # delivery_ratings = [element.text for element in delivery_rating_elements]


#     delivery_rating_count_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-8 kEgyiI"]')
#     delivery_rating_counts = [element.text for element in delivery_rating_count_elements]

#     data = []

#       # Combine the scraped data into a dictionary
#     data.append({
#         'Restaurant Name': restaurant_name[restaurant_element],
#         'Dineout_Rating': dineout_ratings[restaurant_element] if restaurant_element < len(dineout_ratings) else None,
#         # 'Dineout_Rating_Count': dineout_rating_counts[i] if i < len(dineout_rating_counts) else None,
#         # 'Delivery_Rating': delivery_ratings[i] if i < len(delivery_ratings) else None,
#         'Delivery_Rating_Count': delivery_rating_counts[restaurant_element] if restaurant_element < len(delivery_rating_counts) else None
#     })




#     driver.back()
#     time.sleep(5)

# # Close the browser
# driver.quit()

# # # Combine the scraped data into a list of dictionaries
# # data = []
# # for i in range(len(current_restaurant_name)):
# #     data.append({
# #         'Restaurant Name': restaurant_name[i],
# #         # 'Food Item': food_items[i],
# #         # 'Price': prices[i],
# #         # 'Avg Time Taken': avg_time_taken[i],
# #         'Address': addresses[i],
# #         # 'Dineout_Rating': dineout_ratings[i] if i < len(dineout_ratings) else None,
# #         # 'Dineout_Rating_Count': dineout_rating_counts[i] if i < len(dineout_rating_counts) else None,
# #         # 'Delivery_Rating': delivery_ratings[i] if i < len(delivery_ratings) else None,
# #         # 'Delivery_Rating_Count': delivery_rating_counts[i] if i < len(delivery_rating_counts) else None
# #     })

# # print(data)

# # Convert the data to CSV
# csv_filename = "restaurant_data_1.csv"
# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=['Restaurant Name','Dineout_Rating','Delivery_Rating_Count'])
#     writer.writeheader()
#     writer.writerows(data)

# print(f"Scraped data saved to {csv_filename}")





#RATINGS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Edge()
# url = r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Checkout Best Food Places To Eat In Agra _ Zomato.html"
# driver.get(url)

# # Wait for the elements to load
# time.sleep(2)

# # Find restaurant elements
# restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-lffWgi flnmvC"]')

# # Create an empty list to store the scraped data
# data = []

# # Iterate over all restaurants
# for restaurant_element in range(4):
#     # Find restaurant elements again to avoid StaleElementReferenceException
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-lffWgi flnmvC"]')
#     restaurant_elements[restaurant_element].click()
#     time.sleep(5)

#     # Extract data for each restaurant
#     current_restaurant_name = restaurant_elements[restaurant_element].

#     # price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hez2tp-0 sc-fGSyRc dMkcNo"]')
#     # prices = [element.text.replace('₹', '') for element in price_elements]

#     # food_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hez2tp-0 sc-fGSyRc eWQqcH"]')
#     # food_items = [element.text for element in food_item_elements]

#     # time_taken_elements = driver.find_elements(By.CLASS_NAME, 'min-basic-info-right')
#     # avg_time_taken = [element.text for element in time_taken_elements]

#     # address_element = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#     # addresses = [element.text for element in address_element]

#     dineout_rating_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-1 cILgox"]')
#     dineout_ratings = [element.text for element in dineout_rating_elements]

#     # dineout_rating_count_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[1]/div[2]/div[1]')
#     # dineout_rating_counts = [element.text for element in dineout_rating_count_elements]

#     # delivery_rating_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[3]/div[1]/div/div/div[1]')
#     # delivery_ratings = [element.text for element in delivery_rating_elements]

#     delivery_rating_count_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1q7bklc-8 kEgyiI"]')
#     delivery_rating_counts = [element.text for element in delivery_rating_count_elements]

#     # Append data to the list
#     data.append({
#         'Restaurant Name': current_restaurant_name,
#         # 'Food Item': food_items,
#         # 'Price': prices,
#         # 'Avg Time Taken': avg_time_taken,
#         # 'Address': addresses,
#         'Dineout_Rating': dineout_ratings,
#         # 'Dineout_Rating_Count': dineout_rating_counts,
#         # 'Delivery_Rating': delivery_ratings,
#         'Delivery_Rating_Count': delivery_rating_counts
#     })

#     # Go back to the main page
#     driver.back()
#     time.sleep(5)

# # Close the browser
# driver.quit()

# # Convert the data to CSV
# csv_filename = "restaurant_data.csv"
# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=['Restaurant Name', 'Dineout_Rating','Delivery_Rating_Count'])
#     writer.writeheader()
#     writer.writerows(data)

# print(f"Scraped data saved to {csv_filename}")


































































# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Edge()
# url = r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Checkout Best Food Places To Eat In Agra _ Zomato.html"
# driver.get(url)

# # Wait for the elements to load
# time.sleep(2)

# # Scraping logic for restaurant names and addresses using XPath
# name_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hp8d8a-0 sc-lffWgi flnmvC"]')
# item = [element.text for element in name_elements]

# price_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hez2tp-0 sc-fGSyRc dMkcNo"]')
# prices = [element.text.replace('₹', '') for element in price_elements]

# food_item_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hez2tp-0 sc-fGSyRc eWQqcH"]')
# food_items = [element.text for element in food_item_elements]

# time_taken_elements = driver.find_elements(by=By.CLASS_NAME, value='min-basic-info-right')
# avg_time_taken = [element.text for element in time_taken_elements]

# # Limit the range to 10 restaurants
# num_restaurants = min(10, len(item))

# # Combine the scraped data into a list of dictionaries for only 10 restaurants
# data = []
# for i in range(num_restaurants):
#     data.append({
#         'Restaurant Name': item[i],
#         'Food Item': food_items[i],
#         'Price': prices[i],
#         'Avg Time Taken': avg_time_taken[i]
#     })

# # Convert the data to CSV
# csv_filename = "restaurant_data.csv"
# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=['Restaurant Name', 'Food Item','Price','Avg Time Taken'])
#     writer.writeheader()
#     writer.writerows(data)

# print(f"Scraped data saved to {csv_filename}")

# # Close the browser
# driver.quit()























