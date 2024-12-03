import json
import numpy
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tfidf = TfidfVectorizer(analyzer='word')


# method that initializes various variables depending on the training data
def initialize():
    # assign data from intents.json file to variable
    with open("intents.json", "r") as file:
        data = json.load(file)

    pattern_list = []   # list of patterns
    pattern_tags = {}   # dictionary of patterns as keys and their tags as value

    for intent in data['intents']:
        for pattern in intent['patterns']:
            pattern_list.append(pattern)
            pattern_tags[pattern] = intent['tag']

    # vectors of all the patterns
    patterns_tfidf = tfidf.fit_transform(pattern_list).toarray()
    # dataframe of all pattern vectors
    patterns_df = pandas.DataFrame(patterns_tfidf, columns=tfidf.get_feature_names_out())

    return pattern_list, patterns_df, pattern_tags, data


# used for getting the correct intent based on user input
def intent_match(inp, pattern_list, patterns_df, pattern_tags, confidence_threshold):
    inp_tfidf = tfidf.transform([inp.lower()]).toarray()        # convert user input to vector

    result = cosine_similarity(patterns_df, inp_tfidf)          # get the similarity for all patterns based on input

    # check confidence level of the top similar match
    if result.max() >= confidence_threshold:
        id_argmax = numpy.argmax(result)
        predicted_tag = pattern_tags[pattern_list[id_argmax]]   # Get the tag directly using the dictionary
        return predicted_tag
    else:
        return "error"
