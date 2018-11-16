import pandas as pd
import numpy as np
import re
import os
import glob

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib


result = pd.read_csv('./disease-symptom-db.csv', encoding='utf-8', index_col=None, header=0)

def isValid(cui):
    cui = str(cui)
    pattern = re.compile("C\\d{7}")
    if not pattern.match(cui):
        return False
    return True

def cuiToNumber(cui):
      return cui.strip("C").strip("0")

def convertCUI(cui):
    cui = str(cui)
    if not isValid(cui):
        return "C" + cui.zfill(7)
    else:
        return cui

def clean(the_string):
    return str(the_string.encode('utf-8'))

result['Disease'] = result['Disease'].apply(convertCUI)
result['Symptom'] = result['Symptom'].apply(convertCUI)

result.to_csv("./disease-symptom-db.csv",index=False)

df_foreign = pd.read_csv('./DiseaseSymptomKB.csv', encoding='utf-8', index_col=None, header=0)

result = result.append(df_foreign)

result.to_csv("./disease-symptom-merged.csv",index=False)

result['Disease'] = result['Disease'].astype(str)
result['Symptom'] = result['Symptom'].astype(str)

result['Symptom'].replace('', np.nan, inplace=True)
result.dropna(subset=['Symptom'], inplace=True)

result['Disease'].replace('', np.nan, inplace=True)
result.dropna(subset=['Disease'], inplace=True)

df = pd.DataFrame(result)
df.columns

df_1 = pd.get_dummies(df.Symptom)
df_s = df['Disease']
df_pivoted = pd.concat([df_s,df_1], axis=1)
df_pivoted.drop_duplicates(keep='first',inplace=True)

cols = df_pivoted.columns
cols = cols[1:] # skip 'Disease'

df_pivoted = df_pivoted.groupby('Disease').sum()
df_pivoted = df_pivoted.reset_index()


all_files_ml = "./data/all-files-for-ml"

df_pivoted.to_csv(os.path.join(all_files_ml, "all_pivoted.csv"), index=False)

cols = df_pivoted.columns
cols = cols[1:] # skip 'title'
x = df_pivoted[cols] # symptom rows
y = df_pivoted['Disease'] # diseases
x.to_csv(os.path.join(all_files_ml, "all_x.csv"), index=False)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

mnb = MultinomialNB()
mnb = mnb.fit(x_train, y_train)

mnb.score(x_test, y_test)


mnb_tot = MultinomialNB()
mnb_tot = mnb_tot.fit(x, y)

mnb_tot.score(x, y)

disease_pred = mnb_tot.predict(x)

disease_real = y.values


for i in range(0, len(disease_real)):
    if disease_pred[i]!=disease_real[i]:
        print ('Pred: {0} Actual:{1}'.format(disease_pred[i], disease_real[i]))


joblib.dump(mnb, os.path.join(all_files_ml, 'all_mnb.pkl'), protocol=2)

data = pd.read_csv(os.path.join(all_files_ml, "all_x.csv"))

df = pd.DataFrame(data)
cols = df.columns
features = cols # = symptoms
features_raw = [str(features[x]) for x in range(len(features))]
features_raw = ','.join(map(str, features_raw))


# convert feature array into dict of symptom: index
feature_dict = {}
for i,f in enumerate(features):
    feature_dict[f] = i

def findFeatures(disease):
    return result.loc[result['Disease'] == disease]["Symptom"].values.astype(str)

sample = np.zeros((len(features),), dtype=np.int)
sampe = sample.tolist()

search = ["C0857794", "C0149793", "C0000786"]
for i,s in enumerate(search):
    sample[feature_dict[s]] = 1

sample = np.array(sample).reshape(1,len(sample))

results = mnb.predict_proba(sample)[0]


# gets a dictionary of {'class_name': probability}
prob_per_class_dictionary = dict(zip(mnb.classes_, results))

# gets a list of ['most_probable_class', 'second_most_probable_class', ..., 'least_class']
results_ordered_by_probability = map(lambda x: {"disease": x[0],"prop": x[1] * 100, "sy": findFeatures(x[0])}, sorted(zip(mnb.classes_, results), key=lambda x: x[1], reverse=True))


print (list(results_ordered_by_probability))


#store the predicted probabilities for class 1
y_pred_prob = mnb.predict_proba(sample)[0]