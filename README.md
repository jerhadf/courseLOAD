# layuplister

An interface for layuplist and short-term d-plan creation

## Installation

### Setting up virtual environment

* Run this to install pip: `easy_install pip`
* Run this to install virtualenv: `python3 -m pip install --user virtualenv`
* Just run this: `python3 -m virtualenv env` to create a virtual environment.
* To activate (On Windows): `.\env\Scripts\activate`
* On Mac OS: `source env/bin/activate`
* For more info follow this guide: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/
* Then run `pip install -r requirements.txt`

# Tools Used

* *Google Cloud Natural Language Processing API* : used to perform sentiment analysis of professor reviews

* *BeautifulSoup* : Python library to scrape the web

* *Python* : The most beautiful language on this planet. We know the Zen of Python by heart

##Description
* *courseLOAD began as a project attempting to solve a recurring issue nearly all Dartmouth students experience when planning out their course loads with respect to their D-PLAN. Course listings are disparate and one has to peruse through multiple departmental sites in order to see which courses are offered in which terms. courseLOAD planned to overcome this by scraping departmental sites and recommending sample D-PLANs depending on student specifications on major/minor as well as professor preferences etc. We also wanted to include a simplified professor rating system using Google Cloud Platform’s sentiment analysis API in tandem with LayupList to aggregate sentiment and magnitude score for each individual professor's reviews on LayupList.


However, our plans came to a halt when we realised that DALI Lab already had a project in the works dealing with our exact problem! Upon talking to the team, we decided that we would focus our work on the professor rating system using sentiment analysis. The team at DALI offered to collaborate with us after HackDartmouth and merge our functionalities.


## Challenges

* *Logging in to LayupList* : LayupList requires login credentials to access data. Required using   `mechanize` module to navigate through webforms on LayupList without logging in. Without access to API key, we had to c

* *Getting LayupList data* : Used `mechanize` libraries for Python, `urlliib`, and BeautifulSoup to extract data from site --> Clean and process data --> feed as text files into NLP model to analyze reviews sentiment and find score for professors.


* *Converting Plaintext Reviews to a Score* : Cleaned and processed extracted HTML data form LayupList to place every review for every professor into individual text files that can be passed through NLP model to generate sentiment and magnitude score. Wanted to aggregate an overall score for each professor which required running NLP model on each sentence and aggregating sentiment/magnitude values for each sentence into an overall sentiment and magntitude score for each professor. 

* *Integrating with DALI Lab D-Planner project* : DALI Lab members have designed interface for Dartmouth students to map out D-Plan for their terms. We recognized that we could pair our work into the backend of their application/web page to incorporate meaningful data quickly into site for student's use. 

* *Don't have access to LayupList API and ITC API that encapsulates all data* : In order to fully access all of the data to fully operationalize CourseLOAD, we needed access to the API keys for LayupList for review data and ITC API key to access course/professor data. This challenge meant we had to create a working protype of a sytem that will be able to generate scores for all professors once we have the necessary keys. Because we were not able to access those keys in a 24hr. period, we had to utilize web scraping libraries to pull as much data as we could from the sites. Once we have access to the API keys, we will be able to fully incorporate all of the necessary data into CourseLOAD.