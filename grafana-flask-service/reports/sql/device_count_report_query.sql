SELECT
    o.company AS Organization,
    dca.cat_name AS 'Device Category',
    la.type AS 'Device Type',
    CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    COUNT(ld.id) AS Device_Count
FROM
    master_dev.legend_device ld,
    master_biz.organizations o,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.legend_asset la
WHERE
    (ld.roa_id = o.roa_id)
    AND (ld.class_type = dcl.class_type)
    AND (dca.Fid = dcl.family)
    AND la.did = ld.id
    AND o.company IN %s
    AND ld.device IN %s
GROUP BY
    o.company,
    dcl.class asc
ORDER BY
    la.type asc