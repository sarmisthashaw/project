# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from bs4 import BeautifulSoup
# import re
# from concurrent.futures import ThreadPoolExecutor

# def extract_city(address):
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None

# def get_city_links(driver):
#     cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
#     cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

#     hrefs = []
#     for city, city_1 in zip(cities, cities_1):
#         link_0 = city.get_attribute('href')
#         link_1 = city_1.get_attribute('href')
#         hrefs.extend([link_0, link_1])

#     return hrefs

# def scrape_restaurant_data(driver, link, restaurant_df):
#     driver.get(link)

#     for i in range(10, 111):
#         for j in range(1, 4):
#             try:
#                 location_element = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[{i}]/div/div[{j}]/div/div/a[2]/div[3]/div[1]/p')
#                 location = location_element.text
#                 city = extract_city(location)

#                 restaurant_in = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[{i}]/div/div[{j}]/div/div/a[2]')
#                 name = restaurant_in.text.split('\n')[0]
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)

#                 try:
#                     order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a')
#                     order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]

#                     for z in range(2, 11):
#                         for f in range(1, 11):
#                             if order_online_link:
#                                 driver.get(order_online_link[0])
#                                 driver.implicitly_wait(10)
#                                 food_items = driver.find_elements(By.XPATH, f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{z}]/div[2]/div[{f}]/div/div/div[2]/div/div')

#                                 if not food_items:
#                                     print(f"Food items list is out of range. Skipping {name}")
#                                     break

#                                 data = []

#                                 for item in food_items:
#                                     food_item = item.text
#                                     split_data = food_item.split('\n')
#                                     data.append(split_data)

#                                 rating_1 = 0
#                                 star_elements = driver.find_elements(By.XPATH, f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{z}]/div[2]/div[{f}]/div/div/div[2]/div/div/div[1]/div/i')

#                                 try:
#                                     for star in range(len(star_elements)):
#                                         html_string = star_elements[star].get_attribute('innerHTML')
#                                         soup = BeautifulSoup(html_string, 'lxml')
#                                         fill_value = soup.svg['fill']
#                                         title_text = soup.title.text
#                                         if fill_value == '#F3C117' and title_text == 'star-fill':
#                                             rating_1 += 1
#                                         else:
#                                             rating_1 += 0
#                                 except Exception as e:
#                                     print(f"Error: {e}")

#                                     soup = BeautifulSoup(html_string, 'html.parser')
#                                     linear_gradient = soup.find('linearGradient')
#                                     stops = linear_gradient.find_all('stop')
#                                     percentage = stops[1]['offset']
#                                     decimal_rating = int(percentage.strip('%')) / 100
#                                     rating_1 = decimal_rating

#                                 rating = 0
#                                 star_elements = driver.find_elements(By.XPATH,f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{z}]/div[2]/div[{f}]/div/div/div[2]/div/div/div[1]/div/i')

#                                 try:
#                                     for star in range(len(star_elements)):
#                                         html_string = star_elements[star].get_attribute('innerHTML')
#                                         soup = BeautifulSoup(html_string, 'lxml')
#                                         fill_value = soup.svg['fill']
#                                         title_text = soup.title.text
#                                         if fill_value == '#F3C117' and title_text == 'star-fill':
#                                             rating += 1
#                                 except Exception as e:
#                                     print(f"Error: {e}")

#                                     soup = BeautifulSoup(html_string, 'html.parser')
#                                     linear_gradient = soup.find('linearGradient')
#                                     if linear_gradient:
#                                         linear_gradient_id = linear_gradient['id']
#                                         linear_gradient_x1 = linear_gradient['x1']
#                                         linear_gradient_x2 = linear_gradient['x2']

#                                         stops = linear_gradient.find_all('stop')
#                                         percentage = stops[1]['offset']
#                                         decimal_rating = int(percentage.strip('%')) / 100

#                                         rating = decimal_rating

#                                 ratings = rating + rating_1

#                                 restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                                     'Restaurant_Name': [name],
#                                     'City': [city],
#                                     'Cuisine': [data],
#                                     'Rating': [ratings],
#                                 })], ignore_index=True)
#                                 restaurant_df.to_csv('order_details.csv', index=False)

#                                 print(f"Scraped data for {name}")

#                 except NoSuchElementException:
#                     print(f'Order Online link not found on this page. Skipping...', rest_href)

#                 driver.back()
#                 time.sleep(5)

#             except NoSuchElementException:
#                 print(f'Element not found at XPath. Skipping to the next iteration...')

# def main():
#     restaurant_df = pd.DataFrame(columns=['Restaurant_Name', 'City', 'Cuisine', 'Rating'])
#     driver = webdriver.Edge()

#     url = "https://www.zomato.com/india"
#     driver.get(url)

#     time.sleep(5)

#     city_links = get_city_links(driver)

#     with ThreadPoolExecutor(max_workers=5) as executor:
#         executor.map(lambda link: scrape_restaurant_data(driver, link, restaurant_df), city_links)

#     print(restaurant_df)

#     driver.quit()

# if __name__ == "__main__":
#     main()

######################################################################################################## correct code   ############################################
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import re

# Create an empty DataFrame to store restaurant details
restaurant_df = pd.DataFrame(columns=['Restaurant_Name', 'City', 'Cuisine','Rating'])

driver = webdriver.Edge()

url = "https://www.zomato.com/india"
driver.get(url)

# Wait for the page to load (you can adjust the sleep time based on your needs)
time.sleep(5)
def extract_city(address):
    # Use a regular expression to extract the city name
    match = re.search(r'(\w+)$', address)
    if match:
        return match.group(1)
    return None

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
    
    for i in range(10, 111):
        for j in range(1, 4):
            try:
                location_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]/div[3]/div[1]/p')
                location = location_element.text

                city = extract_city(location) 

                restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
                name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
                print(name)
                rest_href = restaurant_in.get_attribute('href')
                driver.get(rest_href)

               
                
                try:
                    order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
                    order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
                    print("Order Online Link:", order_online_link)
                    
                    for z in range(2,11):
                        for f in range(1, 11):
                            if order_online_link:
                                driver.get(order_online_link[0])
                                driver.implicitly_wait(10)                   
                                food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section['+str(z)+']/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
                                if not food_items:
                                    print(f"Food items list is out of range. Skipping {name}")
                                    break

                                data = []

                                for item in food_items:
                                    food_item = item.text
                                    split_data = food_item.split('\n')
                                                                    
                                    data.append(split_data)
                                # print(data)

                                # df = pd.DataFrame(data)
                                # print(df)



                                    # print('food_item:',item.text)
                                
                                
                                time.sleep(5)

                                rating_1 = 0                                   
                                star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section['+str(z)+']/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

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

                                # Initialize 'rating'
                                rating = 0

                                star_elements = driver.find_elements(By.XPATH,'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section['+str(z)+']/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')
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
                                print("Rate", ratings)

                                # Add the scraped data to the DataFrame
                                restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
                                    'Restaurant_Name': [name],
                                    'City':[city],
                                    'Cuisine':[data],
                                    'Rating': [ratings],
                                })], ignore_index=True)
                                restaurant_df.to_csv('order_details.csv', index=False)


                                print(f"Scraped data for {name}")

                except NoSuchElementException:
                    print(f'Order Online link not found on this page. Skipping...', rest_href)

                # After scraping, you can go back to the previous page if needed
                driver.back()
                time.sleep(5)
                driver.back()

            except NoSuchElementException:
                print(f'Element not found at XPath. Skipping to the next iteration...')

# # Save the DataFrame to a CSV file after the outer loop
# restaurant_df.to_csv('order_details.csv', index=False)

# Display the final DataFrame with restaurant details
print(restaurant_df)

# Close the browser
driver.quit()

#################################################################### same ratings for each ############################################################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup

# import time
# import re

# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None

# def scrape_data(url, combined_df):
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
                
#                 # Initialize 'rating'
#                 rating = 0

#                 for f in range(1, 100):
#                     rating_1 = 0
#                     star_elements = driver.find_elements(By.XPATH,
#                                                             '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')

#                     try:
#                         for star in range(len(star_elements)):
#                             html_string = star_elements[star].get_attribute('innerHTML')
#                             soup = BeautifulSoup(html_string, 'lxml')
#                             fill_value = soup.svg['fill']
#                             title_text = soup.title.text
#                             if fill_value == '#F3C117' and title_text == 'star-fill':
#                                 rating_1 += 1
#                             else:
#                                 rating_1 += 0
#                     except Exception as e:
#                         print(f"Error: {e}")

#                         soup = BeautifulSoup(html_string, 'html.parser')
#                         linear_gradient = soup.find('linearGradient')
#                         linear_gradient = soup.svg.lineargradient
#                         stops = linear_gradient.find_all('stop')
#                         percentage = stops[1]['offset']
#                         decimal_rating = int(percentage.strip('%')) / 100

#                         rating_1 = decimal_rating

#                     star_elements = driver.find_elements(By.XPATH,
#                                                         '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')
#                     try:
#                         for star in range(len(star_elements)):
#                             html_string = star_elements[star].get_attribute('innerHTML')
#                             soup = BeautifulSoup(html_string, 'lxml')
#                             fill_value = soup.svg['fill']
#                             title_text = soup.title.text
#                             if fill_value == '#F3C117' and title_text == 'star-fill':
#                                 rating += 1
#                     except Exception as e:
#                         # Handle specific exceptions or log the error
#                         print(f"Error: {e}")

#                         soup = BeautifulSoup(html_string, 'html.parser')
#                         linear_gradient = soup.find('linearGradient')
#                         # linear_gradient= soup.svg.lineargradient
#                         if linear_gradient:
#                             linear_gradient_id = linear_gradient['id']
#                             linear_gradient_x1 = linear_gradient['x1']
#                             linear_gradient_x2 = linear_gradient['x2']

#                             stops = linear_gradient.find_all('stop')
#                             percentage = stops[1]['offset']
#                             decimal_rating = int(percentage.strip('%')) / 100

#                             rating = decimal_rating

#                     ratings = rating + rating_1

#                     # Add the scraped data to the list for the current restaurant
#                     restaurant_data.extend([{
#                         'Restaurant_Name': current_restaurant_name,
#                         "city": city,
#                         'Order_Items': order_item,
#                         'Prices': float(price) if price else None,
#                         'Rating': ratings,
#                         'Votes': votes
#                     } for order_item, price, votes in zip(order_items, prices, no_of_votes)])

#             except NoSuchElementException as e:
#                 print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

#             # After scraping or if "Order Online" link not found, go back to the main page
#             finally:
#                 driver.back()
#                 time.sleep(2)
#                 driver.back()

#                 # Re-find restaurant elements after navigating back
#                 restaurant_elements = driver.find_elements(By.XPATH,
#                                                             '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#                 # Wait for the main page to load again
#                 time.sleep(7)

#         # Convert the list of dictionaries to a DataFrame for the current restaurant
#         df_restaurant = pd.DataFrame(restaurant_data)

#         # Append the DataFrame for the current restaurant to the overall data list
#         data.append(df_restaurant)

#         # Combine the DataFrames for all restaurants into a single DataFrame
#         combined_df = pd.concat(data, ignore_index=True)

#         # Display the combined DataFrame
#         # print(combined_df)

#         # Save the combined DataFrame to a CSV file
#         combined_df.to_csv("combined_order.csv", index=False)

#     # Close the browser
#     driver.quit()

# if __name__ == "__main__":
#     urls = [
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
#         # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html"
#         # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
#     ]

#     combined_df = pd.DataFrame()

#     for url in urls:
#         scrape_data(url, combined_df)


###############################################################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup
# import time
# import re

# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None

# def scrape_data(url, combined_df):
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
#                 for f in range(1, 100):

#                     rating_1 = 0
#                     star_elements = driver.find_elements(By.XPATH,
#                                                           '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')

#                     try:
#                         for star in range(len(star_elements)):
#                             html_string = star_elements[star].get_attribute('innerHTML')
#                             soup = BeautifulSoup(html_string, 'lxml')
#                             fill_value = soup.svg['fill']
#                             title_text = soup.title.text
#                             if fill_value == '#F3C117' and title_text == 'star-fill':
#                                 rating_1 += 1
#                             else:
#                                 rating_1 += 0
#                     except Exception as e:
#                         print(f"Error: {e}")

#                         soup = BeautifulSoup(html_string, 'html.parser')
#                         linear_gradient = soup.find('linearGradient')
#                         linear_gradient = soup.svg.lineargradient
#                         stops = linear_gradient.find_all('stop')
#                         percentage = stops[1]['offset']
#                         decimal_rating = int(percentage.strip('%')) / 100

#                         rating_1 = decimal_rating

#                     # Initialize 'rating'
#                     rating = 0
#                     star_elements = driver.find_elements(By.XPATH,
#                                                           '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')
#                     try:
#                         for star in range(len(star_elements)):
#                             html_string = star_elements[star].get_attribute('innerHTML')
#                             soup = BeautifulSoup(html_string, 'lxml')
#                             fill_value = soup.svg['fill']
#                             title_text = soup.title.text
#                             if fill_value == '#F3C117' and title_text == 'star-fill':
#                                 rating += 1
#                     except Exception as e:
#                         # Handle specific exceptions or log the error
#                         print(f"Error: {e}")

#                         soup = BeautifulSoup(html_string, 'html.parser')
#                         linear_gradient = soup.find('linearGradient')
#                         # linear_gradient= soup.svg.lineargradient
#                         if linear_gradient:
#                             linear_gradient_id = linear_gradient['id']
#                             linear_gradient_x1 = linear_gradient['x1']
#                             linear_gradient_x2 = linear_gradient['x2']

#                             stops = linear_gradient.find_all('stop')
#                             percentage = stops[1]['offset']
#                             decimal_rating = int(percentage.strip('%')) / 100

#                             rating = decimal_rating
#                     ratings = rating + rating_1

#                     # Add the scraped data to the DataFrame
#                     restaurant_data.extend([{
#                         'Restaurant_Name': current_restaurant_name,
#                         "city": city,
#                         'Order_Items': order_item,
#                         'Prices': float(price) if price else None,
#                         'Rating': ratings,
#                         'Votes': votes
#                     } for order_item, price, votes in zip(order_items, prices, no_of_votes)])

#             except NoSuchElementException as e:
#                 print(f"Order Online link not found for {current_restaurant_name}. Skipping...")

#             # After scraping or if "Order Online" link not found, go back to the main page
#             finally:
#                 driver.back()
#                 time.sleep(2)
#                 driver.back()

#                 # Re-find restaurant elements after navigating back
#                 restaurant_elements = driver.find_elements(By.XPATH,
#                                                             '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]')

#                 # Wait for the main page to load again
#                 time.sleep(7)

#         # Convert the list of dictionaries to a DataFrame for the current restaurant
#         df_restaurant = pd.DataFrame(restaurant_data)

#         # Append the DataFrame for the current restaurant to the overall data list
#         data.append(df_restaurant)

#         # Close the browser
#         driver.quit()

#     # Combine the DataFrames for all restaurants into a single DataFrame
#     combined_df = pd.concat(data, ignore_index=True)

#     # Display the combined DataFrame
#     print(combined_df)

#     # Save the combined DataFrame to a CSV file
#     combined_df.to_csv("combined_order_1.csv", index=False)

# if __name__ == "__main__":
#     urls = [
#         r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html"
#         # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Bengaluru - Zomato.html"
#         # r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Kolkata - Zomato.html"
#     ]

#     combined_df = pd.DataFrame()

#     for url in urls:
#         scrape_data(url, combined_df)








################################################################### not printing data in csv ###################################################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from bs4 import BeautifulSoup

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Order Items', 'Prices', 'Rating', 'Votes'])

# driver = webdriver.Edge()

# url = "https://www.zomato.com/india"
# driver.get(url)

# # Wait for the page to load (you can adjust the sleep time based on your needs)
# time.sleep(5)

# # Find all the restaurant links using the appropriate XPath
# cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
# cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

# # Create a list to store the href values
# hrefs = []

# # Iterate through the found links and extract href attributes
# for city, city_1 in zip(cities, cities_1):
#     link_0 = city.get_attribute('href')
#     link_1 = city_1.get_attribute('href')
#     hrefs.extend([link_0, link_1])

# # Open each link in the browser
# for link in hrefs:
#     driver.get(link)
#     print(link)
    
#     for i in range(10, 111):
#         for j in range(1, 4):
#             try:
#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
#                 name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#                 print(name)
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)
                
#                 try:
#                     order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
#                     order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
#                     print("Order Online Link:", order_online_link)

#                     for p in range(2,10):
#                         for f in range(1, 21):
#                             if order_online_link:
#                                 driver.get(order_online_link[0])
#                                 food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section['+str(p)+']/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
#                                 if not food_items:
#                                     print(f"Food items list is out of range. Skipping {name}")
#                                     break

#                                 for item in food_items:
#                                     print('food_item:', item.text)
#                                     print('-------------------------------')

#                                     # Extract food item details
#                                     food_name = item.find_element(By.XPATH, './/div/div[1]').text
#                                     print('food_name',food_name)
#                                     price = item.find_element(By.XPATH, './/div/div[2]/div[1]').text
#                                     print('price',price)

#                                     votes = item.find_element(By.XPATH, './/div/div[2]/div[2]').text

                                
#                                 time.sleep(5)

#                                 rating_1 = 0                                   
#                                 star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

#                                 try:
#                                     for star in range(len(star_elements)):
#                                         html_string = star_elements[star].get_attribute('innerHTML')
#                                         soup = BeautifulSoup(html_string, 'lxml')
#                                         fill_value = soup.svg['fill']
#                                         title_text = soup.title.text
#                                         if fill_value == '#F3C117' and title_text == 'star-fill':
#                                             rating_1 += 1
#                                         else:
#                                             rating_1 += 0
#                                 except Exception as e:
#                                     print(f"Error: {e}")

#                                     soup = BeautifulSoup(html_string, 'html.parser')
#                                     linear_gradient = soup.find('linearGradient')
#                                     linear_gradient = soup.svg.lineargradient
#                                     stops = linear_gradient.find_all('stop')
#                                     percentage = stops[1]['offset']
#                                     decimal_rating = int(percentage.strip('%')) / 100

#                                     rating_1 = decimal_rating

#                                 # Initialize 'rating'
#                                 rating = 0

#                                 star_elements = driver.find_elements(By.XPATH,'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')
#                                 try:
#                                     for star in range(len(star_elements)):
#                                         html_string = star_elements[star].get_attribute('innerHTML')
#                                         soup = BeautifulSoup(html_string, 'lxml')
#                                         fill_value = soup.svg['fill']
#                                         title_text = soup.title.text
#                                         if fill_value == '#F3C117' and title_text == 'star-fill':
#                                             rating += 1
#                                 except Exception as e:
#                                     # Handle specific exceptions or log the error
#                                     print(f"Error: {e}")

#                                     soup = BeautifulSoup(html_string, 'html.parser')
#                                     linear_gradient = soup.find('linearGradient')
#                                     # linear_gradient= soup.svg.lineargradient
#                                     if linear_gradient:
#                                         linear_gradient_id = linear_gradient['id']
#                                         linear_gradient_x1 = linear_gradient['x1']
#                                         linear_gradient_x2 = linear_gradient['x2']

#                                         stops = linear_gradient.find_all('stop')
#                                         percentage = stops[1]['offset']
#                                         decimal_rating = int(percentage.strip('%')) / 100

#                                         rating = decimal_rating

#                                 ratings = rating + rating_1
#                                 print("Rate", ratings)

#                                 # Add the scraped data to the DataFrame
#                                 restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                                         'Restaurant Name': [name],
#                                         'Order Items': [food_name],
#                                         'Prices': [price],
#                                         'Votes': [votes],
#                                     })], ignore_index=True)
#                                 print(f"Scraped data for {name}")

#                 except NoSuchElementException:
#                     print(f'Order Online link not found on this page. Skipping...', rest_href)

#                 # After scraping, you can go back to the previous page if needed
#                 driver.back()
#                 time.sleep(5)

#             except NoSuchElementException:
#                 print(f'Element not found at XPath. Skipping to the next iteration...')

# # Save the DataFrame to a CSV file after the outer loop
#     restaurant_df.to_csv('order_details.csv', index=False)

# # Display the final DataFrame with restaurant details
# print(restaurant_df)

# # Close the browser
# driver.quit()




####################################################### giving star rating ###################################################################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from bs4 import BeautifulSoup

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Order Items', 'Prices', 'Rating', 'Votes'])

# driver = webdriver.Edge()

# url = "https://www.zomato.com/india"
# driver.get(url)

# # Wait for the page to load (you can adjust the sleep time based on your needs)
# time.sleep(5)

# # Find all the restaurant links using the appropriate XPath
# cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
# cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

# # Create a list to store the href values
# hrefs = []

# # Iterate through the found links and extract href attributes
# for city, city_1 in zip(cities, cities_1):
#     link_0 = city.get_attribute('href')
#     link_1 = city_1.get_attribute('href')
#     hrefs.extend([link_0, link_1])

# # Open each link in the browser
# for link in hrefs:
#     driver.get(link)
#     print(link)
    
#     for i in range(10, 111):
#         for j in range(1, 4):
#             restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
#             name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#             print(name)
#             rest_href = restaurant_in.get_attribute('href')
#             driver.get(rest_href)
            
#             try:
#                 order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
#                 order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
#                 print("Order Online Link:", order_online_link)
                
#                 for f in range(1, 100):
#                     if order_online_link:
#                         driver.get(order_online_link[0])
#                         driver.implicitly_wait(10)
#                         food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
#                         if not food_items:
#                             print(f"Food items list is out of range. Skipping {name}")
#                             break

#                         print(food_items)
#                         for item in food_items:
#                             print(item.text)
                        
#                         time.sleep(5)

#                         rating_1 = 0                                   
#                         star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

#                         try:
#                             for star in range(len(star_elements)):
#                                 html_string = star_elements[star].get_attribute('innerHTML')
#                                 soup = BeautifulSoup(html_string, 'lxml')
#                                 fill_value = soup.svg['fill']
#                                 title_text = soup.title.text
#                                 if fill_value == '#F3C117' and title_text == 'star-fill':
#                                     rating_1 += 1
#                                 else:
#                                     rating_1 += 0
#                         except Exception as e:
#                             print(f"Error: {e}")

#                             soup = BeautifulSoup(html_string, 'html.parser')
#                             linear_gradient = soup.find('linearGradient')
#                             linear_gradient = soup.svg.lineargradient
#                             stops = linear_gradient.find_all('stop')
#                             percentage = stops[1]['offset']
#                             decimal_rating = int(percentage.strip('%')) / 100

#                             rating_1 = decimal_rating

#                         # Initialize 'rating'
#                         rating = 0

#                         star_elements = driver.find_elements(By.XPATH,'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(f) + ']/div/div/div[2]/div/div/div[1]/div/i')
#                         try:
#                             for star in range(len(star_elements)):
#                                 html_string = star_elements[star].get_attribute('innerHTML')
#                                 soup = BeautifulSoup(html_string, 'lxml')
#                                 fill_value = soup.svg['fill']
#                                 title_text = soup.title.text
#                                 if fill_value == '#F3C117' and title_text == 'star-fill':
#                                     rating += 1
#                         except Exception as e:
#                             # Handle specific exceptions or log the error
#                             print(f"Error: {e}")

#                             soup = BeautifulSoup(html_string, 'html.parser')
#                             linear_gradient = soup.find('linearGradient')
#                             # linear_gradient= soup.svg.lineargradient
#                             if linear_gradient:
#                                 linear_gradient_id = linear_gradient['id']
#                                 linear_gradient_x1 = linear_gradient['x1']
#                                 linear_gradient_x2 = linear_gradient['x2']

#                                 stops = linear_gradient.find_all('stop')
#                                 percentage = stops[1]['offset']
#                                 decimal_rating = int(percentage.strip('%')) / 100

#                                 rating = decimal_rating

#                         ratings = rating + rating_1
#                         print("Rate", ratings)

#                         # Add the scraped data to the DataFrame
#                         restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                             'Restaurant Name': [name],
#                             'Rating': [ratings],
#                         })], ignore_index=True)

#                         print(f"Scraped data for {name}")

#             except NoSuchElementException:
#                 print(f'Order Online link not found on this page. Skipping...', rest_href)

#             # After scraping, you can go back to the previous page if needed
#             driver.back()
#             time.sleep(5)

# # Save the DataFrame to a CSV file after the outer loop
# restaurant_df.to_csv('order_details.csv', index=False)

# # Display the final DataFrame with restaurant details
# print(restaurant_df)

# # Close the browser
# driver.quit()



########################################################## find_all error #########################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# from bs4 import BeautifulSoup

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Order Items', 'Prices', 'Rating', 'Votes'])

# driver = webdriver.Edge()

# url = "https://www.zomato.com/india"
# driver.get(url)

# # Wait for the page to load (you can adjust the sleep time based on your needs)
# time.sleep(5)

# # Find all the restaurant links using the appropriate XPath
# cities = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 fTtEw"]/a')
# cities_1 = driver.find_elements(By.XPATH, '//div[@class="sc-bke1zw-1 bcVYKA"]/a')

# # Create a list to store the href values
# hrefs = []

# # Iterate through the found links and extract href attributes
# for city, city_1 in zip(cities, cities_1):
#     link_0 = city.get_attribute('href')
#     link_1 = city_1.get_attribute('href')
#     hrefs.extend([link_0, link_1])

# # Open each link in the browser
# for link in hrefs:
#     driver.get(link)
#     print(link)
    
#     for i in range(10, 13):
#         for j in range(1, 4):
#             restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
#             name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#             print(name)
#             rest_href = restaurant_in.get_attribute('href')
#             driver.get(rest_href)
            
#             try:
#                 order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
#                 order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
#                 print("Order Online Link:", order_online_link)
                
#                 for f in range(1, 100):
#                     if order_online_link:
#                         driver.get(order_online_link[0])
#                         driver.implicitly_wait(10)
#                         food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
#                         if not food_items:
#                             print(f"Food items list is out of range. Skipping {name}")
#                             break

#                         print(food_items)
#                         for item in food_items:
#                             print(item.text)
                        
#                         time.sleep(5)

#                     rating_1 = 0
#                     star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

#                     try:
#                         for star in range(len(star_elements)):
#                             html_string = star_elements[star].get_attribute('innerHTML')
#                             soup = BeautifulSoup(html_string, 'lxml')
#                             fill_value = soup.svg['fill']
#                             title_text = soup.title.text
#                             if fill_value == '#F3C117' and title_text == 'star-fill':
#                                 rating_1 += 1
#                             else:
#                                 rating_1 += 0
#                     except Exception as e:
#                         print(f"Error: {e}")

#                         soup = BeautifulSoup(html_string, 'html.parser')
#                         linear_gradient = soup.find('linearGradient')
#                         stops = linear_gradient.find_all('stop')
#                         percentage = stops[1]['offset']
#                         decimal_rating = int(percentage.strip('%')) / 100

#                         rating_1 = decimal_rating

#                     rating = 0
#                     star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')
#                     try:
#                         for star in range(len(star_elements)):
#                             html_string = star_elements[star].get_attribute('innerHTML')
#                             soup = BeautifulSoup(html_string, 'lxml')
#                             fill_value = soup.svg['fill']
#                             title_text = soup.title.text
#                             if fill_value == '#F3C117' and title_text == 'star-fill':
#                                 rating += 1
#                     except Exception as e:
#                         # Handle specific exceptions or log the error
#                         print(f"Error: {e}")

#                         soup = BeautifulSoup(html_string, 'html.parser')
#                         linear_gradient = soup.find('linearGradient')
#                         if linear_gradient:
#                             linear_gradient_id = linear_gradient['id']
#                             linear_gradient_x1 = linear_gradient['x1']
#                             linear_gradient_x2 = linear_gradient['x2']

#                             stops = linear_gradient.find_all('stop')
#                             percentage = stops[1]['offset']
#                             decimal_rating = int(percentage.strip('%')) / 100

#                             rating = decimal_rating
#                     ratings = rating + rating_1
#                     print("Rate",ratings)

#                 # Add the scraped data to the DataFrame
#                 restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                     'Restaurant Name': [name],
#                     'Rating': [ratings],
#                 })], ignore_index=True)

#                 print(f"Scraped data for {name}")

#             except NoSuchElementException:
#                 print(f'Order Online link not found on this page. Skipping...', rest_href)

#             # After scraping, you can go back to the previous page if needed
#             driver.back()
#             time.sleep(5)

# # Save the DataFrame to a CSV file after the outer loop
# restaurant_df.to_csv('order_details.csv', index=False)

# # Display the final DataFrame with restaurant details
# print(restaurant_df)

# # Close the browser
# driver.quit()





######################################################################################################################################################################################################################3
# # from selenium import webdriver
# # import pandas as pd
# # import numpy as np
# # from selenium.webdriver.common.by import By
# # from selenium.common.exceptions import NoSuchElementException
# # import time
# # import csv
# # from concurrent.futures import ThreadPoolExecutor
# # from tqdm import tqdm
# # import requests
# # from bs4 import BeautifulSoup






# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup

# # Launch the Edge browser
# driver = webdriver.Edge()

# # Open the local HTML file
# driver.get(r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html")

# # Find the element and extract information
# rest = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[10]/div/div[2]/div/div/a[2]')
# print("Restaurant Name:", rest.text)
# print("Restaurant URL:", rest.get_attribute('href'))

# # Directly use the URL obtained earlier
# url = 'https://www.zomato.com/agra/bistro-57-1-civil-lines/info'
# driver.get(url)
# dat = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/article/div') 
# for i in dat:
#     print(i.text)
# #     print(i.get_attribute('href'))
#     print('-----------')

# url = 'https://www.zomato.com/agra/bistro-57-1-civil-lines/info'
# driver.get(url)

# # Wait for the data to load, you can adjust the wait time as needed
# driver.implicitly_wait(10)

# # Fetch the HTML content after the page has loaded
# html_content = driver.page_source

# # Use BeautifulSoup to parse the HTML content
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find all 'a' tags within the specified class
# hrefs = soup.select('.sc-1y3q50z-5.jPTnRn a')

# # Extract and print the href values
# link = []
# order_online_tab = []
# for href in hrefs:
#     print(href.get('href'))
#     link.append(href.get('href'))
# order_online_link = [i for i in link if 'order' in i]
# order_online_tab.append(order_online_link)
# print(order_online_link)

# driver.quit()



#################################### All Links ##########################################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # Launch the Edge browser
# driver = webdriver.Edge()

# # Open the local HTML file
# driver.get(r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html")

# # Find the element and extract information
# rest = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[10]/div/div[2]/div/div/a[2]')
# print("Restaurant Name:", rest.text)
# print("Restaurant URL:", rest.get_attribute('href'))

# # Use the URL obtained earlier
# url = 'https://www.zomato.com/agra/bistro-57-1-civil-lines/info'
# driver.get(url)

# # Wait for the data to load, you can adjust the wait time as needed
# driver.implicitly_wait(10)

# # Find all 'a' tags within the specified class
# order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a')

# # Extract and print the href values
# for link in order_online_links:
#     print(link.get_attribute('href'))

################################################### order tab link #############################################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # Launch the Edge browser
# driver = webdriver.Edge()

# # Open the local HTML file
# driver.get(r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html")

# # Find the element and extract information
# rest = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[10]/div/div[2]/div/div/a[2]')
# print("Restaurant Name:", rest.text)
# print("Restaurant URL:", rest.get_attribute('href'))

# # Use the URL obtained earlier
# url = 'https://www.zomato.com/agra/bistro-57-1-civil-lines/info'
# driver.get(url)

# # Wait for the data to load, you can adjust the wait time as needed
# driver.implicitly_wait(10)

# # Find all 'a' tags within the specified class
# order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a')

# # Extract and print the href values for 'Order Online' links
# order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
# print(order_online_link)

############################################## order data ##############################################
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # Launch the Edge browser
# driver = webdriver.Edge()

# # Open the local HTML file
# driver.get(r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html")

# # Find the element and extract information
# rest = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[10]/div/div[2]/div/div/a[2]')
# print("Restaurant Name:", rest.text)
# print("Restaurant URL:", rest.get_attribute('href'))

# # Use the URL obtained earlier
# url = 'https://www.zomato.com/agra/bistro-57-1-civil-lines/info'
# driver.get(url)

# # Wait for the data to load, you can adjust the wait time as needed
# driver.implicitly_wait(10)

# # Find all 'a' tags within the specified class
# order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 

# # Extract and print the href values for 'Order Online' links
# order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
# print(order_online_link)


# # Find and print the text content of the specified div using the given XPath
# order_link = 'https://www.zomato.com/agra/bistro-57-1-civil-lines/order'
# driver.get(order_link)
# div_data = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[1]/div/div/div[2]/div/div')
# # Access the first element in the list and print its text content
# if div_data:
#     print("Div Data:", div_data[0].text)
# else:
#     print("Div Data not found")

############################################ Star data ###########################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # Launch the Edge browser
# driver = webdriver.Edge()

# # Open the local HTML file or navigate to the webpage
# # In this case, we navigate to the 'Order Online' link
# order_link = 'https://www.zomato.com/agra/bistro-57-1-civil-lines/order'
# driver.get(order_link)

# # Wait for the data to load, you can adjust the wait time as needed
# driver.implicitly_wait(10)

# # Find and print the text content of the specified div using the given XPath
# div_data = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[1]/div/div/div[2]/div/div')
# # Access the first element in the list and print its text content
# if div_data:
#     print("Div Data:", div_data[0].text)

#     # Extract the color code of the first star from the star rating
# #     star_color_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/i[1]')
#     star_color_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div')
#     print(star_color_element)                     

#     print(star_color_element.text)                     
#     star_color_style = star_color_element.get_attribute('style')
#     print('colour code:', star_color_style)
    
#     # Extract the color code from the style attribute
#     color_code = star_color_style.split(':')[1].strip()  # Assuming the color information is after the colon
    
#     print("Star Color Code:", color_code)

# else:
#     print("Div Data not found")

# # Close the browser
# driver.quit()
# ###################################################################################  float 48%        ############################################################################################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup

# # Launch the Edge browser
# driver = webdriver.Edge()

# # Open the local HTML file
# driver.get(r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html")

# # Find the element and extract information
# rest = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[10]/div/div[1]/div/div/a[2]')  
# restaurant_name = rest.text
# restaurant_url = rest.get_attribute('href')

# print("Restaurant Name:", restaurant_name)
# print("Restaurant URL:", restaurant_url)

# # Use the URL obtained earlier
# driver.get(restaurant_url)

# # Find all 'a' tags within the specified class
# order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 

# # Extract and print the href values for 'Order Online' links
# order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
# print("Order Online Link:", order_online_link)

# # Check if there is an 'Order Online' link, then proceed
# if order_online_link:
#     # Navigate to the 'Order Online' link
#     driver.get(order_online_link[0])

#     # Wait for the data to load, you can adjust the wait time as needed
#     driver.implicitly_wait(10)
    
#     # Find all <i> tags within the specified XPath
#     star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[1]/div/div/div[2]/div/div/div[1]/div/i')
    
#     # Initialize a variable to store the total ratings
#     total_ratings = 0



#     # Print the total ratings
#     print("Total Ratings:", total_ratings)

# else:
#     print("Order Online link not found.")

# # Close the browser
# driver.quit()

####################################################################################################################


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup

# # Launch the Edge browser
# driver = webdriver.Edge()

# # Open the local HTML file
# driver.get(r"C:\Users\SRIJAN\OneDrive - S. Jaykishan\Desktop\Project Data\Trending dining restaurants in Agra - Zomato.html")

# # Find the element and extract information
# rest = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[10]/div/div[1]/div/div/a[2]')  
# restaurant_name = rest.text
# restaurant_url = rest.get_attribute('href')

# print("Restaurant Name:", restaurant_name)
# print("Restaurant URL:", restaurant_url)

# # Use the URL obtained earlier
# driver.get(restaurant_url)

# # Find all 'a' tags within the specified class
# order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 

# # Extract and print the href values for 'Order Online' links
# order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
# print("Order Online Link:", order_online_link)

# # Check if there is an 'Order Online' link, then proceed
# if order_online_link:
#     # Navigate to the 'Order Online' link
#     driver.get(order_online_link[0])

#     # Wait for the data to load, you can adjust the wait time as needed
#     driver.implicitly_wait(10)
#     food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[1]/div/div/div[2]/div/div')
#     print(food_items)
    
#     # Iterate through each food item
#     for food_item in food_items:
#         print(food_item.text)

#         # Find all <i> tags within the specified XPath for the current food item
#         star_elements = food_item.find_elements(By.XPATH, './div/i')
        
#         # Initialize a variable to store the total ratings for the current food item
#         total_ratings = 0

#         # Iterate through each <i> element and extract the color and ratings
#         for star_element in star_elements:
#             # Extract the color attribute
#             star_color = star_element.get_attribute('color')
#             print("color:", star_color)
            
#             # Check if the color is yellow (#F3C117) for solid fill
#             if star_color.lower() == "#f3c117":
#                 # Add 1 rating for solid fill
#                 total_ratings += 1

#             elif "linear-gradient" in star_element.get_attribute('style'):
#                 # If gradient fill, extract the stops
#                 stops = star_element.get_attribute('style').split("stop-color=")
                
#                 # Find the stop with the color #F3C117
#                 for stop in stops:
#                     if "#F3C117" in stop:
#                         # Extract the offset percentage using the provided logic
#                         percentage_string = stop.split('"')[1][:-1]
#                         percentage_integer = int(percentage_string.rstrip('%'))
#                         offset_percentage = percentage_integer / 100.0
#                         print("percentage:", offset_percentage)
                        
#                         # Add the offset as a decimal to total ratings
#                         total_ratings += offset_percentage
#                         break  # Break after finding the stop with the color #F3C117

#         # Print the total ratings for the current food item
#         print("Total Ratings for the current food item:", total_ratings)
#         print("-" * 50)

# else:
#     print("Order Online link not found.")

# # Close the browser
# driver.quit()
