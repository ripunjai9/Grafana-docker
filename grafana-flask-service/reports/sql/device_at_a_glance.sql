SELECT
    ld.device AS Device,
    ld.id AS id,
    min(nh.min_data) AS "CPU %% Min",
    avg(nh.avg_data) AS "CPU %% AVG",
    max(nh.max_data) AS "CPU %% Max"
FROM
    NET_SNMP_CPU_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = OVERALL_CPU_PID
    AND nh.collection_time BETWEEN %s
    AND %s
    AND o.company IN %s
    AND ld.device IN %s
GROUP BY
    ld.device
ORDER BY
    nh.did

===next===

SELECT
    ld.device AS Device,
    ld.id AS id,
    min(nh.min_data) AS "Mem %% Min",
    avg(nh.avg_data) AS "Mem %% AVG",
    max(nh.max_data) AS "Mem %% Peak"
FROM
    NET_SNMP_PHYSICAL_MEMORY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = PHYSICAL_MEMORY_UTILIZATION_PID
    AND nh.collection_time BETWEEN %s
    AND %s
    AND o.company IN %s
    AND ld.device IN %s
GROUP BY
    ld.device
ORDER BY
    nh.did

===next===

SELECT
    ld.device AS Device,
    ld.id AS id,
    MIN(nh.min_data) AS 'Swap %% MIN',
    avg(nh.avg_data) AS 'Swap %% AVG',
    MAX(nh.max_data) AS 'Swap %% MAX'
FROM
    NET_SNMP_SWAP_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
WHERE
    nh.pres_id = SWAP_UTILIZATION_PID
    AND nh.collection_time BETWEEN %s
    AND %s
    AND o.company IN %s
    AND ld.device IN %s
GROUP BY
    ld.device


===next===


SELECT
    ld.device AS deviceName,
    ld.id AS id,
    avg(avg_d_check) * 100 AS Availability
FROM
    data_avail.normalized_hourly nd,
    master_dev.legend_device ld,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_biz.organizations o,
    master_biz.legend_asset la
WHERE
    ld.roa_id = o.roa_id
    AND nd.collection_time BETWEEN %s
    AND %s
    AND o.company IN %s
    AND ld.class_type = dcl.class_type
    AND dca.Fid = dcl.family
    AND la.did = ld.id
    AND nd.did = ld.id
    AND ld.device IN %s
GROUP BY
    ld.device

===next===

SELECT
    ec.Xname AS Device_Name,
    ec.Xid AS DID,
    concat(
        YEAR(ec.date_first),
        '-',
        MONTH(ec.date_first)
    ) AS month_year,
    count(*) AS Scheduled_outage_Count
FROM
    master_events.events_cleared ec,
    scheduler.tasks t,
    scheduler.schedules s
WHERE
    alert_id IN (267)
    AND (t.Xid = ec.Xid)
    AND (s.schedule_id = t.task_id)
    AND t.Xid IN (
        SELECT
            Xid
        FROM
            scheduler.tasks t
    )
    AND ec.Xname IN %s
    AND ec.date_first BETWEEN %s
    AND %s
    AND t.last_run BETWEEN %s
    AND %s
GROUP BY
    ec.Xname,
    month_year
ORDER BY
    ec.date_first

===next===

SELECT
    ec.Xname AS Device_Name,
    ec.Xid AS DID,
    concat(
        YEAR(ec.date_first),
        '-',
        MONTH(ec.date_first)
    ) AS month_year,
    count(*) AS Unscheduled_outage_Count
FROM
    master_events.events_cleared ec,
    scheduler.tasks t,
    scheduler.schedules s
WHERE
    alert_id IN (267)
    AND (t.Xid != ec.Xid)
    AND (s.schedule_id != t.task_id)
    AND t.Xid IN (
        SELECT
            Xid
        FROM
            scheduler.tasks t
    )
    AND ec.Xname IN %s
    AND ec.date_first BETWEEN %s
    AND %s
    AND t.last_run BETWEEN %s
    AND %s
GROUP BY
    ec.Xname,
    month_year
ORDER BY
    ec.date_first