SELECT
    now() AS time,
    left(e_ac.emessage, 50) AS Message,
    COUNT(*) Message_count
FROM
    master_dev.legend_device AS ld,
    master_events.events_active AS e_ac,
    master_biz.organizations AS org
WHERE
    e_ac.Xname = ld.device
    AND (ld.roa_id = org.roa_id)
    AND org.company IN %s
GROUP BY
    e_ac.emessage
ORDER BY
    Message_count DESC
limit
    6