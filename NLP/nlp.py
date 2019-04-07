import argparse #allow application to accept input filenames as args
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types #classes required for creating requests

# parse the passed argument for the text filename and pass it to the analyze() function
if __name__  == '__main__':
    parser = argparse.ArgumentParser(
        description = __doc__,
        formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'prof_review_file',
        help = 'File of prof refiew that we want to analyze')
    args = parser.parse_args()

    analyze(args.prof_review_file)

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

    print_result(annotations)

def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentimen.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
    return 0

# run: /Users/johnmcdonald/Desktop/layuplister/env/bin/python /Users/johnmcdonald/Desktop/layuplister/NLP/nlp.py