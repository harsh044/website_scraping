from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup

# Set up the webdriver (make sure you have the appropriate webdriver installed, e.g., chromedriver)
driver = webdriver.Chrome()

# Replace the URL with the actual URL of the website you want to scrape
class WebScraping:

    def get_exhibition_link(self):
        url = "https://www.achema.de/en/search"
        driver.get(url)
        flag = True

        # Add a loop to navigate through multiple pages
        all_single_exhibition_link_list = []
        for page in range(0,226):
            time.sleep(10)

            if flag:
                cc_window = driver.find_element(By.CLASS_NAME,'cc-window')
                cc_compliance = cc_window.find_element(By.CLASS_NAME,'cc-compliance')
                cc_compliance.find_element(By.CLASS_NAME,'cc-all').click()
                flag = False
            
            # Wait for the new page content to load (replace the following with the appropriate conditions)
            time.sleep(10)
            new_page_content_locator = driver.find_element(By.ID,'ix-results-details')

            list_body = new_page_content_locator.find_elements(By.CLASS_NAME,'ix-result-row')
            single_exhibition_link_list = []
            cnt = 0
            for i in list_body:
                cnt+=1
                exhibition_link = i.find_element(By.TAG_NAME,'a').get_attribute('href')
                single_exhibition_link_list.append(exhibition_link)
                # print(f"{cnt} > {exhibition_link}")

            all_single_exhibition_link_list.append(single_exhibition_link_list)
            
            # Find and click the "Next" button
            next_button = driver.find_element(By.ID,'pagination')
            pages = next_button.find_elements(By.CLASS_NAME,'page-item')
            for p in pages:
                click_page = p.find_element(By.TAG_NAME,'a')
                if click_page.text:
                    if click_page.text == 'Next':
                        click_page.click()
                        break
                # print('page >',p.text)
            # next_button.click()
            # print('page_completed > ',page)
            page+=1
            print('getting_links >',page)
            
        # Close the webdriver when done
        final_exhibition_links_list = [item for sublist in all_single_exhibition_link_list for item in sublist]

        return final_exhibition_links_list

    def data_scrape(self,exhibition_link_list):
        try:
            cnt = 0
            all_data = []
            for link in exhibition_link_list:
                driver.get(link)

                time.sleep(5)

                name = driver.find_element(By.CLASS_NAME,'ix-name').text

                html = driver.page_source

                soup = BeautifulSoup(html, 'html.parser')

                # Extracting all detils
                all_details = [line.strip() for line in soup.find('div', {'id': 'ix-aussteller-address'}).stripped_strings]
                if not all_details:
                    continue
                name = all_details[0]
                address = f"{all_details[1]},{all_details[2]},{all_details[3]}"
                phone_number = all_details[all_details.index('Tel.:') + 1] if 'Tel.:' in all_details else ''
                country = all_details[3]
                email = all_details[all_details.index('E-Mail:') + 1] if 'E-Mail' in all_details else ''

                data = {
                    "Company Name":name,
                    "Address":address,
                    "Country":country,
                    "Mobile Number":phone_number,
                    "Email":email
                }
                cnt+=1
                print(cnt)
                all_data.append(data)

            return all_data
        except Exception as e:
            raise e
        
    def star_scraping(self):
        try:
            # First extract all single exhibitions links
            all_exhibition_links_list = self.get_exhibition_link()
            print('all_exhibition_links_list_count >',len(all_exhibition_links_list))

            # this function run for scrape all details from exhibition
            exhibition_details = self.data_scrape(all_exhibition_links_list)

            all_exhibition_details = pd.DataFrame(exhibition_details)
            all_exhibition_details.to_excel(f'files_website_3/company_details.xlsx',index=False)

        except Exception as e:
            print("No popup found or encountered an error:", str(e))
            raise e

if __name__=="__main__": 
    WebScraping().star_scraping()

