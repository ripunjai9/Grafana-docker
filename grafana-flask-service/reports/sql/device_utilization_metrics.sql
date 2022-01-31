SELECT
    o.company AS Organization,
    ld.device AS Device,
    concat(round(AVG(nh.avg_data), 2), '%%') AS 'CPU %% AVG',
    concat(round(MAX(nh.max_data), 2), '%%') AS 'CPU %% Peak'
FROM
    NET_SNMP_CPU_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND o.company IN %s
    AND ld.device in %s
    AND nh.collection_time BETWEEN %s
    AND %s
GROUP BY
    ld.device
ORDER BY
    nh.avg_data DESC

===next===

SELECT
    o.company AS Organization,
    ld.device AS Device,
    concat(round(AVG(nh.avg_data), 2), '%%') AS 'Mem %% AVG',
    concat(round(MAX(nh.max_data), 2), '%%') AS 'Mem %% Peak'
FROM
    NET_SNMP_PHYSICAL_MEMORY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = PHYSICAL_MEMORY_UTILIZATION_PID
    AND o.company IN %s
    AND ld.device in %s
    AND nh.collection_time BETWEEN %s
    AND %s
GROUP BY
    ld.device
ORDER BY
    nh.avg_data DESC
===next===

SELECT
    o.company AS Organization,
    ld.device AS Device,
    concat(round(AVG(nh.avg_data), 2), '%%') AS 'Swap %% AVG',
    concat(round(MAX(nh.max_data), 2), '%%') AS 'Swap %% Peak'
FROM
    NET_SNMP_SWAP_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = SWAP_UTILIZATION_PID
    AND o.company IN %s
    AND ld.device in %s
    AND nh.collection_time BETWEEN %s
    AND %s
GROUP BY
    ld.device
ORDER BY
    nh.avg_data DESC;
===next=== 


SELECT
    o.company AS Organization,
    ld.device AS Device,
    concat(round(avg(nd.avg_d_check) * 100, 2), '', '%%') AS 'Avail %% Avg',
    concat(round(avg(nd.max_d_check) * 100, 2), '', '%%') AS 'Avail %% Peak',
    concat(round(avg(nd.avg_d_latency), 2), '', 'ms') AS 'Latency %% Avg',
    concat(round(avg(nd.max_d_latency), 2), '', 'ms') AS 'Latency %% Peak'
FROM
    data_avail.normalized_daily nd,
    master_dev.legend_device ld,
    master_biz.organizations o
WHERE
    ld.roa_id = o.roa_id
    AND o.company IN %s
    AND ld.device in %s
    AND nd.did = ld.id
    AND nd.collection_time BETWEEN %s
    AND %s
group by
    ld.device
Order by
    nd.avg_d_check DESC
