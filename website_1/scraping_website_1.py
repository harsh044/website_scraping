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
            page_data = []
            for url in a_tags_list:
                driver.get(url)

                single_page = driver.find_element(By.CSS_SELECTOR,'#content > div:nth-child(1) > div:nth-child(2)')

                try:
                    ex_title = single_page.find_element(By.CLASS_NAME,'exhibitor-title').text
                except NoSuchElementException:
                    ex_title = ''
                try:
                    ex_email = single_page.find_element(By.XPATH,'/html/body/div[6]/main/div/div/div[2]/div/div/div[2]/div/div/div[2]/div[4]/p[3]/a').text
                except NoSuchElementException:
                    ex_email = ''
                try:
                    ex_country = single_page.find_element(By.XPATH,'/html/body/div[6]/main/div/div/div[2]/div/div/div[2]/div/div/div[2]/div[3]').text
                except NoSuchElementException:
                    ex_country = ''
                try:
                    ex_address_1 = single_page.find_element(By.XPATH,'/html/body/div[6]/main/div/div/div[2]/div/div/div[2]/div/div/div[2]/div[1]').text
                except NoSuchElementException:
                    ex_address_1 = ''
                try:
                    ex_address_2 = single_page.find_element(By.XPATH,'/html/body/div[6]/main/div/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]').text
                except NoSuchElementException:
                    ex_address_2 = ''
                try:
                    ex_address_3 = single_page.find_element(By.XPATH,'/html/body/div[6]/main/div/div/div[2]/div/div/div[2]/div/div/div[2]/div[3]').text
                except NoSuchElementException:
                    ex_address_3 = ''
                try:
                    ex_phone_num = single_page.find_element(By.XPATH,'/html/body/div[6]/main/div/div/div[2]/div/div/div[2]/div/div/div[2]/div[4]/p[4]/a').text
                except NoSuchElementException:
                    ex_phone_num = ''

                ex_address = f"{ex_address_1},{ex_address_2},{ex_address_3}"
                data = {
                    'Company Name':ex_title,
                    'Address':ex_address,
                    'Email':ex_email,
                    'Mobile Number':ex_phone_num,
                    'Country':ex_country
                }
                page_data.append(data)
                print('title >',data)
            
            return page_data

        except Exception as e:
            raise e

    def star_scraping(self):
        try:
            count = 0
            flag = True
            for page_num in range(0,28):
                count += 1
                driver.get(f"https://www.frontale.de/en/exhibitors-products/find-exhibitors#e={page_num*2}0")

                time.sleep(5)

                try:
                    if flag:
                        popup_close_button = driver.find_element(By.ID, 'cmpwelcomebtnyes') #cmpboxbtn cmpboxbtnno cmptxt_btn_no
                        popup_close_button.click()
                        print("Closed the popup.")
                        flag = False
                    
                    time.sleep(5)

                    exhibitor_links = driver.find_elements(By.CSS_SELECTOR, '.search-result-list li')

                    a_tags_list = []
                    for list_tag in exhibitor_links:
                        # get all products page link 
                        a_tag = list_tag.find_element(By.TAG_NAME, 'a').get_attribute('href')

                        a_tags_list.append(a_tag)

                    company_data = self.page_scrape(a_tags_list)
                    company_df = pd.DataFrame(company_data)
                    company_df.to_excel(f'company_details_page_{count}.xlsx',index=False)
                    print('page_count >',count)
                except Exception as e:
                    raise e
        except Exception as e:
            print("No popup found or encountered an error:", str(e))
            raise e

if __name__=="__main__": 
    WebScraping().star_scraping()
