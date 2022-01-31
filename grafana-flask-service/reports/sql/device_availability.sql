SELECT
    o.company AS Organization,
    ld.device AS 'Device Name',
    CONCAT(ROUND(avg(nd.avg_d_check), 2) * 100, '%%') AS 'Uptime %%',
    CONCAT(100 - (ROUND(avg(nd.avg_d_check), 2)) * 100, '%%') AS 'DownTime %%',
    $Durationtime - (($Durationtime) / 100) *(ROUND(avg(nd.avg_d_check), 2) * 100) AS 'Downtime',
    ld.create_date AS DiscoveryDate,
    (($Durationtime) / 100) *(ROUND(avg(nd.avg_d_check), 2) * 100) AS 'Uptime'
FROM
    data_avail.normalized_daily nd,
    master_dev.legend_device ld,
    master_biz.organizations o,
    master_biz.legend_asset la
WHERE
    ld.roa_id = o.roa_id
    AND la.did = ld.id
    AND nd.did = ld.id
    AND o.company IN %s
    AND ld.device IN %s
    AND nd.collection_time BETWEEN %s
    AND %s
GROUP BY
    ld.device
ORDER BY
    ld.device DESC