import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

discs = pd.read_csv(r'data\squawks_all_with_date.LST', header = 0, sep = '|', encoding = "ISO-8859-1", error_bad_lines=False, dtype=str)
discs = discs.fillna('')

print(len(discs))
discs['ATA_PRED'] = discs['ATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
discs = discs[discs['ATA_PRED'] != 0]

from processing import preprocessor

NGRAM_RANGE = (1, 2)
TOP_K = 20000
TOKEN_MODE = 'word'
MIN_DOCUMENT_FREQUENCY = 1

kwargs = {
        'ngram_range': NGRAM_RANGE,  # Use 1-grams + 2-grams.
        # 'dtype': 'int32',
        'strip_accents': 'unicode',
        'decode_error': 'replace',
        'sublinear_tf' :True, 
        'stop_words': 'english',
        'preprocessor': preprocessor, 
        'analyzer': TOKEN_MODE,  # Split text into word tokens.
        'min_df': MIN_DOCUMENT_FREQUENCY,
}
subata_vectorizer = TfidfVectorizer(**kwargs)

subata_discs = discs[discs.groupby('ATA_SUBATA')['MODEL_ID'].transform('count') >10]
subata_discs['ATA_SUBATA_PRED'] = subata_discs['ATA_SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
subata_discs = subata_discs[subata_discs['ATA_SUBATA_PRED'] != 0]
subata_x_train = subata_vectorizer.fit_transform(subata_discs.SQK_DESC)

clf_logis = LogisticRegression(random_state=0,  multi_class='ovr', n_jobs = -1).fit(subata_x_train, subata_discs.ATA_SUBATA_PRED.values)

joblib.dump(clf_logis, 'subata_classif_logis_2022_10_14.pkl')
joblib.dump(subata_vectorizer, 'subata_vectorizer_logis_2022_10_14.pkl')

subata_discs['PREDICTED_SUBATA'] = clf_logis.predict(subata_x_train)
subata_discs.to_excel('subata_pred_logis.xlsx')


