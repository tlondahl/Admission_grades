import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import time
import math
start_time = time.time()

path = '/Applications/chromedriver' #where i've saved the chrome driver locally
driver = webdriver.Chrome(path)
driver.get('https://statistik.uhr.se/')

# Type in what you want to search for in the search field
search = driver.find_element_by_id('Search')
search.send_keys('master')

# Select the School
school = Select(driver.find_element_by_id('EducationOrgId'))
school.select_by_value('SU ')

# Select if you want to look at only programs, courses or both
prog = Select(driver.find_element_by_id('ProgKurs'))
prog.select_by_value('p')

dfs = []
dfs2 = []
# Define a function for iterating through several semesters
def scraper(terms):
    def wait(): # A function for waiting until the tables are present after each search
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions) \
            .until(EC.presence_of_element_located((By.ID, 'DataTables_Table_' + str(searches))))
        WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr/td[1]')))
    # Select witch semester
    semester = Select(driver.find_element_by_id('AdmissionRoundId'))
    # options = semester.options
    searches = 0
    for index in range(0, terms):
        semester.select_by_index(index)
        # Click on the search button
        driver.find_element_by_id('search-button').click()
        # Wait until the table emerges
        wait()
        # Scrape the semester, name of the program, the school and number of applicants
        #current_page = int(driver.find_element_by_class_name('paginate_active').text)
        pages = 1
        number_of_pages = math.ceil(int(driver.find_element_by_id('DataTables_Table_'+str(searches)+'_info').text.split()[-2])/25)
        while pages <= number_of_pages:
            dfs.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click the button to get the gender data
        driver.find_element_by_xpath('//*[@id="Sub_Applying"]/div[2]/label').click()
        searches += 1
        pages = 1
        wait()
        while pages <= number_of_pages:
            dfs.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click the button to get age data
        driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/div[2]/div[1]/div[3]/label').click()
        searches += 1
        pages = 1
        wait()
        while pages <= number_of_pages:
            dfs.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click the button to get the admissions data
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/ul/li[3]/a/label').click()
        searches += 1
        pages = 1
        wait()
        while pages <= number_of_pages:
            dfs2.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click on the button for number of applicants
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/ul/li[1]/a/label').click()
        searches += 1
        # Click in the next page
        wait()
    driver.quit()




scraper(1)

print(dfs)
print('the script ran for ',time.time()-start_time,' seconds')
# df = dfs[0]

# dfs[-1].to_csv('admissions')


# df.to_csv('admission.csv')

