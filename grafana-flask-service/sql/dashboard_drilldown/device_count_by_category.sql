SELECT
    o.company AS Organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS 'Device Location',
    la.make AS Vendor
FROM
    master_dev.legend_device ld,
    master_biz.organizations o,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.legend_asset la,
    master_biz.asset_location al
WHERE
    la.did = ld.id
    AND (ld.roa_id = o.roa_id)
    AND o.company IN %s
    AND (ld.class_type = dcl.class_type)
    AND (dca.Fid = dcl.family)
    AND (al.iid = la.id)
ORDER BY
    la.type