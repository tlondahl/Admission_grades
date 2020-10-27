import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

path = '/Applications/chromedriver' #where i've saved the chrome driver locally
driver = webdriver.Chrome(path)
# driver.implicitly_wait(30)
driver.get('https://statistik.uhr.se/')

# Type in what you want to search for in the search field
search = driver.find_element_by_id('Search')
search.send_keys('Jur')



# Select the School
school = Select(driver.find_element_by_id('EducationOrgId'))
school.select_by_value('SU ')

# Select if you want to look at only programs, courses or both
prog = Select(driver.find_element_by_id('ProgKurs'))
prog.select_by_value('p')

# Variables I want to scrape
term = []
name = []
uni = []
applicants = []
BI = []
BII = []

# Define a function for iterating through several semesters
def iteration(terms):
    # Select witch semester
    semester = Select(driver.find_element_by_id('AdmissionRoundId'))
    # options = semester.options
    searches = 0
    for index in range(0, terms):
        semester.select_by_index(index)
        # Click on the search button
        driver.find_element_by_id('search-button').click()
        # Wait until the table emerges
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        WebDriverWait(driver, 10,ignored_exceptions=ignored_exceptions)\
            .until(EC.presence_of_element_located((By.ID, 'DataTables_Table_'+str(searches))))
        WebDriverWait(driver, 10)\
            .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr/td[1]')))
        term.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr/td[1]').text)
        name.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr/td[3]').text)
        uni.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr/td[5]').text)
        applicants.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr/td[6]').text)
        searches += 1
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/ul/li[3]/a/label').click()
        WebDriverWait(driver, 10)\
            .until(EC.presence_of_element_located((By.ID, 'DataTables_Table_'+str(searches))))
        WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr[2]/td[7]')))
        BI.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr[2]/td[7]').text)
        BII.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr[3]/td[7]').text)
        searches += 2
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/ul/li[1]/a/label').click()

iteration(10)

df = pd.DataFrame({
    'term': term,
    'name':name,
    'university': uni,
    'applicants': applicants,
    'BI': BI,
    'BII': BII
})
print(df.head().to_markdown())

