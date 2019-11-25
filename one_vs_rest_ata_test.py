import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.externals import joblib

loaded_model = joblib.load('ata_classif_logis.pkl')
print(loaded_model.classes_)


discs = pd.read_csv('../sqk_test_desc.LST', sep = '|', encoding = "ISO-8859-1")
print(discs.head())
#discs_more_50 = discs[discs.groupby('ATA_LOOKUP')['MODEL_ID'].transform('count') >50]
#train_discs = discs_more_50

#subata_discs = discs[discs.groupby('SUBATA')['MODEL_ID'].transform('count') > 50]
#subata_discs['SUBATA_PRED'] = subata_discs['SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
#subata_discs = subata_discs[subata_discs['SUBATA_PRED'] != 0]

test_discs = discs

from processing import preprocessor

NGRAM_RANGE = (1, 2)
TOP_K = 20000
TOKEN_MODE = 'word'
MIN_DOCUMENT_FREQUENCY = 2

kwargs = {
        'ngram_range': NGRAM_RANGE,  # Use 1-grams + 2-grams.
        'dtype': 'int32',
        'strip_accents': 'unicode',
        'decode_error': 'replace',
        'sublinear_tf' :True, 
        'stop_words': 'english',
        'preprocessor': preprocessor, 
        'analyzer': TOKEN_MODE,  # Split text into word tokens.
        'min_df': MIN_DOCUMENT_FREQUENCY,
}

print(preprocessor('#6 SPOILER OUTB BONDING JUMPER LOOSE,INB BONDING JUMPER WORN,PLS TIGHT AND REPLACE'))
vectorizer = joblib.load('ata_vectorizer.pkl')

x_test = vectorizer.transform(test_discs.DESCRIPTION)

from sklearn.metrics import accuracy_score

#print(accuracy_score(test_discs.ATA_LOOKUP.values, loaded_model.predict(x_test)))
preds = loaded_model.predict_proba(x_test)
top_correct_vals = [0, 0, 0, 0, 0]
for i, val in enumerate(test_discs.ATA_LOOKUP.values):
        #check top 5
        argsorted = sorted(range(len(preds[i])), key=preds[i].__getitem__)
        argsorted.reverse()
        for j in range(len(top_correct_vals)):
                classes = loaded_model.classes_[argsorted[0 : (j+1)]]
                if val in classes:
                        top_correct_vals[j] += 1

print(top_correct_vals)        
print([a/len(preds) for a  in top_correct_vals])

