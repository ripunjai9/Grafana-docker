SELECT
    org.company AS Organization,
    ld.device AS Device,
    ec.emessage AS 'Event Message',
    CASE
        WHEN ec.eseverity = 0 THEN 'Healthy'
        WHEN ec.eseverity = 1 THEN 'Notice'
        WHEN ec.eseverity = 2 THEN 'Minor'
        WHEN ec.eseverity = 3 THEN 'Major'
        WHEN ec.eseverity = 4 THEN 'Critical'
        ELSE 'Severity Not Found'
    END AS 'Severity',
    ec.date_first AS 'First Occurrence',
    ec.date_last AS 'Last Detected',
    'cleared' AS 'Event Status'
FROM
    master_events.events_cleared ec,
    master_biz.organizations AS org,
    master_dev.legend_device AS ld
WHERE
    ec.Xid = ld.id
    AND ld.roa_id = org.roa_id
    AND org.company IN %s
    AND ld.device IN %s
    AND ec.date_first BETWEEN %s
    AND %s
UNION
SELECT
    org.company AS Organization,
    ld.device AS Device,
    ec.emessage AS 'Event Message',
    CASE
        WHEN ec.eseverity = 0 THEN 'Healthy'
        WHEN ec.eseverity = 1 THEN 'Notice'
        WHEN ec.eseverity = 2 THEN 'Minor'
        WHEN ec.eseverity = 3 THEN 'Major'
        WHEN ec.eseverity = 4 THEN 'Critical'
        ELSE 'Severity Not Found'
    END AS 'Severity',
    ec.date_first AS 'First Occurrence',
    '' AS 'Last Detected',
    'active' AS 'Event Status'
FROM
    master_events.events_active ec,
    master_biz.organizations AS org,
    master_dev.legend_device AS ld
WHERE
    ec.Xid = ld.id
    AND ld.roa_id = org.roa_id
    AND org.company IN %s
    AND ld.device IN %s
    AND ec.date_first BETWEEN %s
    AND %s
ORDER BY
    Device