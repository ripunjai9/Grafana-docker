SELECT
    now() AS time,
    ld.device AS Device,
    nh.avg_data AS Peak_Memory
FROM
    NET_SNMP_CPU_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family),
    master_biz.legend_asset la
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND nh.collection_time > DATE_ADD(NOW(), INTERVAL -1 DAY)
    AND o.company IN %s
    AND la.did = ld.id
    AND la.type = %s
GROUP BY
    nh.did
ORDER BY
    nh.avg_data DESC
LIMIT
    5;