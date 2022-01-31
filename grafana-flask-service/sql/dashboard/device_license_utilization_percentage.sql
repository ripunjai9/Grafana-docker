SELECT
    now() AS time,
    ld.device AS Device,
    CASE
        WHEN nhkk.avg_data is NOT NULL THEN avg(nhkk.avg_data)
        WHEN nh.avg_data is NOT NULL THEN avg(nh.avg_data)
        WHEN nhpp.avg_data is NOT NULL THEN avg(nhpp.avg_data)
    END AS avergae
FROM
    master_dev.legend_device ld
    LEFT JOIN POLYCOM_DMA_LICENSES_DID.normalized_hourly nhkk ON nhkk.did = ld.id
    LEFT JOIN POLYCOM_RPAD_BASIC_PERFORMANCE_DID.normalized_hourly nh ON nh.did = ld.id
    LEFT JOIN POLYCOM_RPRM_LICENSES_ENDPOINTS_COUNT_DID.normalized_hourly nhpp ON nhpp.did = ld.id
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master_biz.legend_asset la ON (la.did = ld.id)
WHERE
    (
        nhkk.pres_id = 4493
        OR nh.pres_id = PERCENTAGE_RPAD_LICENSES_USED_PID
        OR nhpp.pres_id = PERCENTAGE_SEAT_LICENSES_USED_PID
    )
    AND (
        nhkk.collection_time > DATE_ADD(NOW(), INTERVAL -1 HOUR)
        OR nh.collection_time > DATE_ADD(NOW(), INTERVAL -1 HOUR)
        OR nhpp.collection_time > DATE_ADD(NOW(), INTERVAL -1 HOUR)
    )
    AND o.company IN %s
    AND la.type = %s
GROUP BY
    ld.device
ORDER BY
    avergae DESC