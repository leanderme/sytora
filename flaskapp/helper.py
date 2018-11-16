import re
import json
from sklearn.naive_bayes import GaussianNB
import numpy as np
import pickle as pkl
from sklearn.externals import joblib
import pandas as pd
from decimal import Decimal
from werkzeug.utils import secure_filename
import logging
from flask import escape
from flask_expects_json import expects_json
import math
import operator
from more_itertools import unique_everseen
from uuid import uuid4

import os
import uuid
import requests
import sys
from umls.umls import UMLSLookup

all_csv = pd.read_csv('../disease-symptom-merged.csv', encoding='utf-8', index_col=None, header=0)

def dot_product2(v1, v2):
    return sum(map(operator.mul, v1, v2))


def vector_cos5(v1, v2):
    prod = dot_product2(v1, v2)
    len1 = math.sqrt(dot_product2(v1, v1))
    len2 = math.sqrt(dot_product2(v2, v2))
    return prod / (len1 * len2)

def isValid(cui):
  pattern = re.compile("C\\d{7}")
  if not pattern.match(cui):
    return False
  return True

def cuiToNumber(cui):
  return cui.strip("C").strip("0")

def convertCUI(cui):
  if not isValid(cui):
    return "C" + cui.zfill(7)
  else:
    return cui

def syInData():
    return all_csv['Symptom'].unique()

def isInDB(cui):
  return any(all_csv.Symptom == str(cui))

def get_model():
    model_file = '../data/all-files-for-ml/' + 'all_mnb' + '.pkl'
    mnb = joblib.load(open(model_file, 'rb'))
    data = pd.read_csv("../data/all-files-for-ml/all_x.csv")
    df = pd.DataFrame(data)
    cols = df.columns
    features = cols # = symptoms
    features_raw = [str(features[x]) for x in range(len(features))]
    # convert feature array into dict of symptom: index
    feature_dict = {}
    for i,f in enumerate(features):
        feature_dict[f] = i
    return mnb, features, feature_dict

def getRelatedSymptomsForDisease(cui):
    return all_csv.loc[all_csv['Disease'] == cui]["Symptom"].unique().tolist()

def findFeatures(cui, lang):
    symptom_strings = []
    look_umls = UMLSLookup()

    for s_cui in getRelatedSymptomsForDisease(cui):
        meaning_umls = look_umls.lookup_code_meaning(s_cui, lat=lang, preferred=False)
        if meaning_umls:
            symptom_strings.append(meaning_umls[0])
        else:
            symptom_strings.append(all_csv.loc[all_csv['Disease'] == cui]["Symptom"].unique()[0])
    return symptom_strings

    

def findSymptom(cui, lang):
    look_umls = UMLSLookup()
    meaning_umls = look_umls.lookup_code_meaning(cui, lat=lang, preferred=False)

    if meaning_umls:
        return str(meaning_umls[0])

    else:
        print("Using fallback CSV for: " + cui)
        return cui


def findDisease(cui, lang):
    look_umls = UMLSLookup()
    meaning_umls = look_umls.lookup_code_meaning(cui, lat=lang, preferred=False)

    if meaning_umls:
        return str(meaning_umls[0])
    else:
        #disease = str(all_csv.loc[all_csv['Disease'] == cui]["Disease_UMLS"].unique()[0].encode('utf8'))
        print("Using fallback CSV for: " + cui )
        return cui 