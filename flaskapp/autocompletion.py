from redis_completion import RedisEngine
import pandas as pd
import json
engine = RedisEngine(prefix='umls')


def loadumls():
    engine = RedisEngine(prefix='umls')
    data = pd.read_csv("../umls/umls7-08-11-2017@08-32h.csv")
    df = pd.DataFrame(data)
    df_dictarr = df.to_dict('records')
    for item in df_dictarr:
        # print item['value']
        # id, search phrase, data
        engine.store_json(item['value'], item['label'], {'label': item['label'], 'value': item['value']})

def search(p):
    return engine.search_json(p)