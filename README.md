# Admission Grades
## Summary
In this project I built a web scraper in order to get the admission data of all swedish universities. This data was later used to build a model to predict upcomming admission grades. The model currently has an R^2 score of 0.6 and a MSE of 2.43. However, I am cirrently working on ways to improve it further.

![Distribution plot of actual vs fitted values](https://github.com/tlondahl/Admission_grades/blob/main/distplot_2.png)

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
- Datetime
- Scikit-learn 

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

## Version 4.0 - All the data you want to one csv
In version 4 I developed version 3 even further. Some of the changes I made was:
- Enabled the script to run through several pages without getting stuck
- Once all the data was collected the script compiled all the data into one dataframe which then was saved as a csv file.

### Results
I ran the code scraping 24 semesters back, i.e. 12 years of addmission data. The script worked and could easilly be adjusted to scrape any data, for any programs, from any University. The code can be found [here](https://github.com/tlondahl/Admission_grades/blob/main/scraper4.py) and the result looks as follows (since the column names are in Swedish I'll add a translation below) and can be found in this [csv file](https://github.com/tlondahl/Admission_grades/blob/main/admission_data.csv):

|    | Termin   | Program/kurs   | Utbildningens namn      | Anm.kod   | Univ/högskola              |   Totalt antal sökande |   1:a handssökande |   Kvinnor 1:a hand |   Kvinnor totalt |   Män 1:a hand |   Män totalt |   25-34 1:a hand |   25-34 totalt |   <= 24 1:a hand |   <= 24 totalt |   >=35 1:a hand |   >=35 totalt |    BI |    BII |     HP |
|---:|:---------|:---------------|:------------------------|:----------|:---------------------------|-----------------------:|-------------------:|-------------------:|-----------------:|---------------:|-------------:|-----------------:|---------------:|-----------------:|---------------:|----------------:|--------------:|------:|-------:|-------:|
|  0 | HT2020   | Program        | Fysisk planering        | BTH-87001 | Blekinge tekniska högskola |                    433 |                 98 |                 47 |              241 |             51 |          191 |               15 |             73 |               80 |            348 |               3 |            11 | 15.31 |  16.6  |   0.65 |
|  1 | HT2020   | Program        | Sjuksköterskeprogrammet | BTH-87005 | Blekinge tekniska högskola |                    668 |                147 |                111 |              507 |             34 |          156 |               53 |            203 |               59 |            374 |              33 |            86 | 14.1  | nan    | nan    |
|  2 | HT2019   | Program        | Fysisk planering        | BTH-86954 | Blekinge tekniska högskola |                    342 |                 92 |                 51 |              177 |             41 |          163 |               20 |             69 |               70 |            263 |               2 |             8 | 14.2  |  16.67 |   0.7  |
|  3 | HT2019   | Program        | Fysisk planering        | BTH-86954 | Blekinge tekniska högskola |                    342 |                 92 |                 51 |              177 |             41 |          163 |               20 |             69 |               70 |            263 |               2 |             8 | 14.2  |  16.67 |   0.7  |
|  4 | HT2019   | Program        | Fysisk planering        | BTH-86954 | Blekinge tekniska högskola |                    342 |                 92 |                 51 |              177 |             41 |          163 |               20 |             69 |               70 |            263 |               2 |             8 | 14.2  |  16.67 |   0.7  |

| Column Name | English translation/explanation |
|---:|:---------|
|Termin | Semester |
|Program/kurs | If it is a program och course |
|Utbildningens namn | The name of the program/course |
|Anm.kod | The admission code, i.e. the code for that program/course and semester |
|Univ/högskola | Univeristy/College |
|Totalt antal sökande | Total number of applicants |
|1:a handssökande | Number of applicants who had that course/program as their first choice |
|Kvinnor 1:a hand | Number of women who had it as their first choice |
|Kvinnor totalt | Number of women who applied in total |
|Män 1:a hand | Number of men who had it as their first choice |
|Män totalt | Number of men who applied in total |
|25-34 1:a hand | Number of people between the age of 25-34 who applied with this as their first choice |
|25-34 totalt | Number of people between the age of 25-34 who applied in total |
|<= 24 1:a hand | Number of people with an age lower than 24 who applied with this as their first choice |
|<= 24 totalt | Number of people with an age lower than 24 who applied in total |
|>=35 1:a hand' | Number of people with an age higher than 35 who applied with this as their first choice |
|>=35 totalt' | Number of people with an age higher than 35 who applied in total |
|BI | The lowest admitted high school grade (for people who had _**not**_ improved their grades since graduating high schools) |
|BII | The lowest admitted high school grade (for people who _**had**_ improved their grades since graduating high schools) |
|HP | The lowest score on the Swedish SAT (Högskoleprovet) that was admitted |


# Data Cleaning and EDA
To make the data more usable I had to do some cleaning. Some examples of what I did was:
- Creating a date column with the date of each row (i.e. which date that perticular grade was the lowest addmitted grade.
- Unified some of the program names making sure the same type of programs were called the same thing.
- Dopped duplicated and NaN values

when looking at the data there were some interdependent variables (as expected), for instance the number of applicant who ranked a program as number 1 and the total number of applicants. If one increased it is quite likely that the other increases as well. Out of those two it seemed that it was the total number of applicant who had the greates correlation with the target value

![Heatmap of the numeric variables](https://github.com/tlondahl/Admission_grades/blob/main/heatmap.png)

Furthermore when looking at the different variables there were no one with a super high correlation. The highest correlation were araound 0.55, for instance appl_tot.

## Model building and Evaluation
I used a Linear regression and with after some experiemtns I found that the most accurate model I could achive at this time was a model with the following features:
- 'appl_tot', 
- 'semester' 
- 'name', 
- 'Uni'
- 'days'

The highest score was 0.60 with an Mean Squared Error of 2.43, which is not very accurate. Hence, I will do some more feature enginnering and try to see if I can raise the scores of my model. As you can see below it tends to miss grades in the lower and higher end and instead predict a higher volume near the middle of the distribution curve.

![Distribution plot of actual vs fitted values](https://github.com/tlondahl/Admission_grades/blob/main/distplot_2.png)
