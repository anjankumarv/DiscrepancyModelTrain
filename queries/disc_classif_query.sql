
select distinct s.squawk_id, s.date_opened, p.model_id, t.model_name, s.ata_lookup ata, s.SUPPLEMENT_ATA_LOOKUP sub_ata, t.sqk_cnt as group_count, 
REGEXP_REPLACE(TRIM(s.description), CHR(12)||'|'||CHR(14)||'|'||CHR(10)||'|'||CHR(13)||'|¦|\|', '') description
  
from csi.squawk s 
inner join csi.profile p on p.profile_id = s.profile_id and p.status = '0'
 inner join csi.linkenterpriserel ler on ler.profile_id = p.profile_id --and ler.enterprise_id = '344197.DB1'
-- inner join csi.enterprise e on e.enterprise_id = ler.enterprise_id --and e.enterprise_id = '491251.DB1'--e.name like 'WHEELS UP PRIVATE%' --'WHEELS UP PRIVATE%'
inner join csi.linkenterprises le on le.child_enterprise_id = ler.enterprise_id and le.parent_enterprise_id = '491251.DB1'
inner join (
    select * from (
        select model_id, MODEL_NAME, ata_lookup, SUPPLEMENT_ATA_LOOKUP, sqk_cnt, row_number() over(partition by model_id order by sqk_cnt desc) as rnk from (
            select m.model_id, MODEL_NAME, S.ATA_LOOKUP, s.SUPPLEMENT_ATA_LOOKUP, count(distinct squawk_id) sqk_cnt from csi.squawk s 
            inner join csi.profile p on p.profile_id = s.profile_id 
            inner join csi.linkenterpriserel ler on ler.profile_id = p.profile_id --and ler.enterprise_id = '344197.DB1'
            inner join csi.linkenterprises le on le.child_enterprise_id = ler.enterprise_id and le.parent_enterprise_id = '491251.DB1'
            --inner join csi.enterprise e on e.enterprise_id = ler.enterprise_id --and e.enterprise_id = '491251.DB1' -- e.name like 'WHEELS UP PRIVATE%'--'WHEELS UP PRIVATE%'
            inner join csi.model m on m.model_id = p.model_id 
            where (m.MODEL_NAME like 'CITATION X%' or model_name like 'BEECHJET 400%') 
            --and DATE_OPENED > sysdate - 90 
            and DATE_OPENED  > sysdate-365*2 -- to_date('2021-01-01', 'YYYY-MM-DD') --between to_date('2022-04-01', 'YYYY-MM-DD') and to_date('2022-05-01', 'YYYY-MM-DD')
            and m.status = '0' and p.status = '0' and s.status = '0' 
            and trim(S.ATA_LOOKUP) is not null and s.ATA_LOOKUP not like '%-%' and s.SUPPLEMENT_ATA_LOOKUP is not null
            group by m.model_id, MODEL_NAME, S.ATA_LOOKUP, S.SUPPLEMENT_ATA_LOOKUP
            order by 1, 5 desc
        ) 
        order by model_id, rnk
    ) --where rnk < 11
) t on t.model_id = p.model_id and s.ata_lookup = t.ata_lookup and s.SUPPLEMENT_ATA_LOOKUP = t.SUPPLEMENT_ATA_LOOKUP and s.status = '0'
--inner join csi.linksquawktask lst on lst.squawk_id = s.squawk_id
-------------------------------------------------------------------------------------------
--and s.DATE_OPENED > sysdate - 90 
and s.DATE_OPENED > sysdate- 365*2 --to_date('2021-01-01', 'YYYY-MM-DD') --between to_date('2022-04-01', 'YYYY-MM-DD') and to_date('2022-05-01', 'YYYY-MM-DD')
order by model_name, sqk_cnt desc


select distinct s.squawk_id, s.profile_id, s.date_opened, p.model_id, m.model_name, s.ata_lookup ata, s.SUPPLEMENT_ATA_LOOKUP sub_ata,
--REGEXP_REPLACE(TRIM(s.description), CHR(12)||'|'||CHR(14)||'|'||CHR(10)||'|'||CHR(13)||'|¦|\|', '') description,
edw.clean_notes(s.description) sqk_desc,
edw.clean_notes(n.note) corr_action
  from csi.squawk s 
  inner join csi.profile p on p.profile_id = s.profile_id and p.status = '0'
  --inner join csi.linkprofiles lp on lp.child_profile_id = p.profile_id or lp.parent_profile_id = p.profile_id
  inner join csi.linkenterpriserel ler on ler.profile_id = p.profile_id
  inner join csi.linkenterprises le on le.child_enterprise_id = ler.enterprise_id and le.parent_enterprise_id = '491251.DB1'

inner join csi.model m on m.model_id = p.model_id and m.status = '0'
left outer join csi.note n on n.note_id = s.CORRECTIVE_ACTION_NOTE_ID and n.status = '0'
where DATE_OPENED  > sysdate-365*2 and (m.MODEL_NAME like 'CITATION X%' or model_name like 'BEECHJET 400%')
and trim(S.ATA_LOOKUP) is not null and s.ATA_LOOKUP not like '%-%' and s.SUPPLEMENT_ATA_LOOKUP is not null
and s.status = '0'

