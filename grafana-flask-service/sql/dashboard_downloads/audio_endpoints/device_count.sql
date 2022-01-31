SELECT
    o.company AS organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    Concat(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS 'Device Location',
    la.make AS vendor
FROM
    master_dev.legend_device ld
    INNER JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    INNER JOIN master.definitions_dev_classes dcl ON (
        ld.class_type = dcl.class_type
    )
    INNER JOIN master.definitions_dev_cats dca ON (dca.fid = dcl.family)
    INNER JOIN master_biz.legend_asset la ON (la.did = ld.id),
    master_biz.asset_location al
WHERE
    la.type = %s
    AND o.company IN %s
    AND al.iid = la.id
ORDER BY
    device,
    la.type ASC