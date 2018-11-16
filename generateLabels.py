import sqlite3
import csv, codecs, cStringIO
import pandas as pd

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f", 
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

conn = sqlite3.connect('./flaskapp/databases/umls.db')
c = conn.cursor()
c.execute('select * from descriptions')

writer = UnicodeWriter(open("./data/descriptions.csv", "wb"))
writer.writerows(c)

umlsDF = pd.read_csv('./data/descriptions.csv', encoding='utf-8', index_col=None, header=0)
umlsDF.columns = ['CUI', 'LAT', 'SAB', 'TTY', 'STR', 'STY']

result = pd.read_csv('./disease-symptom-cuis.csv', encoding='utf-8', index_col=None, header=0)

def findConcept(cui, lat):
    results = umlsDF.loc[(umlsDF['CUI']==cui) & (umlsDF['LAT']==lat)]["STR"].unique()
    
    if len(results) >= 1:
        return results[0]
    else:
        return cui

import io, json

labelsDir = "./flaskapp/app/frontend/data/"
languages = ["GER", "ENG"]
convertIso = {"GER": "de", "ENG": "en"}
sy_cuis = result["Symptom"].unique()

for lat in languages:
    currentLatOut = []
    
    for sy in sy_cuis:
        currentLatOut.append({"label": findConcept(sy, lat), "value": sy})
        
    with io.open(labelsDir + convertIso[lat] + '_Labels.js', 'w', encoding='utf-8') as f:
        f.write("exports." + convertIso[lat] + "LABELS = " + json.dumps(currentLatOut, ensure_ascii=False) + ";")