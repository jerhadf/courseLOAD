import argparse #allow application to accept input filenames as args
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types #classes required for creating requests
import os 

review_list = [
    "I personally am not that interested by the topic, but it seemed like other people were. I think the Prof is great and really enthusiastic and good at making us see connections. The readings were diverse, although often too long considering other classes. The class covered a wide variety of topics. I recommend it.",
    "The 10A got a little long every day, but Cook gave us a break, and kept class interesting. Very knowledgeable teacher. His ideas on what Christianity and the Bible say are sometimes a a little off-base, but rarely in critical matters",
    "So I took this course for the distribs-CI and LIT. Although I really don't like English classes, this wasn't all that bad. See Cook is a great prof. He just goes off talking about stuff during class and seems to know everything about literature. If you can, take a class with him."
]


sentiment_list = [] # list of 3 floating point numbers, each one a sentiment score

def analyze(prof_review_file):
    """run sentiment analysis on text within passed filename"""
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

# parse the passed argument for the text filename and pass it to the analyze() function
if __name__  == '__main__':
    import os

    directory = os.fsencode("prof_reviews")

    filenames = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filenames.append(filename)
    print(filenames)
    
    # sentiment = analyze("prof_reviews/Sample.txt")
    # score = sentiment.document_sentiment.score
    # magnitude = sentiment.document_sentiment.magnitude
    # print(f"SCORE: {score} MAGNITUDE: {magnitude}")

    # parser = argparse.ArgumentParser(
    #     description = __doc__,
    #     formatter_class = argparse.RawDescriptionHelpFormatter)
    # parser.add_argument(
    #     'prof_review_file',
    #     help = 'File of prof refiew that we want to analyze')
    # args = parser.parse_args()

    # analyze(args.prof_review_file)

# run: /Users/johnmcdonald/Desktop/layuplister/env/bin/python /Users/johnmcdonald/Desktop/layuplister/NLP/nlp.py