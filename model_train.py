import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer

discs = pd.read_csv(r'resources\model\2019\all_sqk_desc_model_all.LST', header = None, sep = '|', encoding = "ISO-8859-1", names = ['SUBATA', 'SQUAWK_DESCRIPTION', 'MODEL_ID', 'ATA_LOOKUP', 'SUBATA_LOOKUP'])
print(len(discs))
discs_more_50 = discs[discs.groupby('ATA_LOOKUP')['MODEL_ID'].transform('count') >50]
train_discs = discs_more_50

from processing import preprocessor

NGRAM_RANGE = (1, 2)
TOP_K = 20000
TOKEN_MODE = 'word'
MIN_DOCUMENT_FREQUENCY = 2

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
vectorizer = TfidfVectorizer(**kwargs)
print(preprocessor('#6 SPOILER OUTB BONDING JUMPER LOOSE,INB BONDING JUMPER WORN,PLS TIGHT AND REPLACE'))

x_train =vectorizer.fit_transform(train_discs.SQUAWK_DESCRIPTION)

from sklearn.svm import LinearSVC, SVC

main_clf = LinearSVC(random_state=0, tol=1e-5, C = 0.5)
#main_clf = SVC(kernel = 'linear', random_state=0, tol=1e-5, C = 0.5, probability = False)
main_clf.fit(x_train, train_discs.ATA_LOOKUP.values)

print(main_clf.predict(vectorizer.transform(['ENGINE OIL INSPECTION AND SERVICING'])))  

subata_discs = discs[discs.groupby('SUBATA')['MODEL_ID'].transform('count') >10]
subata_discs['SUBATA_PRED'] = subata_discs['SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
subata_discs = subata_discs[subata_discs['SUBATA_PRED'] != 0]

print('subata discs', len(subata_discs))

subata_x_train = vectorizer.transform(subata_discs.SQUAWK_DESCRIPTION)

main_clf_1 = LinearSVC(random_state=0, tol=1e-5, C = 0.5)
#main_clf = SVC(kernel = 'linear', random_state=0, tol=1e-5, C = 0.5, probability = False)
main_clf_1.fit(subata_x_train, subata_discs.SUBATA_PRED.values)


from sklearn.externals import joblib

joblib.dump(main_clf, 'ata_classif_linearsvc.pkl')
joblib.dump(main_clf_1, 'subata_classif_linearsvc.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
