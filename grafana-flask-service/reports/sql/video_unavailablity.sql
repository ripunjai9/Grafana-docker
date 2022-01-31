SELECT
    o.company AS Organization,
    ld.device AS "Device Name",
    la.type AS "Device Type",
    dca.cat_name AS 'Device Category',
    ROUND(AVG (1 - nd.avg_d_check) *(24), 2) AS 'Unavailability in Hours'
FROM
    data_avail.normalized_daily nd,
    master_dev.legend_device ld,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.organizations o,
    master_biz.legend_asset la
WHERE
    ld.roa_id = o.roa_id
    AND o.company IN %s
    AND ld.class_type = dcl.class_type
    AND dca.Fid = dcl.family
    AND la.did = ld.id
    AND ld.device IN %s
    AND (
        la.type IN ('Video End Point')
        OR dca.cat_name IN ('Video.Endpoint')
    )
    AND nd.did = ld.id
    AND nd.collection_time BETWEEN %s
    AND %s
GROUP BY
    ld.device
ORDER BY
    la.type ASC