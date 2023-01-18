set colsep |;
set pagesize 0;  
set trimspool on;
set headsep off;
set linesize 4000; 
set numw 9;
SET TERMOUT OFF;
set feedback off;
spool prediction_comparison.LST;

SELECT 'SQUAWK_ID|DESCRIPTION|PROFILE_ID|MODEL_ID|ATA|SUBATA|RECLASSIFIED_ATA_DT|RECLASSIFIED_SUBATA_DT|RECLASSIFIED_TYPE_DT|PRED_CONF_DT|RECLASSIFIED_ATA_SVC|RECLASSIFIED_SUBATA_SVC|RECLASSIFIED_TYPE_SVC|PRED_CONF_SVC' info FROM DUAL
UNION ALL
select 
SQUAWK_ID || '|' || 
edw.clean_notes(trim(s.DESCRIPTION)) || '|' || 
s.profile_id || '|' ||
m.model_id || '|' ||
trim(s.ATA_LOOKUP) || '|' ||
trim(s.supplement_ata_lookup) || '|' ||
RECLASSIFIED_ATA_1|| '|' ||
RECLASSIFIED_ATASUBATA_1|| '|' ||
reclassified_type_1 || '|' || 
PRED_CONFIDENCE_1 || '|' ||
RECLASSIFIED_ATA_2|| '|' ||
RECLASSIFIED_ATASUBATA_2|| '|' ||
reclassified_type_2 || '|' ||
PRED_CONFIDENCE_2 
From edw.squawk s
inner join csi.profile p on p.profile_id = s.profile_id 
inner join csi.model m on m.model_id = p.model_id
where p.status = '0' and m.status = '0' and s.is_deleted = '0' 
and trim(S.ATA_LOOKUP) is not null and trim(s.SUPPLEMENT_ATA_LOOKUP) is not null
and s.ATA_LOOKUP not like '%-%';
spool off;