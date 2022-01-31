SELECT
    o.company AS Organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS 'Device Location',
    la.make AS Vendor,
    CONCAT(round(nh.avg_data, 2)) AS 'CPU Utilization Value'
FROM
    NET_SNMP_CPU_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family),
    master_biz.legend_asset la,
    master_biz.asset_location al
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND nh.collection_time > DATE_ADD(NOW(), INTERVAL -1 DAY)
    AND o.company IN %s
    AND la.did = ld.id
    AND la.type = %s
    AND al.iid = la.id
GROUP BY
    nh.did
ORDER BY
    nh.avg_data DESC
LIMIT
    5;