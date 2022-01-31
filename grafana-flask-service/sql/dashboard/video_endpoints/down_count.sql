SELECT
    Count(*) AS 'Down Count'
FROM
    master_dev.legend_device ld,
    master_biz.organizations o,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_events.events_active ea,
    master_biz.legend_asset la
WHERE
    (ld.roa_id = o.roa_id)
    AND (ld.class_type = dcl.class_type)
    AND (dca.Fid = dcl.family)
    AND (ld.id = ea.Xid)
    AND o.company IN %s
    AND ea.emessage IN (
        'Device Failed Availability Check: UDP - SNMP',
        'Device Failed Availability Check: ICMP - Ping'
    )
    AND la.type = %s
    AND la.did = ld.id