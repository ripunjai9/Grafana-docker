SELECT
    IF(
        al.location IS NULL
        OR al.location = '',
        'NIL',
        al.location
    ) AS Location,
    IF(
        la.type IS NULL
        OR la.type = '',
        'NIL',
        la.type
    ) AS Category,
    count(ld.id) AS L_count
FROM
    master_dev.legend_device ld,
    master_biz.organizations o,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.legend_asset la
    INNER JOIN master_biz.asset_location al ON (la.id = al.iid)
WHERE
    la.did = ld.id
    AND al.iid = la.id
    AND ld.roa_id = o.roa_id
    AND ld.class_type = dcl.class_type
    AND dca.Fid = dcl.family
    AND o.company IN %s
GROUP BY
    Category,
    Location