# Admission Grades
## Introduction
As a part of my learning experience I wanted to build a web scraper. A data scource i knew was quite frustrating to get full data from was the admissions for a certain university program in Sweden with data reaching several years back. To get this you previously had to go to click around at https://statistik.uhr.se/ to see the stats for differen semesters and could only see one semesters data at a time. Hence, I decided to build a web scraper who could do all the manual labor for me and neatly compile the data in a dataframe.

## Version 1.0 - One Program, One School
As a first step on my web scraping journey I decided to start small and scrape the data for one specific program at one specific University. I realized that there had been some development at "UHR" (the official authority of the admission stats in Sweden) since i last applied for school. You could now get a summary table of one program at one university with data up to 4 years old. Hence, I figured this was a good place to start.

### Results
The code can be found [here](https://github.com/tlondahl/Admission_grades/blob/main/scraper.py) and the output can be found [here](https://github.com/tlondahl/Admission_grades/blob/main/Stockholms%2Buniversitet_Juristprogrammet.csv).

The table at the webpage was of rather low quality. Hence, I had to do some cleaning before it was usable. But at least now I would easily get data from the past 4 years in notime.

![Graph of admission grades](https://github.com/tlondahl/Admission_grades/blob/main/Stockholms%2Buniversitet-Juristprogrammet.png)
