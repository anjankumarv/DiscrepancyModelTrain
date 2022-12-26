import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

discs = pd.read_csv(r'data\squawks_all_with_date.LST', header = 0, sep = '|', encoding = "ISO-8859-1", error_bad_lines=False, dtype=str)
discs = discs.fillna('')
print(len(discs))
discs = discs[["SQK_DESC", "ATA", "SUB_ATA", "ATA_SUBATA"]]
discs = discs.drop_duplicates()
print(len(discs))
# discs['ATA_PRED'] = discs['ATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
# discs = discs[discs['ATA_PRED'] != 0]

# discs_more_50 = discs[discs.groupby('ATA_PRED')['MODEL_ID'].transform('count') > 50]
# train_discs = discs_more_50


# from preprocessing_new import preprocessor
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
vectorizer = TfidfVectorizer(**kwargs)
# print(preprocessor('#6 SPOILER OUTB BONDING JUMPER LOOSE,INB BONDING JUMPER WORN,PLS TIGHT AND REPLACE'))

# x_train =vectorizer.fit_transform(train_discs.SQK_DESC)
# print('trainset ready')
# joblib.dump(x_train, 'trainset_preprocessing_new_1.pkl')
# clf = DecisionTreeClassifier(random_state=10)
# clf.fit(x_train, train_discs.ATA_PRED.values)

# train_discs['PREDICTED_ATA_DT'] = clf.predict(x_train)
# train_discs.to_excel('ata_pred_decisiontree_20221220_1.xlsx')
# joblib.dump(clf, 'ata_pred_decisiontree_20221220_1.pkl')
# joblib.dump(vectorizer, 'vectorizer_decisiontree_20221220_1.pkl')

########subata############
subata_discs = discs[discs.groupby('ATA_SUBATA')['ATA'].transform('count') >10]
subata_discs['ATA_SUBATA_PRED'] = subata_discs['ATA_SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
subata_discs = subata_discs[subata_discs['ATA_SUBATA_PRED'] != 0]
print(len(subata_discs))
subata_discs = subata_discs[["SQK_DESC", "ATA_SUBATA_PRED"]]
subata_discs = subata_discs.drop_duplicates()
print(1)
print(len(subata_discs))
# subata_x_train = vectorizer.transform(subata_discs.SQK_DESC)
subata_x_train =vectorizer.fit_transform(subata_discs.SQK_DESC)



# vectorizer = joblib.load('vectorizer_fixed.pkl')
# subata_x_train = joblib.load('subata_x_train_fixed.pkl')
print(2.0)
clf1 = DecisionTreeClassifier(random_state=10, max_depth=200)
clf1.fit(subata_x_train, subata_discs.ATA_SUBATA_PRED.values)
print(2)

print(3)
subata_discs['PREDICTED_SUBATA'] = clf1.predict(subata_x_train)
print(4)
subata_discs.to_excel('subata_pred_decisiontree_depth_200.xlsx')

joblib.dump(subata_x_train, 'subata_x_train_fixed_depth_200.pkl')
joblib.dump(clf1, 'subata_pred_decisiontree_depth_200.pkl')
joblib.dump(vectorizer, 'vectorizer_decisiontree_depth_200.pkl')

# from sklearn.svm import LinearSVC, SVC

# main_clf = LogisticRegression(random_state=10,  multi_class='ovr', n_jobs = -1)#.fit(x_train, train_discs.SUBATA_PRED.values)
# #main_clf = SVC(kernel = 'linear', random_state=0, tol=1e-5, C = 0.5, probability = False)
# main_clf.fit(x_train, train_discs.ATA_PRED.values)

# print(main_clf.predict(vectorizer.transform(['ENGINE OIL INSPECTION AND SERVICING'])))

# subata_discs = discs[discs.groupby('ATA_SUBATA')['MODEL_ID'].transform('count') >10]
# subata_discs['ATA_SUBATA_PRED'] = subata_discs['ATA_SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)
# subata_discs = subata_discs[subata_discs['ATA_SUBATA_PRED'] != 0]

# discs_more_50['PREDICTED_ATA'] = main_clf.predict(x_train)
# discs_more_50.to_excel('ata_pred_discs_logis_proba_20221220.xlsx')

# joblib.dump(vectorizer, 'vectorizer_logis_proba_20221220.pkl')
# joblib.dump(main_clf, 'ata_classif_logis_proba_20221220.pkl')

# print('subata discs', len(subata_discs))

# subata_x_train = vectorizer.transform(subata_discs.SQK_DESC)

# main_clf_1 = LogisticRegression(random_state=10,  multi_class='ovr', n_jobs = -1)#.fit(x_train, train_discs.SUBATA_PRED.values)
# #main_clf = SVC(kernel = 'linear', random_state=0, tol=1e-5, C = 0.5, probability = False)
# main_clf_1.fit(subata_x_train, subata_discs.ATA_SUBATA_PRED.values)


# from sklearn.externals import joblib


# joblib.dump(main_clf_1, 'subata_classif_logis_proba_20221220.pkl')

# subata_discs['PREDICTED_SUBATA'] = main_clf_1.predict(subata_x_train)
# subata_discs.to_excel('subata_pred_discs_logis_proba_20221220.xlsx')