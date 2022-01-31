SELECT
    now() AS time,
    ld.device AS Device,
    nhkk.avg_data AS average
FROM
    master_dev.legend_device ld
    LEFT JOIN POLYCOM_DMA_MCU_VIDEO_USAGE_DID.normalized_hourly nhkk ON nhkk.did = ld.id
WHERE
    nhkk.pres_id = PERCENTAGE_DMA_USED_PORTS_PID
    AND ld.device IN (
        SELECT
            ld.device AS DeviceName
        FROM
            master_dev.legend_device ld
            LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
            LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
            LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family)
            LEFT JOIN master_biz.legend_asset la ON (la.did = ld.id)
        WHERE
            o.company IN %s
            AND la.type = %s
        ORDER BY
            device
    )
    AND nhkk.collection_time > DATE_ADD(NOW(), INTERVAL -1 HOUR)
GROUP BY
    ld.device
ORDER BY
    average DESC