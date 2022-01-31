SELECT
  o.company AS Organization,
  ld.device AS 'Device Name',
  ld.ip AS 'Device IP',
  Substring_index(dca.cat_name, '.', 1) AS 'Device Category',
  la.type AS 'Device Type',
  Concat(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
  al.location AS 'Device Location',
  la.make AS Vendor,
  IF(
    issuer LIKE '%%/O=%%',
    Substring_index(Substring_index(issuer, '/O=', -1), '/', 1),
    'Not Specified'
  ) as 'Certificate Organization',
  concat('( ', dc.cert_id, '', ' )') 'Cert ID',
  dc.expires AS 'Expiration Date',
  datediff(dc.expires, now()) AS 'Days Left'
FROM
  master_dev.device_certificates dc
  LEFT JOIN master_dev.legend_device ld ON (ld.id = dc.did)
  LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
  LEFT JOIN master.definitions_dev_cats dca ON (dca.fid = dcl.family)
  LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
  LEFT JOIN master_biz.legend_asset la ON (la.did = ld.id)
  LEFT JOIN master_biz.asset_location al ON (al.iid = la.id)
WHERE
  la.type = %s
  AND o.company IN %s
  AND dc.expires >= now()
  AND dc.expires < now() + interval 3 month
ORDER BY
  'Expiration Date' ASC