from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

# Open a website
class WebScraping:

    # driver.get(f"https://www.frontale.de/en/exhibitors-products/find-exhibitors#e={0}")
    def page_scrape(self,a_tags_list):
        try:
            cnt = 0
            page_data = []
            for url in a_tags_list:
                driver.get(url)
                cnt+=1

                time.sleep(2)
                try:
                    single_page = driver.find_element(By.CLASS_NAME,'info-holder')
                except NoSuchElementException:
                    continue

                try:
                    ex_title = single_page.find_element(By.CLASS_NAME,'headline-title').text
                except NoSuchElementException:
                    ex_title = ''
                try:
                    ex_email = single_page.find_element(By.CLASS_NAME,'ico_email').text
                except NoSuchElementException:
                    ex_email = ''
                try:
                    ex_country_address = single_page.find_element(By.CLASS_NAME,'location-info').text
                    ex_country = ex_country_address.split('\n')[-1]
                except NoSuchElementException:
                    ex_country = ''
                try:
                    ex_address = single_page.find_element(By.CLASS_NAME,'location-info').text
                except NoSuchElementException:
                    ex_address = ''
                try:
                    ex_phone_num = single_page.find_element(By.CLASS_NAME,'ico_phone').text
                except NoSuchElementException:
                    ex_phone_num = ''

                data = {
                    'Company Name':ex_title,
                    'Address':ex_address,
                    'Email':ex_email,
                    'Mobile Number':ex_phone_num,
                    'Country':ex_country
                }
                page_data.append(data)
                print('per_exhibition >',cnt)
                # print('title >',data)
            
            return page_data

        except Exception as e:
            raise e
    
    def single_exhibition_url(self,pagination):
        try:
            cnt = 0
            single_exhibition_page_data = []
            for url in pagination[:2]:
                driver.get(url)

                exhibition_container = driver.find_element(By.CLASS_NAME,'search-results')

                all_exhibition_container = exhibition_container.find_elements(By.CLASS_NAME,'col1ergebnis')
                all_exhibition_urls = []

                for exhibition_link in all_exhibition_container:
                    url = exhibition_link.find_element(By.CLASS_NAME,'initial_noline').get_attribute('href')
                    all_exhibition_urls.append(url)

                print('all_exhibition_urls_count >',len(all_exhibition_urls))
                
                # scrape exhibitions data
                company_data = self.page_scrape(all_exhibition_urls)

                # single_exhibition_page_data.append(company_data)
                cnt+=1
                print(cnt)
                            # save into excel file 
                company_df = pd.DataFrame(company_data)
                company_df.to_excel(f'files_website_2/company_details_page_{cnt}.xlsx',index=False)
                print('page_count >',cnt)
            
            return True
        except Exception as e:
            raise e

    def star_scraping(self):
        try:
            count = 0
            driver.get(f"https://www.eisenwarenmesse.com/eisenwarenmesse-exhibitors/list-of-exhibitors/")

            time.sleep(5)

            try:                
                # get all pages pagination_links
                exhibitor_container = driver.find_element(By.CLASS_NAME, 'search-results')
                pagination_links = exhibitor_container.find_elements(By.CLASS_NAME, 'entry')
                cnt = 0
                pagination = []

                for page_link in pagination_links:
                    link = page_link.find_element(By.TAG_NAME,'a').get_attribute('href')
                    pagination.append(link)
                    cnt+=1
                print(f"all_Pages_link_count> {len(pagination)}")
                
                company_data = self.single_exhibition_url(pagination)

            except Exception as e:
                raise e
        except Exception as e:
            print("No popup found or encountered an error:", str(e))
            raise e

if __name__=="__main__": 
    WebScraping().star_scraping()
