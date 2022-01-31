SELECT
    o.company AS Organization,
    ld.device AS 'Device Name',
    ld.ip AS 'Device IP',
    SUBSTRING_INDEX(dca.cat_name, ".", 1) AS 'Device Category',
    la.type AS 'Device Type',
    CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
    al.location AS 'Device Location',
    la.make AS Vendor,
    IF(
        issuer LIKE '%%/O=%%',
        SUBSTRING_INDEX(SUBSTRING_INDEX(issuer, '/O=', -1), '/', 1),
        'Not Specified'
    ) AS 'Certificate Organization',
    CONCAT('( ', dc.cert_id, '', ' )') 'Cert ID',
    dc.expires AS 'Expiration Date',
    DATEDIFF(dc.expires, NOW()) AS 'Days Left'
FROM
    master_dev.device_certificates dc
    LEFT JOIN master_dev.legend_device ld ON (ld.id = dc.did)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master_biz.legend_asset la ON (la.did = ld.id)
    LEFT JOIN master_biz.asset_location al ON (al.iid = la.id)
WHERE
    o.company IN %s
    AND la.type = %s
    AND dc.expires >= Now()
    AND dc.expires < NOW() + INTERVAL 3 MONTH
ORDER BY
    'Expiration Date' asc