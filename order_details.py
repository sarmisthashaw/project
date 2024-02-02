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

#     try:
#         # Check if "Dining Out" element is present
#         dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')

#         # If present, click it and do something on the page, e.g., scrape data
#         dining_out_element.click()
#         time.sleep(5)

#         for i in range(10, 13):
#             for j in range(1, 4):
#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[' + str(i) + ']/div/div[' + str(
#                     j) + ']/div/div/a[2]')
#                 name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#                 print(name)
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)

#                 try:
#                     order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a')
#                     order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
#                     print("Order Online Link:", order_online_link)

#                     for f in range(1, 100):
#                         if order_online_link:
#                             driver.get(order_online_link[0])
#                             driver.implicitly_wait(10)
#                             food_items = driver.find_elements(By.XPATH,
#                                                                '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(
#                                                                    f) + ']/div/div/div[2]/div/div')
#                             if not food_items:
#                                 print(f"Food items list is out of range. Skipping {name}")
#                                 break

#                             print(food_items)
#                             for item in food_items:
#                                 print(item.text)

#                             time.sleep(5)

#                         rating_1 = 0
#                         star_elements = driver.find_elements(By.XPATH,
#                                                               '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(
#                                                                   f) + ']/div/div/div[2]/div/div/div[1]/div/i')

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

#                         rating = 0
#                         star_elements = driver.find_elements(By.XPATH,
#                                                               '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[' + str(
#                                                                   f) + ']/div/div/div[2]/div/div/div[1]/div/i')
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

#                     # Add the scraped data to the DataFrame
#                     restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                         'Restaurant Name': [name],
#                         'Rating': [ratings],
#                     })], ignore_index=True)

#                     # Save the DataFrame to a CSV file after scraping each restaurant
#                     restaurant_df.to_csv(f'{name}_details.csv', index=False)

#                     print(f"Scraped data for {name}")

#                 except NoSuchElementException:
#                     print(f'Order Online link not found on this page. Skipping...', rest_href)

#                 # After scraping, you can go back to the previous page if needed
#                 driver.back()
#                 time.sleep(5)

#     except NoSuchElementException:
#         print('Dining Out element not found on this page. Skipping...', link)

# # Save the final DataFrame to a CSV file after the outer loop
# restaurant_df.to_csv('order_details.csv', index=False)

# # Display the final DataFrame with restaurant details
# print(restaurant_df)

# # Close the browser
# driver.quit()

# #######################################################   Printing Rates  ###########################################################################

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup

# Create an empty DataFrame to store restaurant details
restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Order Items', 'Prices', 'Rating', 'Votes'])

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
                restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
                name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
                print(name)
                rest_href = restaurant_in.get_attribute('href')
                driver.get(rest_href)
                
                try:
                    order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
                    order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
                    print("Order Online Link:", order_online_link)
                    
                    for f in range(1, 100):
                        if order_online_link:
                            driver.get(order_online_link[0])
                            driver.implicitly_wait(10)
                            food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
                            if not food_items:
                                print(f"Food items list is out of range. Skipping {name}")
                                break

                            print(food_items)
                            for item in food_items:
                                print(item.text)
                            
                            time.sleep(5)

                        rating_1 = 0
                        star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

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
                        star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')
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
                        print("Rate",ratings)

                    # Add the scraped data to the DataFrame
                    restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
                        'Restaurant Name': [name],
                        'Rating': [ratings],
                    })], ignore_index=True)

                    print(f"Scraped data for {name}")

                except NoSuchElementException:
                    print(f'Order Online link not found on this page. Skipping...', rest_href)

                # After scraping, you can go back to the previous page if needed
                driver.back()
                time.sleep(5)

    except NoSuchElementException:
        print('Dining Out element not found on this page. Skipping...', link)

# Save the DataFrame to a CSV file after the outer loop
restaurant_df.to_csv('order_details.csv', index=False)

# Display the final DataFrame with restaurant details
print(restaurant_df)

# Close the browser
driver.quit()



# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Order Items', 'Prices', 'Rating', 'Votes'])

# driver = webdriver.Edge()

# url = "https://www.zomato.com/india"

# driver.get(url)
# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None


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
    
#     try:
#         # Check if "Dining Out" element is present
#         dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')
            
#             # If present, click it and do something on the page, e.g., scrape data
#         dining_out_element.click()
#         time.sleep(5)

#         for i in range(10, 13):
#             for j in range(1, 4):
#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div['+str(i)+']/div/div['+str(j)+']/div/div/a[2]')
#                 name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)
                
#                 try:
#                     order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
#                     order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
                    
#                     for f in range(1, 100):
#                         if order_online_link:
#                             driver.get(order_online_link[0])
#                             driver.implicitly_wait(10)

                            
#                             # Now, you can perform scraping logic for order items on the "Order Online" section
#                             order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#                             order_items = [element.text for element in order_item_elements]

#                             price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#                             prices = [element.text.replace('₹', '') for element in price_elements]

#                             rating_1 = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating_1 += 1
#                                     else:
#                                         rating_1 += 0
#                             except Exception as e:
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 linear_gradient = soup.svg.lineargradient
#                                 stops = linear_gradient.find_all('stop')
#                                 percentage = stops[1]['offset']
#                                 decimal_rating = int(percentage.strip('%')) / 100

#                                 rating_1 = decimal_rating

#                             rating = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')
#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating += 1
#                             except Exception as e:
#                                 # Handle specific exceptions or log the error
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 # linear_gradient= soup.svg.lineargradient
#                                 if linear_gradient:
#                                     linear_gradient_id = linear_gradient['id']
#                                     linear_gradient_x1 = linear_gradient['x1']
#                                     linear_gradient_x2 = linear_gradient['x2']

#                                     stops = linear_gradient.find_all('stop')
#                                     percentage = stops[1]['offset']
#                                     decimal_rating = int(percentage.strip('%')) / 100

#                                     rating = decimal_rating
#                             ratings = rating + rating_1

#                             votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#                             no_of_votes = [int(element.text.split()[0]) for element in votes_elements]
                            
#                                     # Re-find restaurant name after clicking
#                             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#                             # Find address elements
#                             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#                             addresses = [element.text for element in address_elements]

#                             # Extract city from the address
#                             city = extract_city(addresses[0]) if addresses else None
#                             food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
                                        

#                             # Add the scraped data to the DataFrame
#                             restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                                 'Restaurant Name': [name],
#                                 'Order Items': [order_items],
#                                 'Prices': [prices],
#                                 'Rating': [ratings],
#                                 'Votes': [no_of_votes]
#                             })], ignore_index=True)

#                 except NoSuchElementException:
#                     print(f'Order Online link not found on this page. Skipping...', rest_href)

#                 # After scraping, you can go back to the previous page if needed
#                 driver.back()

#     except NoSuchElementException:
#         print('Dining Out element not found on this page. Skipping...', link)

# # Save the DataFrame to a CSV file after the outer loop
# restaurant_df.to_csv('order_details.csv', index=False)

# # Close the browser
# driver.quit()



######################################### not saving in csv ###############################################################################
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup
# import time
# import re

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Order Items', 'Prices', 'Rating', 'Votes'])

# driver = webdriver.Edge()

# url = "https://www.zomato.com/india"

# driver.get(url)


# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None


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

#     try:
#         # Check if "Dining Out" element is present
#         dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')

#         # If present, click it and do something on the page, e.g., scrape data
#         dining_out_element.click()
#         time.sleep(5)

#         for i in range(10, 13):
#             for j in range(1, 4):
#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[' + str(i) + ']/div/div[' + str(
#                     j) + ']/div/div/a[2]')
#                 name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)

#                 try:
#                     order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
#                     order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
                    
#                     for f in range(1, 100):
#                         if order_online_link:
#                             driver.get(order_online_link[0])
#                             driver.implicitly_wait(10)

                            
#                             # Now, you can perform scraping logic for order items on the "Order Online" section
#                             order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#                             order_items = [element.text for element in order_item_elements]

#                             price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#                             prices = [element.text.replace('₹', '') for element in price_elements]

#                             rating_1 = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating_1 += 1
#                                     else:
#                                         rating_1 += 0
#                             except Exception as e:
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 linear_gradient = soup.svg.lineargradient
#                                 stops = linear_gradient.find_all('stop')
#                                 percentage = stops[1]['offset']
#                                 decimal_rating = int(percentage.strip('%')) / 100

#                                 rating_1 = decimal_rating

#                             rating = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')
#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating += 1
#                             except Exception as e:
#                                 # Handle specific exceptions or log the error
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 # linear_gradient= soup.svg.lineargradient
#                                 if linear_gradient:
#                                     linear_gradient_id = linear_gradient['id']
#                                     linear_gradient_x1 = linear_gradient['x1']
#                                     linear_gradient_x2 = linear_gradient['x2']

#                                     stops = linear_gradient.find_all('stop')
#                                     percentage = stops[1]['offset']
#                                     decimal_rating = int(percentage.strip('%')) / 100

#                                     rating = decimal_rating
#                             ratings = rating + rating_1

#                             votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#                             no_of_votes = [int(element.text.split()[0]) for element in votes_elements]
                            
#                                     # Re-find restaurant name after clicking
#                             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#                             # Find address elements
#                             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#                             addresses = [element.text for element in address_elements]

#                             # Extract city from the address
#                             city = extract_city(addresses[0]) if addresses else None
#                             food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
                                        

#                             # Print the extracted data
#                             print(f"Restaurant Name: {name}")
#                             print(f"Order Items: {order_items}")
#                             print(f"Prices: {prices}")
#                             print(f"Rating: {ratings}")
#                             print(f"Votes: {no_of_votes}")
#                             print("=" * 50)

#                             # Append the data to the DataFrame
#                             restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                                 'Restaurant Name': [name],
#                                 'Order Items': [order_items],
#                                 'Prices': [prices],
#                                 'Rating': [ratings],
#                                 'Votes': [no_of_votes]
#                             })], ignore_index=True)

#                     # Save the DataFrame to the CSV file after each iteration
#                     restaurant_df.to_csv('order_details.csv', index=False)

#                 except NoSuchElementException:
#                     print(f'Order Online link not found on this page. Skipping...', rest_href)

#                 # After scraping, you can go back to the previous page if needed
#                 driver.back()

#     except NoSuchElementException:
#         print('Dining Out element not found on this page. Skipping...', link)

# # Save the final DataFrame to a CSV file after the outer loop
# restaurant_df.to_csv('order_details.csv', index=False)

# # Close the browser
# driver.quit()

################################################repeated data #####################################################

# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup
# import time
# import re

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'Order Items', 'Prices', 'Rating', 'Votes'])

# driver = webdriver.Edge()

# url = "https://www.zomato.com/india"

# driver.get(url)


# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None


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

#     try:
#         # Check if "Dining Out" element is present
#         dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')

#         # If present, click it and do something on the page, e.g., scrape data
#         dining_out_element.click()
#         time.sleep(5)

#         for i in range(10, 13):
#             for j in range(1, 4):
#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[' + str(i) + ']/div/div[' + str(
#                     j) + ']/div/div/a[2]')
#                 name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)

#                 try:
#                     order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
#                     order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
                    
#                     for f in range(1, 100):
#                         if order_online_link:
#                             driver.get(order_online_link[0])
#                             driver.implicitly_wait(10)

#                             # Now, you can perform scraping logic for order items on the "Order Online" section
#                             order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#                             order_items = [element.text for element in order_item_elements]

#                             price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#                             prices = [element.text.replace('₹', '') for element in price_elements]

#                             rating_1 = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating_1 += 1
#                                     else:
#                                         rating_1 += 0
#                             except Exception as e:
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 linear_gradient = soup.svg.lineargradient
#                                 stops = linear_gradient.find_all('stop')
#                                 percentage = stops[1]['offset']
#                                 decimal_rating = int(percentage.strip('%')) / 100

#                                 rating_1 = decimal_rating

#                             rating = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')
#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating += 1
#                             except Exception as e:
#                                 # Handle specific exceptions or log the error
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 # linear_gradient= soup.svg.lineargradient
#                                 if linear_gradient:
#                                     linear_gradient_id = linear_gradient['id']
#                                     linear_gradient_x1 = linear_gradient['x1']
#                                     linear_gradient_x2 = linear_gradient['x2']

#                                     stops = linear_gradient.find_all('stop')
#                                     percentage = stops[1]['offset']
#                                     decimal_rating = int(percentage.strip('%')) / 100

#                                     rating = decimal_rating
#                             ratings = rating + rating_1

#                             votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#                             no_of_votes = [int(element.text.split()[0]) for element in votes_elements]
                            
#                             # Re-find restaurant name after clicking
#                             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#                             # Find address elements
#                             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#                             addresses = [element.text for element in address_elements]

#                             # Extract city from the address
#                             city = extract_city(addresses[0]) if addresses else None
#                             food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
                                        

#                             # Append the data to the DataFrame
#                             restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                                 'Restaurant Name': [name],
#                                 'City': [city],
#                                 'Order Items': [order_items],
#                                 'Prices': [prices],
#                                 'Rating': [ratings],
#                                 'Votes': [no_of_votes]
#                             })], ignore_index=True)

#                             # Save the DataFrame to the CSV file after scraping each restaurant
#                         restaurant_df.to_csv('order_details.csv', index=False)

#                 except NoSuchElementException:
#                     print(f'Order Online link not found on this page. Skipping...', rest_href)

#                 # After scraping, you can go back to the previous page if needed
#                 driver.back()

#     except NoSuchElementException:
#         print('Dining Out element not found on this page. Skipping...', link)

# # Save the final DataFrame to a CSV file after the outer loop
#     restaurant_df.to_csv('order_details.csv', index=False)

# # Close the browser
# driver.quit()



# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup
# import time
# import re

# # Create an empty DataFrame to store restaurant details
# restaurant_df = pd.DataFrame(columns=['Restaurant Name', 'City', 'Order Items', 'Prices', 'Rating', 'Votes'])

# driver = webdriver.Edge()

# url = "https://www.zomato.com/india"

# driver.get(url)


# def extract_city(address):
#     # Use a regular expression to extract the city name
#     match = re.search(r'(\w+)$', address)
#     if match:
#         return match.group(1)
#     return None


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

#     try:
#         # Check if "Dining Out" element is present
#         dining_out_element = driver.find_element(By.XPATH, '//div[@class="sc-gxbSSY fsqyAa" and text()="Dining Out"]')

#         # If present, click it and do something on the page, e.g., scrape data
#         dining_out_element.click()
#         time.sleep(5)

#         for i in range(10, 13):
#             for j in range(1, 4):
#                 restaurant_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[' + str(i) + ']/div/div[' + str(
#                     j) + ']/div/div/a[2]')
#                 name = restaurant_in.text.split('\n')[0]  # Extract only the restaurant name
#                 rest_href = restaurant_in.get_attribute('href')
#                 driver.get(rest_href)

#                 try:
#                     order_online_links = driver.find_elements(By.CSS_SELECTOR, '.sc-1y3q50z-5.jPTnRn a') 
#                     order_online_link = [link.get_attribute('href') for link in order_online_links if 'Order Online' in link.text]
                    
#                     for f in range(1, 100):
#                         if order_online_link:
#                             driver.get(order_online_link[0])
#                             driver.implicitly_wait(10)

#                             # Now, you can perform scraping logic for order items on the "Order Online" section
#                             order_item_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1s0saks-15 iSmBPS"]')
#                             order_items = [element.text for element in order_item_elements]

#                             price_elements = driver.find_elements(By.XPATH, '//*[@class="sc-17hyc2s-1 cCiQWA"]')
#                             prices = [element.text.replace('₹', '') for element in price_elements]

#                             rating_1 = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')

#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating_1 += 1
#                                     else:
#                                         rating_1 += 0
#                             except Exception as e:
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 linear_gradient = soup.svg.lineargradient
#                                 stops = linear_gradient.find_all('stop')
#                                 percentage = stops[1]['offset']
#                                 decimal_rating = int(percentage.strip('%')) / 100

#                                 rating_1 = decimal_rating

#                             rating = 0
#                             star_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div/div[1]/div/i')
#                             try:
#                                 for star in range(len(star_elements)):
#                                     html_string = star_elements[star].get_attribute('innerHTML')
#                                     soup = BeautifulSoup(html_string, 'lxml')
#                                     fill_value = soup.svg['fill']
#                                     title_text = soup.title.text
#                                     if fill_value == '#F3C117' and title_text == 'star-fill':
#                                         rating += 1
#                             except Exception as e:
#                                 # Handle specific exceptions or log the error
#                                 print(f"Error: {e}")

#                                 soup = BeautifulSoup(html_string, 'html.parser')
#                                 linear_gradient = soup.find('linearGradient')
#                                 # linear_gradient= soup.svg.lineargradient
#                                 if linear_gradient:
#                                     linear_gradient_id = linear_gradient['id']
#                                     linear_gradient_x1 = linear_gradient['x1']
#                                     linear_gradient_x2 = linear_gradient['x2']

#                                     stops = linear_gradient.find_all('stop')
#                                     percentage = stops[1]['offset']
#                                     decimal_rating = int(percentage.strip('%')) / 100

#                                     rating = decimal_rating
#                             ratings = rating + rating_1

#                             votes_elements = driver.find_elements(By.XPATH, '//*[@class="sc-z30xqq-4 hTgtKb"]')
#                             no_of_votes = [int(element.text.split()[0]) for element in votes_elements]
                            
#                             # Re-find restaurant name after clicking
#                             restaurant_elements = driver.find_elements(By.XPATH, '//*[@class="sc-1hp8d8a-0 sc-gkfylT ibDUIH"]') 

#                             # Find address elements
#                             address_elements = driver.find_elements(By.XPATH, '//*[@class="sc-clNaTc vNCcy"]')
#                             addresses = [element.text for element in address_elements]

#                             # Extract city from the address
#                             city = extract_city(addresses[0]) if addresses else None
#                             food_items = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div['+str(f)+']/div/div/div[2]/div/div')
                                        

#                             # Append the data to the DataFrame
#                             restaurant_df = pd.concat([restaurant_df, pd.DataFrame({
#                                 'Restaurant Name': [name],
#                                 'City': [city],
#                                 'Order Items': [order_items],
#                                 'Prices': [prices],
#                                 'Rating': [ratings],
#                                 'Votes': [no_of_votes]
#                             })], ignore_index=True)

#                 except NoSuchElementException:
#                     print(f'Order Online link not found on this page. Skipping...', rest_href)

#                 # After scraping, you can go back to the previous page if needed
#                 driver.back()

#     except NoSuchElementException:
#         print('Dining Out element not found on this page. Skipping...', link)

# # Save the final DataFrame to a CSV file after the outer loop
# restaurant_df.to_csv('order_details.csv', index=False)

# # Close the browser
# driver.quit()
