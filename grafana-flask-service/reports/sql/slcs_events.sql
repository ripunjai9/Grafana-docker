SELECT
    org.company AS 'Organisation',
    ld.id AS 'Device ID',
    ld.ip AS 'Device IP',
    ld.device AS 'Device Name',
    sum(es.ecount) AS 'Detection Count',
    CASE
        WHEN es.eseverity = 0 THEN 'Healthy'
        WHEN es.eseverity = 1 THEN 'Notice'
        WHEN es.eseverity = 2 THEN 'Minor'
        WHEN es.eseverity = 3 THEN 'Major'
        WHEN es.eseverity = 4 THEN 'Critical'
        ELSE 'Severity Not Found'
    END AS 'Severity',
    pe.ename AS 'Event Message',
    MIN(es.date_first) AS 'First Occurrence',
    Max(es.date_first) AS 'Last Detected'
FROM
    master_events.events_summary es,
    master.policies_events pe,
    master_biz.organizations AS org,
    master_dev.legend_device AS ld
WHERE
    pe.id = es.etype
    AND es.Xid = ld.id
    AND ld.roa_id = org.roa_id
    AND org.company IN %s
    AND ld.device IN %s
    AND es.date_first BETWEEN %s
    AND %s
GROUP BY
    es.Xid,
    es.etype
ORDER BY
    pe.ename