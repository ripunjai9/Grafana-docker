SELECT
    ld.Device as device,
    la.did as id,
    CONCAT(la.make, ' | ', la.model) as Device_Class,
    dca.cat_name as Device_Category,
    dsd.sysdescr as Device_Description,
    scg.cug_name as CUG,
    if (ea.Xtype = 1, 'Physical Device', 'Organization') as 'Managed_Type',
    IF (ld.port_scan = 1, 'Y', 'N') as Port_scan,
    ld.create_date as Creation_date,
    IF(ld.Active = 2, 'Y', 'N') as Active,
    ld.ip as IP_address
from
    master_dev.legend_device ld
    left join master.definitions_dev_classes dcl on (ld.class_type = dcl.class_type)
    left join master.definitions_dev_cats dca on (dca.Fid = dcl.family)
    left join master_biz.legend_asset la on (la.did = ld.id)
    left join master.system_collector_groups scg on(ld.cug_id = scg.cug_id)
    left join master_dev.device_snmp_data dsd on (dsd.did = ld.id)
    left join master_events.events_active ea on (ea.Xid = ld.id)
where
    ld.device IN %s

===next===

SELECT
    ld.device as device,
    avg(nh.avg_data) AS "CPU %% Used",
    avg(nh.max_data) AS "CPU %% Peak"
FROM
    master_dev.legend_device ld,
    NET_SNMP_CPU_DID.normalized_daily nh,
    master_biz.organizations o
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND nh.did = ld.id
    AND o.company IN %s
    and ld.device in %s
    AND nh.collection_time BETWEEN %s
    AND %s
group by
    ld.id;

===next===

SELECT
    ld.device as device,
    avg(nh.avg_data) AS "RAM %% Used",
    avg(nh.max_data) AS "RAM %% Peak"
FROM
    master_dev.legend_device ld,
    NET_SNMP_PHYSICAL_MEMORY_DID.normalized_daily nh,
    master_biz.organizations o
WHERE
    nh.pres_id = PHYSICAL_MEMORY_UTILIZATION_PID
    AND nh.did = ld.id
    AND o.company IN %s
    and ld.device in %s
    AND nh.collection_time BETWEEN %s
    AND %s
group by
    ld.id;

===next===

SELECT
    ld.device as device,
    avg(nh.avg_data) AS "SWAP %% Used",
    avg(nh.max_data) AS "SWAP %% Peak"
FROM
    master_dev.legend_device ld,
    NET_SNMP_SWAP_DID.normalized_daily nh,
    master_biz.organizations o
WHERE
    nh.pres_id = SWAP_UTILIZATION_PID
    AND nh.did = ld.id
    AND o.company IN %s
    and ld.device IN %s
    AND nh.collection_time BETWEEN %s AND %s
group by ld.id;

===next===

select
    ld.device as device,
    avg(nd.avg_d_check) * 100 as "Availability",
    avg(nd.avg_d_latency) as "Latency (ms)"
from
    data_avail.normalized_daily nd,
    master_dev.legend_device ld,
    master_biz.organizations o
where
    ld.roa_id = o.roa_id
    AND nd.did = ld.id
    AND o.company IN %s
    and ld.device IN %s
    and nd.collection_time BETWEEN %s
    AND %s
group by
    ld.id;

===next=== 
SELECT
    ld.device as device,
    md.port_num as open_ports
from
    master_dev.device_ports md,
    master_dev.legend_device ld
where
    ld.device IN %s
    AND md.did = ld.id

===next===

select
    ld.device as device,
    la.make as make,
    la.model as model,
    la.asset_tag as asset_tag,
    la.serial as serial,
    la.`type` as asset_type,
    ac.hostid as host_id,
    ac.dns_name as dns_name,
    ac.dns_domain as dns_domain,
    ac.fw_ver as firmware_version,
    ac.dsk_count as disk_count,
    ac.dsk_size as disk_size,
    ac.array_size as disk_array_size,
    ac.hostname as Host_name,
    ac.os as Operating_System,
    la.function
from
    master_dev.legend_device ld
    left join master_biz.legend_asset la on (la.did = ld.id)
    left join master_biz.asset_configuration ac on(ac.iid = ld.iid)
where
    ld.device IN %s

===next===

select
    ld.device as device,
    dh.name as File_system,
    dh.value0 as Size,
    dh.value2 as Space_Used,
    dh.value0 - dh.value2 as Space_Available,
    dh.value4 as 'Used%%'
from
    master_dev.device_hardware dh,
    master_dev.legend_device ld
where
    dh.did = ld.id
    AND ld.device IN %s


===next===

SELECT
    ld.device as device,
    concat(
        YEAR(nh.collection_time),
        '-',
        MONTH(nh.collection_time)
    ) as month_year,
    avg(nh.avg_data) AS "CPU%% AVG"
FROM
    NET_SNMP_CPU_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND o.company IN %s
    AND ld.device IN %s
    AND nh.collection_time BETWEEN %s
    AND %s
GROUP BY
    id,
    month_year
Order by
    id,
    nh.collection_time

===next===

select
    ld.device As deviceName,
    concat(
        YEAR(nd.collection_time),
        '-',
        MONTH(nd.collection_time)
    ) as month_year,
    avg(avg_d_check) * 100 as Availability_chart
from
    data_avail.normalized_daily nd,
    master_dev.legend_device ld,
    master_biz.organizations o,
    master_biz.legend_asset la
where
    ld.roa_id = o.roa_id
    AND la.did = ld.id
    AND o.company IN %s
    AND ld.device IN %s
    AND nd.did = ld.id
    AND nd.collection_time BETWEEN %s
    AND %s
group by
    ld.device,
    month_year
Order by
    la.did,
    nd.collection_time


===next===

SELECT
    ld.device as device,
    concat(
        YEAR(nh.collection_time),
        '-',
        MONTH(nh.collection_time)
    ) as month_year,
    avg(nh.avg_data) AS "Mem %% AVG"
FROM
    NET_SNMP_PHYSICAL_MEMORY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = PHYSICAL_MEMORY_UTILIZATION_PID
    AND o.company IN %s
    AND ld.device IN %s
    AND nh.collection_time BETWEEN %s
    AND %s
GROUP BY
    nh.did,
    month_year
ORDER BY
    nh.did,
    nh.collection_time

===next===

SELECT
    ld.device AS device,
    concat(
        YEAR(nh.collection_time),
        '-',
        MONTH(nh.collection_time)
    ) as month_year,
    avg(nh.avg_data) AS "Swap %% AVG"
FROM
    NET_SNMP_SWAP_DID.normalized_daily nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = SWAP_UTILIZATION_PID
    AND o.company IN %s
    AND ld.device IN %s
    AND nh.collection_time BETWEEN %s
    AND %s
GROUP BY
    nh.did,
    month_year
ORDER BY
    nh.did,
    nh.collection_time