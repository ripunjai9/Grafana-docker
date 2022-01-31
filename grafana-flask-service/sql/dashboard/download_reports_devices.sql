SELECT
    ld.device AS Device_List
FROM
    master_dev.legend_device ld
    LEFT JOIN master_biz.organizations org ON (ld.roa_id = org.roa_id)
WHERE
    org.company IN %s