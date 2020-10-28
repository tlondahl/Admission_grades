# Admission Grades
## Introduction
As a part of my learning experience I wanted to build a web scraper. A data scource i knew was quite frustrating to get full data from was the admissions for a certain university program in Sweden with data reaching several years back. To get this you previously had to go to click around at https://statistik.uhr.se/ to see the stats for differen semesters and could only see one semesters data at a time. Hence, I decided to build a web scraper who could do all the manual labor for me and neatly compile the data in a dataframe.

### Data and packages
The data have been collected from https://statistik.uhr.se/.
The python packages that have been used are the following:
- Pandas
- Selenium
- BeautifulSoup
- Matplotlib
- Seaborn

## Version 1.0 - One Program, One School
As a first step on my web scraping journey I decided to start small and scrape the data for one specific program at one specific University. I realized that there had been some development at "UHR" (the official authority of the admission stats in Sweden) since i last applied for school. You could now get a summary table of one program at one university with data up to 4 years old. Hence, I figured this was a good place to start.

### Results
The code can be found [here](https://github.com/tlondahl/Admission_grades/blob/main/scraper.py) and the output can be found [here](https://github.com/tlondahl/Admission_grades/blob/main/Stockholms%2Buniversitet_Juristprogrammet.csv).

The table at the webpage was of rather low quality. Hence, I had to do some cleaning before it was usable. But at least now I would easily get data from the past 4 years in notime.

![Graph of admission grades](https://github.com/tlondahl/Admission_grades/blob/main/Stockholms%2Buniversitet-Juristprogrammet.png)

## Version 2.0 - Selecting what too look for
To get more data then what was possible in version 1.0 I had to scrape another [web page](https://statistik.uhr.se/), a page where you had to make selections form dropdown lists and/or searchfields. Hence, I needed to look for another solution which could interact with the various filters first before I could scrape the data. I decided to work with Selanium and wrote a program who did the following:
- In the searchfield typed "Jur"
- Selected the spring semester och 2020 (VT2020)
- Selected to only look at Stockholm University
- Selected to only look at programs
- Clicked the search button
- And finally scraped the data to a dataframe

### Results
The code can be found [here](https://github.com/tlondahl/Admission_grades/blob/main/scraper2.py) and the Dataframe looked like this:

|    | Termin   | Program/kurs   | Utbildningens namn   | Anm.kod   | Univ/högskola          |   Totalt antal sökande |   1:a handssökande |
|---:|:---------|:---------------|:---------------------|:----------|:-----------------------|-----------------------:|-------------------:|
|  0 | VT2020   | Program        | Juristprogrammet     | SU-29293  | Stockholms universitet |                   4283 |               1580 |

## Version 3.0 - Multiple Semesters
Version 3 was built upon version 2 but instead of having hard-coded variables for the drop down menues and other variables I made the following altercations:
- Once the data was collected from the table with the number of applicants the program clicked the "Urval 2" button to gat the admissions data.
- Once the admissions data was collected the program changed the semester and iterated through these steps until the desired number of semesters was met

### Results
The code can be found [here](https://github.com/tlondahl/Admission_grades/blob/main/scraper3.py) and the first 5 rows of the dataframe generated looks like this:
|    | term   | name             | university             |   applicants |    BI |   BII |
|---:|:-------|:-----------------|:-----------------------|-------------:|------:|------:|
|  0 | HT2020 | Juristprogrammet | Stockholms universitet |         7204 | 20.89 | 20.8  |
|  1 | HT2019 | Juristprogrammet | Stockholms universitet |         5946 | 20.5  | 20.4  |
|  2 | HT2018 | Juristprogrammet | Stockholms universitet |         7109 | 20.7  | 20.73 |
|  3 | HT2017 | Juristprogrammet | Stockholms universitet |         7226 | 20.57 | 20.36 |
|  4 | HT2016 | Juristprogrammet | Stockholms universitet |         7270 | 20.68 | 20.63 |
