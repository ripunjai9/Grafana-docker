SELECT
    count(ea.id) AS Critical,
    CASE
        WHEN ea.eseverity = 1 THEN 'Notice'
        WHEN ea.eseverity = 2 THEN 'Minor'
        WHEN ea.eseverity = 3 THEN 'Major'
        WHEN ea.eseverity = 4 THEN 'Critical'
        ELSE 'Severity Not Found'
    END AS 'Severity'
FROM
    master_biz.organizations o,
    master_dev.legend_device ld,
    master_events.events_active ea
WHERE
    (ld.roa_id = o.roa_id)
    AND o.company IN %s
    AND (ld.id = ea.Xid)
    AND ea.eseverity != 0
GROUP BY
    ea.eseverity