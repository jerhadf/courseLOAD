import argparse #allow application to accept input filenames as args
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types #classes required for creating requests
import os 
import fileinput
import re
import sys

review_list = [
    "I personally am not that interested by the topic, but it seemed like other people were. I think the Prof is great and really enthusiastic and good at making us see connections. The readings were diverse, although often too long considering other classes. The class covered a wide variety of topics. I recommend it.",
    "The 10A got a little long every day, but Cook gave us a break, and kept class interesting. Very knowledgeable teacher. His ideas on what Christianity and the Bible say are sometimes a a little off-base, but rarely in critical matters",
    "So I took this course for the distribs-CI and LIT. Although I really don't like English classes, this wasn't all that bad. See Cook is a great prof. He just goes off talking about stuff during class and seems to know everything about literature. If you can, take a class with him."
]

sentiment_list = [] # list of 3 floating point numbers, each one a sentiment score

def analyze(prof_review_file):
    """
    Run sentiment analysis on text within passed filename
    """
    client = language.LanguageServiceClient()
    
    with open(prof_review_file, 'r') as review_file:
        """instantiate plain txt doc"""
        content = review_file.read() #reads filename containing text data into variable
    #instantiate Document object w/ contents of file
    document = types.Document(
        content = content, 
        type = enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    return annotations
    print_result(annotations)

def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
    return 0

prof_sentiments = {} # keeps track of professor sentiments 
    
def get_prof_reviews():
    """
    Gets a list of all the filenames in the prof_reviews folder
    """
    directory = os.fsencode("prof_reviews")
    filenames = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filenames.append(filename)
    return filenames

def get_sentiments(): 
    """
    Get the sentiment scores and magnitudes for each professor reviews file and then 
    save the results to a dictionary 
    @prof_name - string, the last name of the professor
    """
    for filename in get_prof_reviews(): 
        # get the professor name
        prof_name = filename.replace(".txt", "")
        
        # analyze sentiment 
        sentiment = analyze(f"prof_reviews/{filename}")
        score = sentiment.document_sentiment.score
        magnitude = sentiment.document_sentiment.magnitude

        # save results to dictionary
        print(f"PROF NAME: {prof_name}\nSCORE: {score} MAGNITUDE: {magnitude}")
        prof_sentiments[prof_name] = {
            "score" : score, 
            "magnitude" : magnitude
        }

        return prof_sentiments

def get_prof_score(prof_name): 
    """
    Get the sentiment scores and magnitudes for each professor reviews file and then 
    save the results to a dictionary 
    @prof_name - string, the last name of the professor
    """

    filename_list = get_prof_reviews() 
    prof_file = f"{prof_name}.txt"

    print(f"IS {prof_file} in {filename_list}??")
    if prof_file in filename_list: 
        print(f".... YES: {prof_file} is in file list ...")
    else:
        print(f"... YES: {prof_file} is not in file list ...")
        return False 
    prof_index = filename_list.index(prof_file)
    
    # analyze sentiment 
    sentiment = analyze(f"prof_reviews/{prof_file}")
    score = sentiment.document_sentiment.score
    magnitude = sentiment.document_sentiment.magnitude

    # save results to dictionary
    print(f"\n**** RESULTS FOUND FOR PROF. {prof_name} ****\n")
    print(f"SENTIMENT SCORE: {score}\nSENTIMENT MAGNITUDE: {magnitude}")
    prof_sentiments[prof_name] = {
        "score" : score, 
        "magnitude" : magnitude
    }

    return prof_sentiments

# parse the passed argument for the text filename and pass it to the analyze() function
if __name__  == '__main__':
    if len(sys.argv) <= 1: 
        print("\nERROR: Need to enter one more command line argument - professor last name\n")
    elif len(sys.argv) > 2: 
        print("\nERROR: Too many command line arguments, should only be one - professor last name\n")
    else: 
        prof_name = sys.argv[1]
    
    prof_sentiment = get_prof_score(prof_name)
    print(prof_sentiment)
    
    # parser = argparse.ArgumentParser(
    #     description = __doc__,
    #     formatter_class = argparse.RawDescriptionHelpFormatter)
    # parser.add_argument(
    #     'prof_review_file',
    #     help = 'File of prof refiew that we want to analyze')
    # args = parser.parse_args()

    # analyze(args.prof_review_file)

# run: /Users/johnmcdonald/Desktop/layuplister/env/bin/python /Users/johnmcdonald/Desktop/layuplister/NLP/nlp.py