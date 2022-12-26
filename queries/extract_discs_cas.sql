select t.*,  row_number() over(order by squawk_id) from ( 
select distinct m.model_id, MODEL_NAME, S.ATA_LOOKUP, s.SUPPLEMENT_ATA_LOOKUP, s.squawk_id --, count(distinct squawk_id) sqk_cnt 
 from csi.squawk s 
            inner join csi.profile p on p.profile_id = s.profile_id 
            inner join csi.linkenterpriserel ler on ler.profile_id = p.profile_id --and ler.enterprise_id = '344197.DB1'
            inner join csi.linkenterprises le on le.child_enterprise_id = ler.enterprise_id and le.parent_enterprise_id = '491251.DB1'
            --inner join csi.enterprise e on e.enterprise_id = ler.enterprise_id --and e.enterprise_id = '491251.DB1' -- e.name like 'WHEELS UP PRIVATE%'--'WHEELS UP PRIVATE%'
            inner join csi.model m on m.model_id = p.model_id 
            where (m.MODEL_NAME like 'CITATION X%' or model_name like 'BEECHJET 400%') 
            --and DATE_OPENED > sysdate - 90 
            and DATE_OPENED between to_date('2022-04-01', 'YYYY-MM-DD') and to_date('2022-05-01', 'YYYY-MM-DD')
            and m.status = '0' and p.status = '0' and s.status = '0' 
            and trim(S.ATA_LOOKUP) is not null and s.ATA_LOOKUP not like '%-%' and s.SUPPLEMENT_ATA_LOOKUP is not null
            --group by m.model_id, MODEL_NAME, S.ATA_LOOKUP, S.SUPPLEMENT_ATA_LOOKUP
            --order by 1, 5 desc
            
) t

select s.description, n.* from csi.squawk s
inner join csi.note n on n.note_id = s.CORRECTIVE_ACTION_NOTE_ID


select * from inv.part where part_nbr = '174095-58'
