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
from concurrent.futures import ProcessPoolExecutor

# Set up the webdriver (make sure you have the appropriate webdriver installed, e.g., chromedriver)
driver = webdriver.Chrome()

# Replace the URL with the actual URL of the website you want to scrape
class WebScraping:
    def __init__(self):
        self.final_all_data = []

    def get_exhibition_link(self):
        try:
            url = "https://www.tube-tradefair.com/vis/v1/en/search?ticket=g_u_e_s_t&_query=&f_type=profile"
            driver.get(url)
            driver.maximize_window()

            for i in range(1,2000):
 
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
                try:
                    end = driver.find_element(By.XPATH,'//*[@id="vis-search-scroll-area"]/div[123]')
                    if end:
                        break
                except Exception as e:
                    print("NOt Found Last element > 123",i)
                    continue

            all_item_container = driver.find_element(By.ID,'vis-search-scroll-area')

            item_container = all_item_container.find_elements(By.CLASS_NAME,'searchresult-list')

            print('item_container count >',len(item_container))

            all_single_page_urls = []
            name_link_data = []
            
            for item in item_container:
                single_page_links = item.find_elements(By.CLASS_NAME,'searchresult-item')

                for link in single_page_links:
                    url = link.find_element(By.TAG_NAME,'a').get_attribute('href')
                    name_obj = link.find_element(By.CLASS_NAME,'searchresult-box__media__body')
                    name = name_obj.find_element(By.TAG_NAME,'h3').text
                    data = {
                        "Company Name":name,
                        "Company Url":url
                    }
                    name_link_data.append(data)
                    # all_single_page_urls.append(url)

            all_exhibition_details = pd.DataFrame(name_link_data)
            all_exhibition_details.to_excel(f'files_website_4/company_name_and_urls.xlsx',index=False)
            
            print('item_container count >',len(name_link_data))

            return ''

        except Exception as e:
            raise e
    
    def data_scrape(self,exhibition_link_list):
        try:
            cnt = 0
            final_all_data = []
            for url in exhibition_link_list:
                cnt+=1
                driver.get(url)

                time.sleep(10)
                try:
                    find_button = driver.find_element(By.CLASS_NAME,'profile__cta-buttons')
                    find_button.find_element(By.TAG_NAME,'button').click()
                    time.sleep(5)
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
                    return None
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
                    "Mobile Number":mobile_number
                }
                final_all_data.append(final_data)
                print('Count >',cnt)

            return final_all_data

        except Exception as e:
            raise e

    def chunks(self, l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]

    def star_scraping(self):
        try:
            # First extract all single exhibitions links
            # _ = self.get_exhibition_link()

            # this function run for scrape all details from exhibition
            company_name_urls = pd.read_excel('files_website_4/company_name_and_urls.xlsx')

            all_exhibition_links_list = company_name_urls['Company Url'].tolist()
            
            start_from = 100
            to_end = 300
            
            exhibition_details = self.data_scrape(all_exhibition_links_list[start_from:to_end])

            all_exhibition_details = pd.DataFrame(exhibition_details)
            all_exhibition_details.to_excel(f'files_website_4/company_details_{start_from}_to_{to_end}.xlsx',index=False)

        except Exception as e:
            print("No popup found or encountered an error:", str(e))
            raise e

if __name__=="__main__": 
    WebScraping().star_scraping()
