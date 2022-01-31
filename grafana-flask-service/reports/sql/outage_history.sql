SELECT
    o.company,
    ld.device,
    ld.id,
    alert_id,
    user_del,
    date_first
FROM
    master_events.events_cleared ec,
    master_biz.organizations o,
    master_dev.legend_device ld
WHERE
    xid IN (
        SELECT
            id
        FROM
            master_dev.legend_device
    )
    AND alert_id IN (267, 268)
    AND ld.roa_id = o.roa_id
    AND ld.id = xid
    AND o.company IN %s
    AND ld.device IN %s
    AND date_first BETWEEN %s
    AND %s

===next===

SELECT
    o.company,
    ld.device,
    MIN(date_first),
    '' AS end_date,
    'still down' AS still_down
FROM
    master_events.events_active ec,
    master_biz.organizations o,
    master_dev.legend_device ld
WHERE
    xid IN (
        SELECT
            id
        FROM
            master_dev.legend_device
    )
    AND ld.roa_id = o.roa_id
    AND ld.id = xid
    AND o.company IN %s
    AND ld.device IN %s
    AND date_first BETWEEN %s
    AND %s
GROUP BY
    ld.device
ORDER BY
    date_first DESC