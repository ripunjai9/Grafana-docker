SELECT
    o.company AS organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    Concat(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS 'Device Location',
    la.make AS vendor,
    Concat(Round(nh.avg_data, 2), '', '%%') AS 'Memory Utilization Value'
FROM
    NET_SNMP_PHYSICAL_MEMORY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (
        ld.class_type = dcl.class_type
    )
    LEFT JOIN master.definitions_dev_cats dca ON (dca.fid = dcl.family),
    master_biz.legend_asset la,
    master_biz.asset_location al
WHERE
    nh.pres_id = PHYSICAL_MEMORY_UTILIZATION_PID
    AND nh.collection_time > date_add(Now(), interval -1 day)
    AND o.company IN %s
    AND la.did = ld.id
    AND la.type = %s
    AND al.iid = la.id
GROUP BY
    nh.did
ORDER BY
    nh.max_data DESC
limit
    5