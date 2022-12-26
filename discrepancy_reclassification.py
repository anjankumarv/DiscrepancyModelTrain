from pydoc import describe
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing_new import preprocessor_new, preprocessor, process_task_nbr_v1, process_part_nbr_str, replace_spcl_char, process_position_code
from sklearn.externals import joblib

def format_ata_subata(subata):
    subata = str(subata)
    if len(subata) == 3:
        return '{0}-{1}0'.format(subata[:2], subata[-1:])
    return '0{0}-{1}0'.format(subata[:1], subata[-1:])


print(format_ata_subata('232'))
print(format_ata_subata('28'))

squawks = pd.read_excel(r'subata_pred_with_ata_0.xlsx', header=0, dtype=str)
squawks['MANAGED_ATA_SUBATA'] = ''
squawks['MANAGED_ATA_SUBATA_STATUS'] = ''
print(len(squawks))

for idx, row in squawks.iterrows():
    if idx%100000 == 0:
        print(idx)

    if row['ATA_SUBATA_PRED'] == row['PREDICTED_SUBATA']:
        if len(row['SUB_ATA']) == 1:
            squawks.at[idx, 'MANAGED_ATA_SUBATA'] = row['ATA']+'-'+row['SUB_ATA']
            squawks.at[idx, 'MANAGED_ATA_SUBATA_STATUS'] = 'MATCHED'

        elif len(row['SUB_ATA']) == 2:
            if int(row['SUB_ATA'])%10 == 0:
                squawks.at[idx, 'MANAGED_ATA_SUBATA'] = row['ATA']+'-'+row['SUB_ATA']
                squawks.at[idx, 'MANAGED_ATA_SUBATA_STATUS'] = 'MATCHED'
            else:
                squawks.at[idx, 'MANAGED_ATA_SUBATA'] = row['ATA']+'-'+row['SUB_ATA']
                squawks.at[idx, 'MANAGED_ATA_SUBATA_STATUS'] = 'MATCHED_USER_PREF_2D_SUBATA'
        
        elif len(row['SUB_ATA']) == 3:
            if int(row['SUB_ATA'])%100 == 0:
                squawks.at[idx, 'MANAGED_ATA_SUBATA'] = row['ATA']+'-'+row['SUB_ATA']
                squawks.at[idx, 'MANAGED_ATA_SUBATA_STATUS'] = 'MATCHED'
            else:
                squawks.at[idx, 'MANAGED_ATA_SUBATA'] = row['ATA']+'-'+row['SUB_ATA']
                squawks.at[idx, 'MANAGED_ATA_SUBATA_STATUS'] = 'MATCHED_USER_PREF_3D_SUBATA'
    else:
        squawks.at[idx, 'MANAGED_ATA_SUBATA'] = format_ata_subata(row['PREDICTED_SUBATA'])
        squawks.at[idx, 'MANAGED_ATA_SUBATA_STATUS'] = 'MODEL_PREF'

squawks.to_excel('subata_pred_with_ata_0_managed.xlsx')
print('7')





