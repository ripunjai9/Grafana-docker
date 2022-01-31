SELECT
    temp.*
FROM
    (
        SELECT
            CAST(la.id AS CHAR) AS 'Asset',
            o.company AS Organization,
            ld.device AS Device,
            ld.ip AS 'Device IP',
            dca.cat_name AS 'Device Category',
            la.type AS 'Device Type',
            CONCAT(dcl.class, ' | ', dcl.descript) AS 'Device Class | Sub Class',
            al.location AS 'Device Location',
            la.make AS 'Make (Vendor)',
            la.model AS Model,
            la.serial AS 'Serial Number',
            ac.fw_ver AS 'Firmware Verison',
            ac.os AS 'Operating System',
            ac.memory AS 'RAM (Installed Memory)',
            ac.speed AS 'CPU Speed'
        FROM
            master_dev.legend_device ld,
            master_biz.organizations o,
            master.definitions_dev_classes dcl,
            master.definitions_dev_cats dca,
            master_biz.legend_asset la,
            master_biz.asset_location al,
            master_biz.asset_configuration ac
        WHERE
            la.did = ld.id
            AND al.iid = la.id
            AND la.id = ac.iid
            AND ld.roa_id = o.roa_id
            AND ld.class_type = dcl.class_type
            AND dca.Fid = dcl.family
            AND o.company IN %s
    ) temp
WHERE
    temp.Device IN %s