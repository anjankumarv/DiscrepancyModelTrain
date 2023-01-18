set colsep |;
set pagesize 0;  
set trimspool on;
set headsep off;
set linesize 4000; 
set numw 9;
SET TERMOUT OFF;
set feedback off;
spool squawks_all.LST;

SELECT to_clob('SQUAWK_ID|PROFILE_ID|MODEL_ID|ATA|SUB_ATA|ATA_SUBATA|SQK_DESC|CORRECTIVE_ACTION') info FROM DUAL
UNION ALL
select 
to_clob(s.squawk_id || '|' ||
s.profile_id || '|' ||
m.model_id || '|' ||
trim(s.ATA_LOOKUP) || '|' ||
trim(s.supplement_ata_lookup) || '|' ||
(case when REGEXP_LIKE(trim(s.supplement_ata_lookup), '^[[:digit:]]+$') and REGEXP_LIKE(trim(s.ATA_LOOKUP), '^[[:digit:]]+$') then 
trim(s.ATA_LOOKUP)||SUBSTR(trim(s.supplement_ata_lookup), 1, 1) else '' end)|| '|' ||
edw.clean_notes(trim(s.DESCRIPTION))) || '|' ||
to_clob(edw.clean_notes(trim(n.note)))
from csi.squawk s
inner join csi.profile p on p.profile_id = s.profile_id 
inner join csi.model m on m.model_id = p.model_id
inner join csi.note n on n.note_id = s.corrective_action_note_id
where p.status = '0' and m.status = '0' and s.status = '0' 
and trim(S.ATA_LOOKUP) is not null and trim(s.SUPPLEMENT_ATA_LOOKUP) is not null
and s.ATA_LOOKUP not like '%-%';
spool off;