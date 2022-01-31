SELECT
    o.company AS organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    Concat(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS 'Device Location',
    la.make AS vendor,
    Concat(Round(nd.avg_d_check * 100), '%%') AS 'Device Availability'
FROM
    data_avail.normalized_daily nd,
    master_dev.legend_device ld
    LEFT JOIN master.definitions_dev_classes dcl ON (
        ld.class_type = dcl.class_type
    )
    LEFT JOIN master.definitions_dev_cats dca ON (dca.fid = dcl.family),
    master_biz.organizations o,
    master_biz.legend_asset la,
    master_biz.asset_location al
WHERE
    ld.roa_id = o.roa_id
    AND la.did = ld.id
    AND al.iid = la.id
    AND la.type = %s
    AND o.company IN %s
    AND nd.did = ld.id
    AND nd.collection_time > date_add(now(), interval -1 day)
    AND nd.avg_d_check <= 1
GROUP BY
    ld.ip