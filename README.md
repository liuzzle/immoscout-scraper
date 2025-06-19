# Immoscout-Scraper

This script scrapes the [immoscout24](https://www.immoscout24.ch/rent/4001994156) website:
- Choose a postal code of your choice, along with some other filters like radius (in km), number of rooms etc. and input the URL
- The script goes to every result item (apartment)'s page and scrape some info. (info about at least 15 apartments) This info can be information about facilities in the vicinity, if pets are allowed or not, etc.
- It uses a set of filters that return more than 50 results, by using pagination to navigate across them and collect information about all the individual apartments.
- Returns a conclusion at the end. Eg. In the neighbourhood of postal code 800X, X% of apartments are within 5 mins to a school. Whereas, in the postal code 800Y, only Y% of apartments are within 5 mins of a school.
