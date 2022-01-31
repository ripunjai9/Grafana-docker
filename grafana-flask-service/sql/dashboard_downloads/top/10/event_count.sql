SELECT
       org.company AS organization,
       e_ac.xname AS 'Device Name',
       ld.ip AS 'Device IP',
       dca.cat_name AS 'Device Category',
       la.type AS 'Device Type',
       Concat(dcl.class, ' | ', dcl.descript) AS 'Device Class Sub Class',
       al.location AS 'Device Location',
       la.make AS vendor,
       e_ac.emessage AS 'Event Message',
       CASE
              WHEN dst.state = 0 THEN 'Healthy'
              WHEN dst.state = 1 THEN 'Notice'
              WHEN dst.state = 2 THEN 'Minor'
              WHEN dst.state = 3 THEN 'Major'
              WHEN dst.state = 4 THEN 'Critical'
              ELSE 'Severity Not Found'
       END AS eseverity,
       e_ac.date_last AS 'Last Detected'
FROM
       master_dev.legend_device AS ld
       LEFT JOIN master.definitions_dev_classes dcl ON (
              ld.class_type = dcl.class_type
       )
       LEFT JOIN master.definitions_dev_cats dca ON (dca.fid = dcl.family)
       LEFT JOIN master_dev.device_state dst ON (dst.did = ld.id)
       LEFT JOIN master_biz.legend_asset la ON (la.did = ld.id),
       master_events.events_active AS e_ac,
       master_biz.asset_location al,
       master_biz.organizations AS org
WHERE
       e_ac.xname = ld.device
       AND ld.roa_id = org.roa_id
       AND org.company IN %s
       AND al.iid = la.id
       AND e_ac.eseverity != 0
       AND e_ac.emessage IN (
              SELECT
                     *
              FROM
                     (
                            SELECT
                                   e_ac.emessage
                            FROM
                                   master_dev.legend_device AS ld,
                                   master_events.events_active AS e_ac,
                                   master_biz.organizations AS org
                            WHERE
                                   e_ac.xname = ld.device
                                   AND (
                                          ld.roa_id = org.roa_id
                                   )
                                   AND e_ac.eseverity != 0
                                   AND org.company IN %s
                            GROUP BY
                                   e_ac.emessage
                            ORDER BY
                                   count(e_ac.emessage) DESC
                            limit
                                   10
                     ) temp_tab
       )
ORDER BY
       e_ac.emessage