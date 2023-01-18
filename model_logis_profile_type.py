import pandas as pd
import numpy as np
import re
from appconfig import *
from sklearn.externals import joblib
from preprocessing_new import preprocessor


discs = pd.read_csv(r'queries\squawks.LST', header = 0, sep = '|', encoding = "ISO-8859-1", error_bad_lines=False, dtype=str)
discs = discs.fillna('')
discs = discs.drop_duplicates()
print('total squawks', len(discs))

vectorizer = joblib.load(vectorizer_path)

from sklearn.linear_model import LogisticRegression
x_train = vectorizer.transform(discs.SQK_DESC)
logis = LogisticRegression(random_state=random_state,  multi_class='ovr', n_jobs = -1)#.fit(subata_x_train, subata_discs.ATA_SUBATA_PRED.values)

logis.fit(x_train, discs.PROFILETYPE_LOOKUP.values)


discs['PROFILE_TYPE_PRED'] = logis.predict(x_train)
discs.to_excel('prof_prediction_logis_20230117_1.xlsx')


# joblib.dump(main_clf, 'ata_classif_linearsvc_proba_20221222.pkl')
joblib.dump(logis, 'profile_pred_logis_20230117_1.pkl')
# joblib.dump(vectorizer, 'vectorizer_logis_20230117_1.pkl')
