from pydoc import describe
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing_new import preprocessor_new, preprocessor, process_task_nbr_v1, process_part_nbr_str, replace_spcl_char, process_position_code
from sklearn.externals import joblib
# from processing import preprocessor

raw_desc = 'FLIGHT GUIDANCE CONTROLLER ALT LIGHT INOP'

vectorizer_new = joblib.load(r'vectorizer_proba_1.pkl')
ata_model_new = joblib.load(r'ata_classif_linearsvc_proba_1.pkl')
subata_model_new = joblib.load(r'subata_classif_linearsvc_proba_1.pkl')

# subata_vectorizer_old = joblib.load('subata_vectorizer.pkl')
# subata_model_old_logis = joblib.load('subata_classif_logis.pkl')

# pred_ata2 = svc_model_old.predict(vectorizer_old.transform([raw_desc]))[0]

# vectorizer_new = joblib.load('vectorizer_only_citx_beech.pkl')
# svc_model_new = joblib.load('ata_classif_linearsvc_only_citx_beech.pkl')

# desc = preprocessor_new(raw_desc)
# desc = desc + ' '+ '10443_DB1'
# pred_ata1 = svc_model_new.predict(vectorizer_new.transform([desc]))[0]

print('models loaded')  



# print(pred_ata1, pred_ata2)
# wheelsup_squawks = pd.read_csv()
# all_squawks = pd.read_csv(r'resources\all_sqk_desc_model_all.LST', header = None, sep = '|', encoding = "ISO-8859-1", 
#                         names = ['SUBATA', 'SQK_DESC', 'MODEL_ID', 'ATA_LOOKUP', 'SUBATA_LOOKUP'], dtype=str)
all_squawks = pd.read_csv(r'data\squawks_all_with_date.LST', header = 0, sep = '|', encoding = "ISO-8859-1", dtype=str, error_bad_lines=False)
all_squawks = all_squawks.fillna('')
all_squawks = all_squawks[0:100]
# all_squawks = pd.read_csv(r'resources\all_sqk_desc_model_all.LST', header = None, sep = '|', encoding = "ISO-8859-1", 
#                         names = ['SUBATA', 'SQUAWK_DESCRIPTION', 'MODEL_ID', 'ATA_LOOKUP', 'SUBATA_LOOKUP'], dtype=str)

# all_squawks = pd.read_excel(r'E:\Projects\Repositories\DiscrepancyModelTrain\resources\last_2_yr_squawks.xlsx', header=0, dtype=str)

ata_with_prob  = ata_model_new.predict_proba(vectorizer_new.transform(['UPDATE FMS DATABASE']))
pred_vals = []
pred_confs = []
for i, val in enumerate(ata_with_prob):
    pred_conf = ata_with_prob[i].max()
    pred_val = list(ata_with_prob[i]).index(pred_conf)
    pred_confs.append(pred_conf)
    pred_vals.append(pred_val)
    
#UPDATE FMS DATABASE


# all_squawks['PROCESSED_DESCRIPTION'] = all_squawks['SQUAWK_DESCRIPTION'].apply(preprocessor)
# all_squawks['filenames'] = dataframe['filenames'].str.replace('?|/', '', regex=True)

# test_squawks = all_squawks[(all_squawks['MODEL_ID'] == '16103.DB1') | (all_squawks['MODEL_ID'] == '10443.DB1') 
#                             | (all_squawks['MODEL_ID'] == '7704.DB2')| (all_squawks['MODEL_ID'] == '4443.DB1')
#                             | (all_squawks['MODEL_ID'] == '3604.DB1')].reset_index()

# all_squawks.to_excel('test.xlsx', engine='xlsxwriter')
# print(test_squawks.shape)  
print('lst loaded')                          
# New model efficiency
# test_squawks['PROCESSED_DESCRIPTION'] = test_squawks['SQUAWK_DESCRIPTION'].apply(preprocessor_new)
# test_squawks['PROCESSED_MODEL_ID'] = test_squawks['MODEL_ID'].apply(replace_spcl_char)
# test_squawks['PROCESSED_DESCRIPTION'] = test_squawks['PROCESSED_DESCRIPTION'] + ' '+ test_squawks['PROCESSED_MODEL_ID']
# x_test_new = vectorizer_new.transform(test_squawks.PROCESSED_DESCRIPTION)
# Y_new = svc_model_new.predict(x_test_new)
# print('predicted new')

# Old model efficiency
# test_squawks['PROCESSED_DESCRIPTION'] = test_squawks['SQUAWK_DESCRIPTION'].apply(preprocessor_new)
# test_squawks['PROCESSED_MODEL_ID'] = test_squawks['PROCESSED_MODEL_ID'].apply(replace_spcl_char)
# test_squawks['PROCESSED_DESCRIPTION'] = test_squawks['PROCESSED_DESCRIPTION'] + ' '+ test_squawks['PROCESSED_MODEL_ID']

x_test = vectorizer_new.transform(all_squawks.SQK_DESC)
# Y_new = ata_model_new.predict(x_test)
print('predicted')
all_squawks['PREDICTED_ATA'] = ata_model_new.predict(x_test)
all_squawks['PREDICTED_SUBATA'] = subata_model_new.predict(x_test)

# x_test_old = subata_vectorizer_old.transform(all_squawks.SQK_DESC)
# all_squawks['PREDICTED_SUBATA_LOGIS'] = subata_model_old_logis.predict(x_test_old)
# test_squawks['PREDICTED_NEW'] = Y_new

all_squawks.to_excel('latest_logis_model_with_latest_data.xlsx', engine='xlsxwriter')




