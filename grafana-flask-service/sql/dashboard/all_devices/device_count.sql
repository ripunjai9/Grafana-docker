SELECT
    COUNT(ld.id) AS 'Total Device Count'
FROM
    master_biz.organizations o,
    master_dev.legend_device ld
WHERE
    (ld.roa_id = o.roa_id)
    AND o.company IN %s