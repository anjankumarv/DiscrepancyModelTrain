from pydoc import describe
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing_new import preprocessor_new, preprocessor, process_task_nbr_v1, process_part_nbr_str, replace_spcl_char, process_position_code
from sklearn.externals import joblib

ata_model = joblib.load(r'resources\ata_classif_linearsvc.pkl')
subata_model = joblib.load(r'resources\subata_classif_linearsvc.pkl')
vectorizer = joblib.load(r'resources\vectorizer.pkl')
print('1')

subata_logis_vectorizer = joblib.load(r'resources\subata_vectorizer.pkl')
subata_logis_model = joblib.load(r'resources\subata_classif_logis.pkl')
print('2')

squawks = pd.read_csv(r'resources\all_sqk_desc_model_all.LST', header = None, sep = '|', 
    names=['ATA_SUBATA', 'SQK_DESC', 'MODEL_ID', 'ATA', 'SUB_ATA'], error_bad_lines=False, encoding = "ISO-8859-1", dtype=str)
squawks = squawks.fillna('')
print('3')

X1 = vectorizer.transform(squawks.SQK_DESC)
print('4')

squawks['PREDICTED_ATA'] = ata_model.predict(X1)
squawks['PREDICTED_SUBATA'] = subata_model.predict(X1)
print('5')

X2 = subata_logis_vectorizer.transform(squawks.SQK_DESC)
squawks['PREDICTED_SUBATA_LOGIS'] = subata_logis_model.predict(X2)
print('6')

squawks.to_excel('old_squacks_pred.xlsx')
print('7')





