SELECT
    ld.device AS 'Device Name',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    t.name AS 'Schedule Summary',
    s.description AS 'Schedule Description',
    s.dtstart AS 'Schedule Start Date',
    ADDDATE(s.dtstart, INTERVAL s.duration MINUTE) AS 'Schedule End Date'
FROM
    scheduler.schedules s,
    master_dev.legend_device ld,
    scheduler.schedules_to_tasks stt,
    master_biz.organizations org,
    scheduler.tasks t,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.legend_asset la
WHERE
    ld.id = t.Xid
    AND stt.task_id = t.task_id
    AND s.schedule_id = stt.schedule_id
    AND ld.roa_id = s.roa_id
    AND ld.roa_id = t.roa_id
    AND ld.class_type = dcl.class_type
    AND dca.Fid = dcl.family
    AND ld.roa_id = org.roa_id
    AND la.did = ld.id
    AND org.company IN %s
    AND ADDDATE(s.dtstart, INTERVAL s.duration MINUTE) > CURRENT_TIMESTAMP;