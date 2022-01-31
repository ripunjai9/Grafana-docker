SELECT
    org.company AS Organization,
    e_ac.Xname AS "Device Name",
    ld.ip AS "Device IP",
    dca.cat_name AS "Device Category",
    la.type AS "Device Type",
    CONCAT(dcl.class, ' | ', dcl.descript) AS "Device Class | Sub Class",
    al.location AS 'Device Location',
    la.make AS Vendor,
    e_ac.emessage AS "Event Message",
    CASE
        WHEN e_ac.eseverity = 0 THEN 'Healthy'
        WHEN e_ac.eseverity = 1 THEN 'Notice'
        WHEN e_ac.eseverity = 2 THEN 'Minor'
        WHEN e_ac.eseverity = 3 THEN 'Major'
        WHEN e_ac.eseverity = 4 THEN 'Critical'
        ELSE 'Severity Not Found'
    END AS ESeverity,
    e_ac.date_last AS "Last Detected"
FROM
    master_dev.legend_device AS ld
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family)
    LEFT JOIN master_dev.device_state dst ON (dst.did = ld.id)
    LEFT JOIN master_biz.legend_asset la ON (la.did = ld.id),
    master_events.events_active AS e_ac,
    master_biz.organizations AS org,
    master_biz.asset_location al
WHERE
    e_ac.Xname = ld.device
    AND ld.roa_id = org.roa_id
    AND org.company IN %s
    AND al.iid = la.id
    AND e_ac.eseverity != 0
    AND e_ac.Xname IN (
        SELECT
            *
        FROM
            (
                SELECT
                    e_ac.Xname
                FROM
                    master_dev.legend_device AS ld,
                    master_events.events_active AS e_ac,
                    master_biz.organizations AS org
                WHERE
                    e_ac.Xname = ld.device
                    AND ld.roa_id = org.roa_id
                    AND org.company IN %s
                    AND e_ac.eseverity != 0
                GROUP BY
                    e_ac.Xname
                ORDER BY
                    count(e_ac.Xname) DESC
                limit
                    10
            ) temp_tab
    )
ORDER BY
    e_ac.Xname ASC