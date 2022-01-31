SELECT
    nhkk.collection_time AS time,
    nhkk.avg_data AS "Total Available",
    concat("Used License %%", '', '[', nhkk.ind, ']')
FROM
    master_dev.legend_device ld
    LEFT JOIN POLYCOM_RPRM_LICENSES_ENDPOINTS_COUNT_DID.normalized_hourly nhkk ON nhkk.did = ld.id
WHERE
    nhkk.pres_id = PERCENTAGE_SEAT_LICENSES_USED_PID
    AND ld.device IN %s
    AND nhkk.collection_time BETWEEN %s
    AND %s