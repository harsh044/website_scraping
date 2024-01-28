from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
import multiprocessing as mp
from selenium.webdriver.common.action_chains import ActionChains

# Set up the webdriver (make sure you have the appropriate webdriver installed, e.g., chromedriver)
driver = webdriver.Chrome()

# Replace the URL with the actual URL of the website you want to scrape
class WebScraping:

    def get_exhibition_link(self):
        try:
            url = "https://www.tube-tradefair.com/vis/v1/en/search?ticket=g_u_e_s_t&_query=&f_type=profile"
            driver.get(url)

            scroll_count = 200
            # Scroll down the page by sending the SPACE key 'scroll_count' times
            for _ in range(scroll_count):
                driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
                time.sleep(10)
                print('count >',_)
            
            all_item_container = driver.find_element(By.ID,'vis-search-scroll-area')

            item_container = all_item_container.find_elements(By.CLASS_NAME,'searchresult-list')

            print('item_container count >',len(item_container))

            all_single_page_urls = []
            for item in item_container:
                single_page_links = item.find_elements(By.CLASS_NAME,'searchresult-item')

                for link in single_page_links:
                    url = link.find_element(By.TAG_NAME,'a').get_attribute('href')
                    all_single_page_urls.append(url)
            
            print('item_container count >',len(all_single_page_urls))

            return all_single_page_urls

        except Exception as e:
            raise e
    
    def data_scrape(self,exhibition_link_list):
        try:
            cnt = 0
            final_all_data = []
            for url in exhibition_link_list:
                cnt+=1
                driver.get(url)

                time.sleep(15)
                try:
                    find_button = driver.find_element(By.CLASS_NAME,'profile__cta-buttons')
                    find_button.find_element(By.TAG_NAME,'button').click()
                except Exception as e:
                    continue
                try:
                    company_obj = driver.find_element(By.ID,'profile-title')
                except Exception as e:
                    continue
                try:
                    company_name = company_obj.find_element(By.TAG_NAME,'h1').text
                except Exception as e:
                    company_name = ''

                try:
                    business_data = driver.find_element(By.ID,'profile-business-data')
                except Exception as e:
                    continue
                try:
                    address_1 = business_data.find_element(By.CLASS_NAME,'address-street').text
                except Exception as e:
                    address_1 = ''
                try:
                    address_2 = business_data.find_element(By.CLASS_NAME,'address-zip').text
                except Exception as e:
                    address_2 = ''
                try:
                    address_3 = business_data.find_element(By.CLASS_NAME,'address-city').text
                except Exception as e:
                    address_3 = ''

                try:
                    country = business_data.find_element(By.CLASS_NAME,'address-country').text
                except Exception as e:
                    country = ''

                address = f"{address_1},{address_2},{address_3},{country}"

                try:
                    email = (business_data.find_element(By.CLASS_NAME,'exh-contact-email').text).split(': ')[1]
                except Exception as e:
                    email = ''
                try:
                    mobile_number = (business_data.find_element(By.CLASS_NAME,'exh-contact-phone').text).split(': ')[1]
                except Exception as e:
                    mobile_number = ''

                final_data = {
                    "Company Name":company_name,
                    "Address":address,
                    "Country":country,
                    "E-mail":email,
                    "Mobile Number":mobile_number,
                    "Company Name":company_name,

                }
                final_all_data.append(final_data)
                print('Count >',cnt)

            return final_all_data
        except Exception as e:
            raise e
        
    def star_scraping(self):
        try:
            # First extract all single exhibitions links
            all_exhibition_links_list = self.get_exhibition_link()
            # all_exhibition_links_list = ['https://www.tube-tradefair.com/vis/v1/en/exhprofiles/v9CvrJxiRJSGlhsGImE7jw?oid=2370184&lang=2&_query=&f_type=profile']

            # this function run for scrape all details from exhibition
            exhibition_details = self.data_scrape(all_exhibition_links_list)

            all_exhibition_details = pd.DataFrame(exhibition_details)
            all_exhibition_details.to_excel(f'files_website_4/company_details.xlsx',index=False)

        except Exception as e:
            print("No popup found or encountered an error:", str(e))
            raise e

if __name__=="__main__": 
    WebScraping().star_scraping()

