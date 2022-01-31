SELECT
    o.company AS Organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS 'Device Location',
    la.make AS Vendor,
    ea.emessage AS 'Event Message',
    CASE
        WHEN dst.state = 0 THEN 'Healthy'
        WHEN dst.state = 1 THEN 'Notice'
        WHEN dst.state = 2 THEN 'Minor'
        WHEN dst.state = 3 THEN 'Major'
        WHEN dst.state = 4 THEN 'Critical'
        ELSE 'Severity Not Found'
    END AS ESeverity,
    date_last AS 'Last Detected'
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
    AND ea.emessage IN (
        'Device Failed Availability Check: UDP - SNMP',
        'Device Failed Availability Check: ICMP - Ping'
    )
    AND o.company IN %s
    AND la.type = %s
    AND la.did = ld.id
    AND al.iid = la.id
    AND ea.eseverity IN ('4', '3', '2', '1')