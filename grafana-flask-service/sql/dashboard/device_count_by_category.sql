SELECT
    now() AS time,
    COUNT(ld.id) AS value,
    IF(
        la.type IS NULL
        OR la.type = '',
        'NIL',
        la.type
    ) AS metric
FROM
    master_dev.legend_device ld,
    master_biz.organizations o,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.legend_asset la
WHERE
    (ld.roa_id = o.roa_id)
    AND o.company IN %s
    AND (ld.class_type = dcl.class_type)
    AND (dca.Fid = dcl.family)
    AND (ld.id = la.did)
GROUP BY
    la.type