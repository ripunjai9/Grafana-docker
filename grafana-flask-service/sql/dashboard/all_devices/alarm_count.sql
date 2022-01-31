SELECT
    count(ea.id) AS 'Alarm Count'
FROM
    master_biz.organizations o,
    master_dev.legend_device ld,
    master_events.events_active ea
WHERE
    (ld.roa_id = o.roa_id)
    AND o.company IN %s
    AND (ld.id = ea.Xid)
    AND ea.eseverity IN ('4', '3', '2', '1')