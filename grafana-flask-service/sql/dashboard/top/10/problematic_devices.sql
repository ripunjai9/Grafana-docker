SELECT
    now() AS time,
    e_ac.Xname AS DeviceName,
    COUNT(*) count
FROM
    master_dev.legend_device AS ld,
    master_events.events_active AS e_ac,
    master_biz.organizations AS org
WHERE
    e_ac.Xname = ld.device
    AND ld.roa_id = org.roa_id
    AND org.company IN %s
    AND e_ac.eseverity != 0
GROUP BY
    e_ac.Xid
ORDER BY
    count DESC
limit
    10