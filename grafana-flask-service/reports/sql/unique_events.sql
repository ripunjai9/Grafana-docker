SELECT
    pe.ename AS 'Event Message',
    sum(es.ecount) AS 'Detection Count Duration',
    $date_time AS date_time
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
    AND es.date_first BETWEEN ($duration)
    AND ld.device IN %s
GROUP BY
    es.etype
ORDER BY
    pe.ename