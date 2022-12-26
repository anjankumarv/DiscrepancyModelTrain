import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib


# vectorizer = joblib.load(r'decisiontree_depth_500\vectorizer_decisiontree_depth_500.pkl')
# clf = joblib.load(r'decisiontree_depth_500\subata_pred_decisiontree_depth_500.pkl')
vectorizer = joblib.load(r'vectorizer_decisiontree_depth_200.pkl')
clf = joblib.load(r'subata_pred_decisiontree_depth_200.pkl')
print(clf.predict(vectorizer.transform(['ENGINE OIL INSPECTION AND SERVICING'])))

discs = pd.read_csv(r'data\squawks_all_with_date.LST', header = 0, sep = '|', encoding = "ISO-8859-1", error_bad_lines=False, dtype=str)
discs = discs.fillna('')
discs['ATA_SUBATA_PRED'] = discs['ATA_SUBATA'].apply(lambda x: int(re.sub('[^0-9]', '', str(x))) if pd.isna(x) == False and re.sub('[^0-9]', '', str(x)) != '' else 0)

print(1)
subata_x_test =vectorizer.transform(discs.SQK_DESC)
print(2)
preds = clf.predict_proba(subata_x_test)
print(3)
# ata_with_prob  = clf.predict_proba(vectorizer.transform(['UPDATE FMS DATABASE']))
pred_vals = []
pred_confs = []
for i, val in enumerate(preds):
    pred_conf = preds[i].max()
    pred_val_idx = list(preds[i]).index(pred_conf)
    pred_val = clf.classes_[pred_val_idx]
    pred_confs.append(pred_conf)
    pred_vals.append(pred_val)

discs['PREDICTED_SUBATA'] = pred_vals
discs['PREDICTED_CONF'] = pred_confs
discs.to_excel('res_dt_depth_200.xlsx')


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