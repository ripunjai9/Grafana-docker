SELECT
    o.company AS Organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS Location,
    la.make AS Vendor,
    CONCAT(ROUND(nd.avg_d_check * 100)) AS 'Device Availability'
FROM
    data_avail.normalized_daily nd,
    master_dev.legend_device ld
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family),
    master_biz.organizations o,
    master_biz.legend_asset la,
    master_biz.asset_location al
WHERE
    ld.roa_id = o.roa_id
    AND la.did = ld.id
    AND al.iid = la.id
    AND o.company IN %s
    AND la.type = %s
    AND nd.did = ld.id
    AND nd.collection_time > DATE_ADD(NOW(), INTERVAL -1 DAY)
    AND nd.avg_d_check <= 1
GROUP BY
    ld.ip