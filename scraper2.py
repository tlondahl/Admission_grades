import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

path = '/Applications/chromedriver' #where i've saved the chrome driver locally
driver = webdriver.Chrome(path)

driver.get('https://statistik.uhr.se/')

# Type in what you want to search for in the search field
search = driver.find_element_by_id('Search')
search.send_keys('Jur')

# Select witch semester
semester = Select(driver.find_element_by_id('AdmissionRoundId'))
semester.select_by_visible_text('VT2020')

# Select the School
school = Select(driver.find_element_by_id('EducationOrgId'))
school.select_by_value('SU ')

# Select if you want to look at only programs, courses or both
prog = Select(driver.find_element_by_id('ProgKurs'))
prog.select_by_value('p')

# Click on the search button
driver.find_element_by_id('search-button').click()

# Wait until the table emerges and then create a dataframe from it
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    df = pd.read_html(driver.page_source)[0]
    print(df.to_markdown())
finally:
    driver.quit()


