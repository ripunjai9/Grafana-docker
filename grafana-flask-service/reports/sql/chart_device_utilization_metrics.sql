SELECT
    ld.device AS Device,
    nh.collection_time AS 'Date time',
    round(nh.avg_data, 2) AS 'CPU %% AVG',
    '' AS 'Mem %% AVG',
    '' AS 'Swap %% AVG'
FROM
    NET_SNMP_CPU_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND nh.collection_time BETWEEN %s
    AND %s
    AND o.company IN %s
    AND ld.device IN %s
UNION
SELECT
    ld.device AS Device,
    nh.collection_time AS 'Date time',
    '' AS 'CPU %% AVG',
    round(nh.avg_data, 2) AS 'Mem %% AVG',
    '' AS 'Swap %% AVG'
FROM
    NET_SNMP_PHYSICAL_MEMORY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = PHYSICAL_MEMORY_UTILIZATION_PID
    AND nh.collection_time BETWEEN %s
    AND %s
    AND o.company IN %s
    AND ld.device IN %s
UNION
SELECT
    ld.device AS Device,
    nh.collection_time AS 'Date time',
    '' AS 'CPU %% AVG',
    '' AS 'Mem %% AVG',
    round(nh.avg_data, 2) AS 'Swap %% AVG'
FROM
    NET_SNMP_SWAP_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = SWAP_UTILIZATION_PID
    AND nh.collection_time BETWEEN %s
    AND %s
    AND o.company IN %s
    AND ld.device IN %s