
import copy

import re
import unicodedata


from program_env.utilities.userDataUtils import (
    sanitize_text
)


# generate keyword cloud

# function call to get followers vs following amount
# Function call to get email
# Function call to filter for keywords in comments
# Function calls to filter for public users
# Function call to  filter for private users
# Function call to filter for verified users
# Function call to filter for business users
# Function call to filter for media count
# Function call to filter for keywords in biography 




#translate foreign texts to -e.g "#proudjorukagulaam\nदर्द स्वयं मृत्यु तक नहीं पहुंच सकता, लेकिन आपको मृत्यु तक ले जा सकता है।", to-> normal
def validateKeywordCloudDetails(keywordDetails_:dict)-> dict: # select keywords that we sould omit when keyword elections
    keywordDetails = copy.deepcopy(keywordDetails_)

    return {}

def captureDictKeyValues(dictionary_:dict, keys:str)-> list:
    dictionary = copy.deepcopy(dictionary_)
    data = []

    for key,values in dictionary.items():

         # sanitize text
        text = sanitize_text(values[keys])
        data.append(text)

    return data

def generateKeywordCloud(keywords_from_strings:list)->dict:  # create a dict cloud of keywords

    #ä 

    

    frame = {
        "username":{
            "bio":""
        }
    }


    #validateKeywordCloudDetails(keywordDetails_:dict)

    return {}

