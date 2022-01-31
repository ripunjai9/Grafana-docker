SELECT
        o.company AS Organization,
        ld.device AS 'Device Name',
        dca.cat_name AS 'Device Category',
        la.type AS 'Device Type',
        if(
                last_read_uptime is null
                OR last_read_uptime = '',
                'down',
                dsd.last_read_uptime / 100
        ) AS 'Uptime',
        dsd.last_read_uptime AS Timetick,
        '' AS 'Up Since',
        Last_poll AS LastPolled
FROM
        master_dev.legend_device ld,
        master_biz.organizations o,
        master_dev.device_snmp_data dsd,
        master.definitions_dev_cats dca,
        master_biz.legend_asset la
WHERE
        (ld.roa_id = o.roa_id)
        AND (ld.id = dsd.did)
        AND la.did = ld.id
        AND o.company IN %s
        AND ld.device IN %s
GROUP BY
        ld.device