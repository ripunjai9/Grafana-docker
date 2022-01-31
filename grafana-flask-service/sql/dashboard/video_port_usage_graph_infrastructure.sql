SELECT
    nhkk.collection_time AS time,
    nhkk.avg_data AS "Total Available",
    concat(al.data, ' ', "Used Port %%")
FROM
    master_dev.legend_device ld
    LEFT JOIN POLYCOM_DMA_MCU_VIDEO_USAGE_DID.normalized_hourly nhkk ON nhkk.did = ld.id,
    POLYCOM_DMA_MCU_VIDEO_USAGE_DID.app_label al
WHERE
    nhkk.pres_id = PERCENTAGE_DMA_USED_PORTS_PID
    AND al.did = nhkk.did
    AND al.ind = nhkk.ind
    AND ld.device IN %s
    AND nhkk.collection_time BETWEEN %s
    AND %s