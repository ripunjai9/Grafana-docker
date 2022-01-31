SELECT
    ld.device AS Device
FROM
    master_dev.legend_device ld
    LEFT JOIN POLYCOM_DMA_MCU_VIDEO_USAGE_DID.normalized_hourly nhkk ON nhkk.did = ld.id
WHERE
    nhkk.pres_id = PERCENTAGE_DMA_USED_PORTS_PID
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
    AND nhkk.collection_time > DATE_ADD(NOW(), INTERVAL -7 DAY)
GROUP BY
    ld.device