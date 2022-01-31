SELECT
    now() AS time,
    avg(nd.avg_d_check) * 100 AS aggg,
    ld.device AS deviceName
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
    AND la.type != %s
    AND nd.did = ld.id
    AND nd.collection_time > DATE_ADD(NOW(), INTERVAL -1 DAY)
    AND nd.avg_d_check <= 1
GROUP BY
    ld.ip
ORDER BY
    aggg asc