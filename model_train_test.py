import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer

discs = pd.read_csv('../all_sqk_desc_model_all.LST', header = None, sep = '|', encoding = "ISO-8859-1", names = ['SUBATA', 'SQUAWK_DESCRIPTION', 'MODEL_ID', 'ATA_LOOKUP', 'SUBATA_LOOKUP'])
print(len(discs))
discs_more_50 = discs[discs.groupby('ATA_LOOKUP')['MODEL_ID'].transform('count') >50]
train_discs = discs_more_50[0:1000]

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

x_train =vectorizer.fit_transform(train_discs.SQUAWK_DESCRIPTION)
print(x_train.shape)
