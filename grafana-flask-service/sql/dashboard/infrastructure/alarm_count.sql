SELECT
    Count(*) AS 'Alarm Count',
    dca.cat_name AS DeviceCategory,
    CONCAT(dcl.class, ' | ', dcl.descript) AS Device_class_subClass,
    o.company AS Organization
FROM
    master_dev.legend_device ld,
    master_biz.organizations o,
    master.definitions_dev_classes dcl,
    master.definitions_dev_cats dca,
    master_events.events_active ea,
    master_biz.legend_asset la
WHERE
    (ld.roa_id = o.roa_id)
    AND (ld.class_type = dcl.class_type)
    AND (dca.Fid = dcl.family)
    AND (ld.id = ea.Xid)
    AND o.company IN %s
    AND la.type = %s
    AND la.did = ld.id
    AND ea.eseverity IN ('4', '3', '2', '1')