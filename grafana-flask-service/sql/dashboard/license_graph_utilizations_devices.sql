SELECT
    ld.device AS Device
FROM
    master_dev.legend_device ld
    LEFT JOIN POLYCOM_DMA_LICENSES_DID.normalized_hourly nhkk ON nhkk.did = ld.id
    LEFT JOIN POLYCOM_RPAD_BASIC_PERFORMANCE_DID.normalized_hourly nh ON nh.did = ld.id
    LEFT JOIN POLYCOM_RPRM_LICENSES_ENDPOINTS_COUNT_DID.normalized_hourly nhpp ON nhpp.did = ld.id
WHERE
    (
        nhkk.pres_id = PERCENTAGE_DMA_LICENSE_USED_PID
        OR nh.pres_id = PERCENTAGE_RPAD_LICENSES_USED_PID
        OR nhpp.pres_id = PERCENTAGE_SEAT_LICENSES_USED_PID
    )
    AND ld.device IN (
        SELECT
            ld.device AS DeviceName
        FROM
            master_dev.legend_device ld,
            master_biz.organizations o,
            master.definitions_dev_classes dcl,
            master.definitions_dev_cats dca,
            master_biz.legend_asset la
        WHERE
            (ld.roa_id = o.roa_id)
            AND (ld.class_type = dcl.class_type)
            AND (dca.Fid = dcl.family)
            AND o.company IN %s
            AND la.type = %s
            AND la.did = ld.id
        ORDER BY
            dca.cat_name asc
    )
    AND (
        nhkk.collection_time > DATE_ADD(NOW(), INTERVAL -7 DAY)
        OR nh.collection_time > DATE_ADD(NOW(), INTERVAL -7 DAY)
        OR nhpp.collection_time > DATE_ADD(NOW(), INTERVAL -7 DAY)
    )
GROUP BY
    ld.device