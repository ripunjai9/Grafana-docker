SELECT
    o.company,
    ld.device AS Device,
    nh.max_data AS "CPU Threshold"
FROM
    NET_SNMP_CPU_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family),
    master_biz.legend_asset la
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND o.company IN %s
    AND ld.device IN %s
    AND nh.collection_time BETWEEN %s
    AND %s
    AND la.did = ld.id
GROUP BY
    nh.did
ORDER BY
    nh.avg_data DESC

===next===

SELECT
    o.company,
    ld.device AS Device,
    nh.max_data AS "Memory Threshold"
FROM
    NET_SNMP_PHYSICAL_MEMORY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family),
    master_biz.legend_asset la
WHERE
    nh.pres_id = PHYSICAL_MEMORY_UTILIZATION_PID
    AND o.company IN %s
    AND ld.device IN %s
    AND nh.collection_time BETWEEN %s
    AND %s
    AND la.did = ld.id
GROUP BY
    nh.did
ORDER BY
    nh.avg_data DESC

===next===

SELECT
    o.company,
    ld.device AS Device,
    nh.max_data AS "Swap Threshold"
FROM
    NET_SNMP_SWAP_DID.normalized_daily nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family),
    master_biz.legend_asset la
WHERE
    nh.pres_id = SWAP_UTILIZATION_PID
    AND o.company IN %s
    AND ld.device IN %s
    AND nh.collection_time BETWEEN %s
    AND %s
    AND la.did = ld.id
GROUP BY
    nh.did
ORDER BY
    nh.avg_data DESC

===next===

SELECT
    o.company,
    ld.device AS Device,
    concat(round(avg(nd.sum_d_latency), 2), '', 'ms') AS 'Latency'
FROM
    data_avail.normalized_daily nd,
    master_dev.legend_device ld,
    master_biz.organizations o
WHERE
    ld.id = nd.did
    AND ld.roa_id = o.roa_id
    AND o.company IN %s
    AND ld.device IN %s
    AND nd.collection_time BETWEEN %s
    AND %s
GROUP BY
    nd.did
