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

pd.set_option('display.max_columns', None)

path = '/Applications/chromedriver' #where i've saved the chrome driver locally
driver = webdriver.Chrome(path)
driver.get('https://statistik.uhr.se/')

# Type in what you want to search for in the search field
# search = driver.find_element_by_id('Search')
# search.send_keys('kandidat')

# Select the School
school = Select(driver.find_element_by_id('EducationOrgId'))
school.select_by_value('SU ')

# Select if you want to look at only programs, courses or both
prog = Select(driver.find_element_by_id('ProgKurs'))
prog.select_by_value('p')

applicants_dfs = []
gender_dfs = []
age_dfs = []
admission_dfs = []

# Define a function for iterating through several semesters
def scraper(terms):
    def wait(): # A function for waiting until the tables are present after each search
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions) \
            .until(EC.presence_of_element_located((By.ID, 'DataTables_Table_' + str(searches))))
        WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div[4]/div/table/tbody/tr/td[1]')))
    # Select which semester
    semester = Select(driver.find_element_by_id('AdmissionRoundId'))
    # options = semester.options
    searches = 0
    for index in range(0, terms):
        if index == 13: #To skip the spring semester of 2021 since it has no admission data
            continue
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
            applicants_dfs.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click the button to get the gender data
        driver.find_element_by_xpath('//*[@id="Sub_Applying"]/div[2]/label').click()
        searches += 1
        pages = 1
        wait()
        while pages <= number_of_pages:
            gender_dfs.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click the button to get age data
        driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/div[2]/div[1]/div[3]/label').click()
        searches += 1
        pages = 1
        wait()
        while pages <= number_of_pages:
            age_dfs.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click the button to get the admissions data
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/ul/li[3]/a/label').click()
        searches += 1
        pages = 1
        wait()
        while pages <= number_of_pages:
            admission_dfs.append(pd.read_html(driver.page_source, header=0)[0])
            driver.find_element_by_id('DataTables_Table_' + str(searches) + '_next').click()
            pages += 1
            wait()
        # Click on the button for number of applicants
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/ul/li[1]/a/label').click()
        searches += 2
        # Click in the next page
    driver.quit()

scraper(25)

# Merge all the lists of dataframe to one df respectively
applicants_df = pd.concat(applicants_dfs)
gender_df = pd.concat(gender_dfs)
age_df = pd.concat(age_dfs)
admission_df = pd.concat(admission_dfs)

#Merge applicants, gender and age
cols_to_use = list(gender_df.columns.difference(applicants_df.columns))
cols_to_use.append('Anm.kod')
df = pd.merge(applicants_df, gender_df[cols_to_use], left_on='Anm.kod', right_on='Anm.kod')
cols_to_use = list(age_df.columns.difference(df.columns))
cols_to_use.append('Anm.kod')
df = pd.merge(df, age_df[cols_to_use], left_on='Anm.kod', right_on='Anm.kod')

# Create a new dataframe for the admissions data with the different admission groups as columns
# Extract the unique admission codes, i.e. codes for each program/course each semester
admission = pd.DataFrame((admission_df[['Anm.kod']].drop_duplicates()), columns=['Anm.kod'])

# Merge the previously created admission df with the admission stats for each admission code ("Anm.kod")
BI = admission_df[admission_df['Urvalsgrupp'] == 'BI']
BII = admission_df[admission_df['Urvalsgrupp'] == 'BII']
HP = admission_df[admission_df['Urvalsgrupp'] == 'HP']
selection_group = [BI, BII, HP]

for group in selection_group:
    admission = pd.merge(admission, group[['Anm.kod', 'Antagningspoäng']], on='Anm.kod')

admission.rename(columns={'Antagningspoäng_x': 'BI', 'Antagningspoäng_y': 'BII', 'Antagningspoäng':'HP'}, inplace=True)

cols_to_use = list(admission.columns.difference(df.columns))
cols_to_use.append('Anm.kod')
df = pd.merge(df, admission[cols_to_use], left_on='Anm.kod', right_on='Anm.kod')

df.to_csv('admission_data_SU.csv')
print(df.info())
print('------')
print('the script ran for ',time.time()-start_time,' seconds')

