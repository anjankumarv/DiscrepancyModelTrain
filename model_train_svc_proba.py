import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from appconfig import random_state
discs = pd.read_csv(r'resources\squawks_all_distinct.LST', header = 0, sep = '|', encoding = "ISO-8859-1", error_bad_lines=False, dtype=str)
discs = discs.fillna('')

discs['ATA_PRED'] = discs['ATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
discs['SUBATA_PRED'] = discs['SUB_ATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)

discs = discs[discs['ATA_PRED'] != 0]
print('ata filtered', len(discs))
# discs = discs[discs['SUBATA_PRED'] != 0]
# print('subata also filtered', len(discs))

# discs = discs[["SQK_DESC", "ATA", "SUB_ATA", "ATA_SUBATA"]]
# discs = discs.drop_duplicates()
# discs = discs[0:1000]
# print(len(discs))
# discs['ATA_PRED'] = discs['ATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
# discs = discs[discs['ATA_PRED'] != 0]

# discs_more_50 = discs[discs.groupby('ATA_PRED')['MODEL_ID'].transform('count') > 50]
# train_discs = discs_more_50
# discs = discs[["SQK_DESC", "ATA", "SUB_ATA", "ATA_SUBATA"]]
# discs = discs.drop_duplicates()

from preprocessing_new import preprocessor

NGRAM_RANGE = (1,2)
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
vectorizer = TfidfVectorizer(**kwargs)
# print(preprocessor('#6 SPOILER OUTB BONDING JUMPER LOOSE,INB BONDING JUMPER WORN,PLS TIGHT AND REPLACE'))

# x_train =vectorizer.fit_transform(train_discs.SQK_DESC)

from sklearn.svm import LinearSVC, SVC

subata_discs = discs[discs.groupby('ATA_SUBATA')['MODEL_ID'].transform('count') > 10]
subata_discs['ATA_SUBATA_PRED'] = subata_discs['ATA_SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
subata_discs = subata_discs[subata_discs['ATA_SUBATA_PRED'] != 0]
subata_discs = subata_discs[["SQK_DESC", "ATA_SUBATA_PRED"]]
subata_discs = subata_discs.drop_duplicates()
print('subata discs final', len(subata_discs))

subata_x_train = vectorizer.fit_transform(subata_discs.SQK_DESC)

svm1 = LinearSVC(random_state=random_state, tol=1e-5, C = 0.5)
main_clf_1 = CalibratedClassifierCV(svm1) 
#main_clf = SVC(kernel = 'linear', random_state=0, tol=1e-5, C = 0.5, probability = False)
main_clf_1.fit(subata_x_train, subata_discs.ATA_SUBATA_PRED.values)


from sklearn.externals import joblib

# discs_more_50['PREDICTED_ATA'] = main_clf.predict(x_train)
# discs_more_50.to_excel('ata_pred_discs_proba_2.xlsx')

subata_discs['PREDICTED_SUBATA'] = main_clf_1.predict(subata_x_train)
subata_discs.to_excel('subata_res_20221222.xlsx')


# joblib.dump(main_clf, 'ata_classif_linearsvc_proba_20221222.pkl')
joblib.dump(main_clf_1, 'subata_classif_linearsvc_proa_20221222.pkl')
joblib.dump(vectorizer, 'vectorizer_proba_20221222.pkl')
