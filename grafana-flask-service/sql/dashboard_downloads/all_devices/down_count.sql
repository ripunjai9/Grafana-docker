Select
       o.company as Organization,
       ld.device as 'Device Name',
       ld.ip as 'Device IP',
       dca.cat_name AS 'Device Category',
       la.type AS 'Device Type',
       CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
       al.location as 'Device Location',
       la.make as Vendor,
       ea.emessage AS 'Event Message',
       CASE
              WHEN dst.state = 0 THEN 'Healthy'
              WHEN dst.state = 1 THEN 'Notice'
              WHEN dst.state = 2 THEN 'Minor'
              WHEN dst.state = 3 THEN 'Major'
              WHEN dst.state = 4 THEN 'Critical'
              ELSE 'Severity Not Found'
       END as ESeverity,
       ea.date_last AS 'Last Detected'
FROM
       master_dev.legend_device ld,
       master_biz.organizations o,
       master.definitions_dev_classes dcl,
       master.definitions_dev_cats dca,
       master_events.events_active ea,
       master_dev.device_state dst,
       master_biz.legend_asset la,
       master_biz.asset_location al
WHERE
       (ld.roa_id = o.roa_id)
       AND (ld.class_type = dcl.class_type)
       AND (dca.Fid = dcl.family)
       AND (ld.id = ea.Xid)
       AND (dst.did = ld.id)
       AND ea.emessage IN %s
       AND o.company IN %s
       AND la.did = ld.id
       AND al.iid = la.id
       AND ea.eseverity IN %s