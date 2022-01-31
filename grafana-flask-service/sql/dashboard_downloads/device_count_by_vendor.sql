SELECT
    o.company AS organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    Concat(dcl.class, ' | ', dcl.descript) AS 'Device Class | SubClass',
    al.location AS 'Device Location',
    la.make AS vendor
FROM
    master_dev.legend_device ld,
    master_biz.organizations o,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.legend_asset la,
    master_biz.asset_location al
WHERE
    la.did = ld.id
    AND al.iid = la.id
    AND ld.roa_id = o.roa_id
    AND ld.class_type = dcl.class_type
    AND dca.fid = dcl.family
    AND o.company IN %s
ORDER BY
    la.make ASC;