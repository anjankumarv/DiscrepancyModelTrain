import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

tasks = pd.read_csv('resources\enrtask_with_quotes_ISO-8859-1.LST', sep = '|', encoding = "ISO-8859-1", header=0, dtype=str)
print(len(tasks))

print(tasks.groupby(['MODEL_ID']).agg(['count']))

tasks_more_50 = tasks[tasks.groupby('ATA_LOOKUP')['MODEL_ID'].transform('count') >50]
print(tasks.shape)
print(tasks_more_50.shape)
train_tasks = tasks_more_50

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
vectorizer = TfidfVectorizer(**kwargs)
print(preprocessor('#6 SPOILER OUTB BONDING JUMPER LOOSE,INB BONDING JUMPER WORN,PLS TIGHT AND REPLACE'))

x_train =vectorizer.fit_transform(train_tasks.TASK_DESCRIPTION)
print("Vector transformed")
clf = LogisticRegression(random_state=0,  multi_class='ovr', n_jobs = -1).fit(x_train, train_tasks.ATA_LOOKUP.values)
print("Logistic model built.")

from sklearn.externals import joblib

joblib.dump(clf, 'output\\task_ata_classif_logis.pkl')
joblib.dump(vectorizer, 'output\\task_ata_vectorizer.pkl')

#joblib.dump(main_clf_1, 'subata_classif_linearsvc.pkl')
