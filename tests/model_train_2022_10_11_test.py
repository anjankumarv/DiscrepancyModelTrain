import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer

discs = pd.read_csv(r'data\squawks_all_with_date.LST', header = 0, sep = '|', encoding = "ISO-8859-1", error_bad_lines=False, dtype=str)
discs = discs.fillna('')

print(len(discs))
discs['ATA_PRED'] = discs['ATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
discs = discs[discs['ATA_PRED'] == 0]
print(len(discs))
# discs_more_50 = discs[discs.groupby('ATA_PRED')['MODEL_ID'].transform('count') > 50]
# train_discs = discs_more_50

# from processing import preprocessor

# NGRAM_RANGE = (1, 2)
# TOP_K = 20000
# TOKEN_MODE = 'word'
# MIN_DOCUMENT_FREQUENCY = 2

# kwargs = {
#         'ngram_range': NGRAM_RANGE,  # Use 1-grams + 2-grams.
#         # 'dtype': 'int32',
#         'strip_accents': 'unicode',
#         'decode_error': 'replace',
#         'sublinear_tf' :True, 
#         'stop_words': 'english',
#         'preprocessor': preprocessor, 
#         'analyzer': TOKEN_MODE,  # Split text into word tokens.
#         'min_df': MIN_DOCUMENT_FREQUENCY,
# }
# vectorizer = TfidfVectorizer(**kwargs)
# print(preprocessor('#6 SPOILER OUTB BONDING JUMPER LOOSE,INB BONDING JUMPER WORN,PLS TIGHT AND REPLACE'))

# x_train =vectorizer.fit_transform(train_discs.SQK_DESC)

# from sklearn.svm import LinearSVC, SVC

# main_clf = LinearSVC(random_state=0, tol=1e-5, C = 0.5)
# #main_clf = SVC(kernel = 'linear', random_state=0, tol=1e-5, C = 0.5, probability = False)
# main_clf.fit(x_train, train_discs.ATA_PRED.values)

# print(main_clf.predict(vectorizer.transform(['ENGINE OIL INSPECTION AND SERVICING'])))  

subata_discs = discs#[discs.groupby('ATA_SUBATA')['MODEL_ID'].transform('count') <= 10]
subata_discs['ATA_SUBATA_PRED'] = subata_discs['ATA_SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
# subata_discs = subata_discs[subata_discs['ATA_SUBATA_PRED'] != 0]
# print(len(subata_discs))

from sklearn.externals import joblib

# vectorizer = joblib.dump(main_clf, 'ata_classif_linearsvc_2022_10_11.pkl')
main_clf_1 = joblib.load('subata_classif_linearsvc_2022_10_11.pkl')
vectorizer = joblib.load('vectorizer_2022_10_11.pkl')
X = vectorizer.transform(subata_discs.SQK_DESC)


subata_discs['PREDICTED_SUBATA'] = main_clf_1.predict(X)
subata_discs.to_excel('subata_pred_with_ata_0.xlsx')