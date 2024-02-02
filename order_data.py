import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import re

def extract_city(address):
    # Use a regular expression to extract the city name
    match = re.search(r'(\w+)$', address)
    if match:
        return match.group(1)
    return None

def scrape_data(url, combined_df):
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(5)

    # Find restaurant elements
    restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
    restaurant_name = [ele.text for ele in restaurant_elements]

    # Create an empty list to store the scraped data
    data = []

    # Iterate over all restaurants
    for restaurant_element in range(len(restaurant_elements)):
        # Get the restaurant name
        current_restaurant_name = restaurant_name[restaurant_element]

        # Click on the restaurant element to go to its page
        restaurant_elements[restaurant_element].click()
        time.sleep(5)

        # Extract address
        address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
        addresses = [element.text for element in address_elements]

        # Create an empty list to store the data for the current restaurant
        restaurant_data = []

        # Iterate over each address and add to the scraped data
        for address in addresses:
            try:
                # Click on the "Order Online" link
                order_online_link = driver.find_element(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a')
                order_online_link.click()
                time.sleep(5)

                # Now, you can perform scraping logic for order items on the "Order Online" section
                order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
                order_items = [element.text for element in order_item_elements]

                price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
                prices = [element.text.replace('₹', '').split('\n')[0] for element in price_elements]

                votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
                no_of_votes = [int(element.text.split()[0]) for element in votes_elements]

                # Re-find restaurant name after clicking
                restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

                # Find address elements
                address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
                addresses = [element.text for element in address_elements]

                # Extract city from the address
                city = extract_city(addresses[0]) if addresses else None
                for f in range(1,100):
                

                    rating_1 = 0
                    star_elements = driver.find_elements(By.XPATH,
                                                                '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')

                    try:
                        for star in range(len(star_elements)):
                            html_string = star_elements[star].get_attribute('innerHTML')
                            soup = BeautifulSoup(html_string, 'lxml')
                            fill_value = soup.svg['fill']
                            title_text = soup.title.text
                            if fill_value == '#F3C117' and title_text == 'star-fill':
                                rating_1 += 1
                            else:
                                rating_1 += 0
                    except Exception as e:
                        print(f"Error: {e}")

                        soup = BeautifulSoup(html_string, 'html.parser')
                        linear_gradient = soup.find('linearGradient')
                        linear_gradient = soup.svg.lineargradient
                        stops = linear_gradient.find_all('stop')
                        percentage = stops[1]['offset']
                        decimal_rating = int(percentage.strip('%')) / 100

                        rating_1 = decimal_rating

                        rating = 0
                        star_elements = driver.find_elements(By.XPATH,'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')
                    try:
                                for star in range(len(star_elements)):
                                    html_string = star_elements[star].get_attribute('innerHTML')
                                    soup = BeautifulSoup(html_string, 'lxml')
                                    fill_value = soup.svg['fill']
                                    title_text = soup.title.text
                                    if fill_value == '#F3C117' and title_text == 'star-fill':
                                        rating += 1
                    except Exception as e:
                                # Handle specific exceptions or log the error
                                print(f"Error: {e}")

                                soup = BeautifulSoup(html_string, 'html.parser')
                                linear_gradient = soup.find('linearGradient')
                                # linear_gradient= soup.svg.lineargradient
                                if linear_gradient:
                                    linear_gradient_id = linear_gradient['id']
                                    linear_gradient_x1 = linear_gradient['x1']
                                    linear_gradient_x2 = linear_gradient['x2']

                                    stops = linear_gradient.find_all('stop')
                                    percentage = stops[1]['offset']
                                    decimal_rating = int(percentage.strip('%')) / 100

                                    rating = decimal_rating
                    ratings = rating + rating_1     
                                                                                    



                # Add the scraped data to the list for the current restaurant
                restaurant_data.extend([{
                    'Restaurant_Name': current_restaurant_name,
                    "city": city,
                    'Order_Items': order_item,
                    'Prices': float(price) if price else None,
                    'Rating': ratings,
                    'Votes': votes
                } for order_item, price,votes in zip(order_items, prices,no_of_votes)])

            except NoSuchElementException as e:
                print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

            # After scraping or if "Order Online" link not found, go back to the main page
            finally:
                driver.back()
                time.sleep(2)
                driver.back()

                # Re-find restaurant elements after navigating back
                restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

                # Wait for the main page to load again
                time.sleep(7)

        # Convert the list of dictionaries to a DataFrame for the current restaurant
        df_restaurant = pd.DataFrame(restaurant_data)

        # Append the DataFrame for the current restaurant to the overall data list
        data.append(df_restaurant)

        # Combine the DataFrames for all restaurants into a single DataFrame
        combined_df = pd.concat(data, ignore_index=True)

        # Display the combined DataFrame
        # print(combined_df)

        # Save the combined DataFrame to a CSV file
        combined_df.to_csv("combined_order_data.csv", index=False)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    urls = [
        r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
        # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html"
        # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
    ]

    combined_df = pd.DataFrame()

    for url in urls:
        scrape_data(url, combined_df)




#################################################################### Store data in sep csv#####################################################
# # ############### correct code      #################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from concurrent.futures import ThreadPoolExecutor
# from tqdm import tqdm
# import re

# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None

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
#     for restaurant_element in range(len(restaurant_elements)):
#         # Get the restaurant name
#         current_restaurant_name = restaurant_name[restaurant_element]

#         # Click on the restaurant element to go to its page
#         restaurant_elements[restaurant_element].click()
#         time.sleep(5)

#         # Extract address
#         address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#         addresses = [element.text for element in address_elements]

#         # Create an empty list to store the data for the current restaurant
#         restaurant_data = []

#         # Iterate over each address and add to the scraped data
#         for address in addresses:
#             try:
#                 # Click on the "Order Online" link
#                 order_online_link = driver.find_element(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a')
#                 order_online_link.click()
#                 time.sleep(5)

#                 # Now, you can perform scraping logic for order items on the "Order Online" section
#                 order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#                 order_items = [element.text for element in order_item_elements]

#                 price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#                 prices = [element.text.replace('₹', '').split('\n')[0] for element in price_elements]

#                 votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#                 no_of_votes = [int(element.text.split()[0]) for element in votes_elements]

#                 # Re-find restaurant name after clicking
#                 restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#                 # Find address elements
#                 address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#                 addresses = [element.text for element in address_elements]

#                 # Extract city from the address
#                 city = extract_city(addresses[0]) if addresses else None

#                 # Add the scraped data to the list for the current restaurant
#                 restaurant_data.extend([{
#                     'Restaurant_Name': current_restaurant_name,
#                     "city": city,
#                     'Order_Items': order_item,
#                     'Prices': float(price) if price else None,
#                     'Votes': votes
#                 } for order_item, price, votes in zip(order_items, prices, no_of_votes)])

#             except NoSuchElementException as e:
#                 print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

#             # After scraping or if "Order Online" link not found, go back to the main page
#             finally:
#                 driver.back()
#                 time.sleep(2)
#                 driver.back()

#                 # Re-find restaurant elements after navigating back
#                 restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#                 # Wait for the main page to load again
#                 time.sleep(7)

#         # Convert the list of dictionaries to a DataFrame for the current restaurant
#         df_restaurant = pd.DataFrame(restaurant_data)

#         # Save the DataFrame to a CSV file for the current restaurant
#         csv_filename = f"{current_restaurant_name}_order_data.csv"
#         df_restaurant.to_csv(csv_filename, index=False)
#         print(f"Scraped data for {current_restaurant_name} saved to {csv_filename}")

#     # Close the browser
#     driver.quit()

# if __name__ == "__main__":
#     urls = [
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
#         # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html"
#         # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
#     ]

#     for url in urls:
#         scrape_data(url)


###################################################################################3            ROUGH                  #############################################################################################


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import csv

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
#     time.sleep(5)  # Adjust the waiting time if needed

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]

#     # Iterate over all restaurants
#     for restaurant_element in range(2):
#         # Get the restaurant name
#         current_restaurant_name = restaurant_name[restaurant_element]

#         # Click on the restaurant element to go to its page
#         restaurant_elements[restaurant_element].click()
#         time.sleep(5)

#         # Extract address
#         address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#         addresses = [element.text for element in address_elements]

#         # Iterate over each address and add to the scraped data
#         for address in addresses:
#             try:
#                 # Click on the "Order Online" link
#                 order_online_link = driver.find_element(By.XPATH, '//*[@class="sc-jhaWeW hAbUan"]')
#                 order_online_link.click()
#                 time.sleep(5)

#                 # Now, you can perform scraping logic for order items on the "Order Online" section
#                 order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#                 order_items = [element.text for element in order_item_elements]

#                 price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#                 prices = [element.text.replace('₹', '') for element in price_elements]

#                 votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#                 no_of_votes = [element.text for element in votes_elements]

#                 # Add the scraped data to the list
#                 scraped_data.append({
#                     'Restaurant_Name': current_restaurant_name,
#                     'Address': address,
#                     'Order_Items': order_items, 
#                     'Prices': prices,                
#                     'Votes': no_of_votes
#                 })

#             except NoSuchElementException as e:
#                 print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

#             # After scraping or if "Order Online" link not found, go back to the main page
#             finally:
#                 driver.back()
#                 time.sleep(2)
#                 driver.back()

#                 # Re-find restaurant elements after navigating back
#                 restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#                 # Wait for the main page to load again
#                 time.sleep(7)

# # Close the browser
# driver.quit()

# # Convert the scraped data to CSV
# csv_filename = "order_data.csv"

# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Restaurant_Name', 'Address','Order_Items','Prices','Votes']  # Add more field names as needed
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(scraped_data)

# print(f"Scraped data saved to {csv_filename}")










##########################################################################          ROUGH         ######################################################################


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import csv

# driver = webdriver.Edge()

# urls = [
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
# ]

# # Create an empty list to store the scraped data
# scraped_data = []

# for url in urls:
#     driver.get(url)
#     time.sleep(5)  # Adjust the waiting time if needed

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#     # Iterate through each restaurant
#     for restaurant_element in range(6):
#         # Click on the restaurant element to go to its page
#         restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#         restaurant_names = [element.text for element in restaurant_elements]
#         restaurant_elements[restaurant_element].click()

#         # Wait for the page to load (you may need to adjust the waiting time)
#         time.sleep(5)

#         # Now, you can perform additional scraping logic for each individual restaurant page
#         # For example, you can extract the address, menu items, prices, etc.

#         # Extract address
#         address_element = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#         address = [element.text for element in address_element]

#         # Extract order items
#         # Click on the "Order Online" link
#         order_online_link = driver.find_element(By.XPATH, '//*[@class="sc-jhaWeW hAbUan"]')
#         order_online_link.click()
#         time.sleep(5)

#             # Now, you can perform scraping logic for order items on the "Order Online" section
#         order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#         order_items = [element.text for element in order_item_elements]

#         # Extract prices
#         price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#         prices = [element.text.replace('₹', '') for element in price_elements]

#         # Extract votes
#         votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#         no_of_votes = [element.text for element in votes_elements]

#         # Add the scraped data to the list
#         scraped_data.append({
#             'Restaurant_Name': restaurant_names[restaurant_element],
#             'Address': address,
#             'Order_Items': order_items,
#             'Prices': prices,
#             'No_of_Votes': no_of_votes
#             # Add more fields as needed
#         })

#         # Perform other scraping logic for the individual restaurant page

#         # After scraping, you may want to go back to the main page
#         driver.back()

#         # Wait for the main page to load again (you may need to adjust the waiting time)
#         time.sleep(5)

# # Close the browser
# driver.quit()

# # Convert the scraped data to CSV
# csv_filename = "scraped_data.csv"

# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Restaurant_Name', 'Address', 'Order_Items', 'Prices', 'No_of_Votes']  # Add more field names as needed
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(scraped_data)

# print(f"Scraped data saved to {csv_filename}")




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import csv

# driver = webdriver.Edge()

# urls = [
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
# ]

# # Create an empty list to store the scraped data
# scraped_data = []

# for url in urls:
#     driver.get(url)
#     time.sleep(5)  # Adjust the waiting time if needed

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#     for restaurant_element in range(min(2, len(restaurant_elements))):
#         # Scraping logic for restaurant names and links
#         name_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#         restaurant_names = [element.text for element in name_elements]

#         address_elements = driver.find_elements(by=By.XPATH, value='//*[@class="sc-clNaTc vNCcy"]')
#         addresses = [element.text for element in address_elements]

#      # Click on the "Order Online" link
#         order_online_link = driver.find_element(By.XPATH, '//*[@class="sc-jhaWeW hAbUan"]')
#         order_online_link.click()
#             # Wait for the "Order Online" section to load (you may need to adjust the waiting time)
#         time.sleep(5)

#             # Now, you can perform scraping logic for order items on the "Order Online" section
#         order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#         order_items = [element.text for element in order_item_elements]
      
#         # Add the scraped data to the list
#         scraped_data.append({
#             'Restaurant_Name': restaurant_names[restaurant_element] if restaurant_names else None,
#             'Address': addresses[restaurant_element] if addresses else None,
#             'Order_Items': order_items
#             # Add more fields as needed
#         })

#     # Perform other scraping logic for the individual restaurant page if needed

# # Close the browser
# driver.quit()

# # Convert the scraped data to CSV
# csv_filename = "scraped_data.csv"

# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Restaurant_Name', 'Address', 'Order_Items']  # Add more field names as needed
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(scraped_data)

# print(f"Scraped data saved to {csv_filename}")



#correct code--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import csv

# driver = webdriver.Edge()

# urls = [
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
# ]

# # Create an empty list to store the scraped data
# scraped_data = []

# for url in urls:
#     driver.get(url)
#     time.sleep(5)  # Adjust the waiting time if needed

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]

#     # Iterate over all restaurants
#     for restaurant_element in range(6):
#         # Get the restaurant name
#         current_restaurant_name = restaurant_name[restaurant_element]

#         # Click on the restaurant element to go to its page
#         restaurant_elements[restaurant_element].click()
#         time.sleep(5)

#         # Extract address
#         address_element = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#         address = [element.text for element in address_element]

#         price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#         prices = [element.text.replace('₹', '') for element in price_elements]

#         try:
#             # Click on the "Order Online" link
#             order_online_link = driver.find_element(By.XPATH, '//*[@class="sc-jhaWeW hAbUan"]')
#             order_online_link.click()
#             time.sleep(5)

#             # Now, you can perform scraping logic for order items on the "Order Online" section
#             order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#             order_items = [element.text for element in order_item_elements]

#             # Add the scraped data to the list
#             scraped_data.append({
#                 'Restaurant_Name': current_restaurant_name,
#                 'Address': address,
#                 'Prices': prices,
#                 'Order_Items': order_items
#                 # Add more fields as needed
#             })

#         except NoSuchElementException as e:
#             print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

#         # After scraping or if "Order Online" link not found, go back to the main page
#         finally:
#             driver.back()
#             time.sleep(2)
#             driver.back()


#             # Re-find restaurant elements after navigating back
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#             # Wait for the main page to load again
#             time.sleep(7)

# # Close the browser
# driver.quit()

# # Convert the scraped data to CSV
# csv_filename = "order_details.csv"

# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Restaurant_Name', 'Address','Prices','Order_Items']  # Add more field names as needed
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(scraped_data)

# print(f"Scraped data saved to {csv_filename}")


#trial full flatten----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import csv

# driver = webdriver.Edge()

# urls = [
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
# ]

# # Create an empty list to store the scraped data
# scraped_data = []

# for url in urls:
#     driver.get(url)
#     time.sleep(5)  # Adjust the waiting time if needed

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]

#     # Iterate over all restaurants
#     for restaurant_element in range(1):
#         # Get the restaurant name
#         current_restaurant_name = restaurant_name[restaurant_element]

#         # Click on the restaurant element to go to its page
#         restaurant_elements[restaurant_element].click()
#         time.sleep(5)

#         # Extract address
#         address_element = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#         address = [element.text for element in address_element]

#         price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#         prices = [element.text.replace('₹', '') for element in price_elements]

#         try:
#             # Click on the "Order Online" link
#             order_online_link = driver.find_element(By.XPATH, '//*[@class="sc-jhaWeW hAbUan"]')
#             order_online_link.click()
#             time.sleep(5)

#             # Now, you can perform scraping logic for order items on the "Order Online" section
#             order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#             order_items = [element.text for element in order_item_elements]

#             # Flatten order items with prices
#             flattened_order_items = []
#             for item, price in zip(order_items, prices):
#                 flattened_order_items.append({
#                     'Restaurant_Name': current_restaurant_name,
#                     'Address': address,
#                     'Order_Item': item,
#                     'Price': price
#                 })

#             # Add the flattened data to the list
#             scraped_data.extend(flattened_order_items)

#         except NoSuchElementException as e:
#             print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

#         # After scraping or if "Order Online" link not found, go back to the main page
#         finally:
#             driver.back()
#             time.sleep(2)
#             driver.back()

#             # Re-find restaurant elements after navigating back
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#             # Wait for the main page to load again
#             time.sleep(7)

# # Close the browser
# driver.quit()

# # Convert the scraped data to CSV
# csv_filename = "flattened_scraped_data.csv"

# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Restaurant_Name', 'Address', 'Order_Item', 'Price']  # Add more field names as needed
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(scraped_data)

# print(f"Flattened scraped data saved to {csv_filename}")




#flattens -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import csv

# def scrape_data(index):
#     name_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_names = [i.text for i in name_elements]
#     try:
#         # Click on the restaurant name to go to the individual link
#         name_elements[index].click()

#         # Wait for the page to load (you may need to adjust the waiting time)
#         time.sleep(5)

#         # Now, you can scrape data from the individual restaurant page

#         # Re-find the order item elements after navigating back
#         order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#         order_items = [element.text for element in order_item_elements]

#         # Return the scraped data as a list of dictionaries
#         return [{'Restaurant_Name': restaurant_names[index], 'Order_Item': order_item} for order_item in order_items]

#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# # Initialize the WebDriver
# driver = webdriver.Edge()
# url = r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Checkout Best Food Places To Eat In Agra _ Zomato.html"
# driver.get(url)

# # Wait for the elements to load
# time.sleep(2)

# # Scraping logic for restaurant names and links
# name_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
# restaurant_names = [i.text for i in name_elements]

# # Scrape data sequentially without threading
# results = []
# for index in range(len(name_elements)):
#     scraped_data = scrape_data(index)
#     if scraped_data is not None:
#         results.extend(scraped_data)

# # Close the browser
# driver.quit()


# print(results)

# # Convert the scraped data to CSV
# csv_filename = "scraped_data_sequential.csv"

# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=['Restaurant_Name', 'Order_Item'])
#     writer.writeheader()
#     writer.writerows(results)

# print(f"Scraped data saved to {csv_filename}")









#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import csv

# driver = webdriver.Edge()

# urls = [
#     r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html",
# ]

# # Create an empty list to store the scraped data
# scraped_data = []

# for url in urls:
#     driver.get(url)
#     time.sleep(5)  # Adjust the waiting time if needed

#     # Find restaurant elements
#     restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')
#     restaurant_name = [ele.text for ele in restaurant_elements]

#     # Iterate over all restaurants
#     for restaurant_element in range(3):
#         # Get the restaurant name
#         current_restaurant_name = restaurant_name[restaurant_element]

#         # Click on the restaurant element to go to its page
#         restaurant_elements[restaurant_element].click()
#         time.sleep(5)

#         # Extract address
#         address_element = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#         address = address_element.text

     
#         try:
#             # Click on the "Order Online" link
#             order_online_link = driver.find_element(By.XPATH, '//*[@class="sc-jhaWeW hAbUan"]')
#             order_online_link.click()
#             time.sleep(5)

#             # Now, you can perform scraping logic for order items on the "Order Online" section
#             order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#             order_items = [element.text for element in order_item_elements]

#             price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]') 
#             prices = [element.text.replace('₹', '') for element in price_elements]

#             votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#             no_of_votes = [element.text for element in votes_elements]

#             # Add the scraped data to the list
#             scraped_data.append({
#                 'Restaurant_Name': current_restaurant_name,
#                 'Address': address,
#                 'Prices': prices,
#                 'Order_Items': order_items,
#                 'Votes': no_of_votes
#             })

#         except NoSuchElementException as e:
#             print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

#         # After scraping or if "Order Online" link not found, go back to the main page
#         finally:
#             driver.back()
#             time.sleep(2)
#             driver.back()


#             # Re-find restaurant elements after navigating back
#             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#             # Wait for the main page to load again
#             time.sleep(7)

# # Close the browser
# driver.quit()

# # Convert the scraped data to CSV
# csv_filename = "order_data.csv"

# with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Restaurant_Name','Address','Prices','Order_Items','Votes']  # Add more field names as needed
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(scraped_data)

# print(f"Scraped data saved to {csv_filename}")




