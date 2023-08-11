# Glassdoor-Scraping

## Basic-Scraper-project
  This jupyter notebook contains simple scraping of job data from glassdoor using scraperApi proxies and beautifulSoup.
  The data extracted contains a list of dictionary with keys {'title', 'company', 'location'}

## Selenium_scraping
  This python file contains the code to extract the same job data automatically from glassdoor website using selenium.
  The user login details and search are automated. 
  User input is required for job title and location, which is inputed into the website using selenium and the resulting url is then parsed using the code from basic scraper
