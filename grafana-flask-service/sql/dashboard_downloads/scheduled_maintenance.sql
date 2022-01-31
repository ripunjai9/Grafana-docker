SELECT
       org.company AS organization,
       ld.device AS 'Device Name',
       ld.ip AS 'Device IP',
       dca.cat_name AS 'Device Category',
       la.type AS 'Device Type',
       Concat(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
       al.location AS 'Device Location',
       la.make AS 'Vendor',
       t.NAME AS 'Schedule Summary',
       s.description AS 'Schedule Description',
       s.dtstart AS 'Schedule Start Date',
       adddate(s.dtstart, interval s.duration minute) AS 'Schedule End Date'
FROM
       scheduler.schedules s,
       master_dev.legend_device ld,
       scheduler.schedules_to_tasks stt,
       master_biz.organizations org,
       scheduler.tasks t,
       master.definitions_dev_classes dcl,
       master.definitions_dev_cats dca,
       master_biz.legend_asset la,
       master_biz.asset_location al
WHERE
       ld.id = t.xid
       AND la.did = ld.id
       AND al.iid = la.id
       AND stt.task_id = t.task_id
       AND s.schedule_id = stt.schedule_id
       AND ld.roa_id = s.roa_id
       AND ld.roa_id = t.roa_id
       AND ld.class_type = dcl.class_type
       AND dca.fid = dcl.family
       AND ld.roa_id = org.roa_id
       AND org.company IN %s
       AND ADDDATE(s.dtstart, INTERVAL s.duration MINUTE) > CURRENT_TIMESTAMP;