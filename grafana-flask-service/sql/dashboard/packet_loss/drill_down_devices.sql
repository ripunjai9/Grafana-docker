SELECT
    ld.device AS Device
FROM
    POLYCOM_GS_CALL_QUALITY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family)
WHERE
    nh.pres_id = MAX_PACKET_LOSS_PID
    AND nh.collection_time > DATE_ADD(NOW(), INTERVAL -1 DAY)
    AND o.company IN %s
GROUP BY
    nh.did
ORDER BY
    nh.avg_data DESC
 LIMIT
    10
