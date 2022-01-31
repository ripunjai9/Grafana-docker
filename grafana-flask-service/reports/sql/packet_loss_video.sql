SELECT
    nh.collection_time as time,
    nh.avg_data,
    concat('videoRX', ' [', nh.ind, ']')
FROM
    POLYCOM_GS_CALL_QUALITY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family)
WHERE
    nh.pres_id = VIDEO_PACKET_LOSS_RX_PID
    AND ld.device = %s
    AND nh.collection_time BETWEEN %s
    AND %s 

===next===

SELECT
    nh.collection_time as time,
    nh.avg_data,
    concat('videoTX', ' [', nh.ind, ']')
FROM
    POLYCOM_GS_CALL_QUALITY_DID.normalized_hourly nh
    LEFT JOIN master_dev.legend_device ld ON (nh.did = ld.id)
    LEFT JOIN master_biz.organizations o ON (ld.roa_id = o.roa_id)
    LEFT JOIN master.definitions_dev_classes dcl ON (ld.class_type = dcl.class_type)
    LEFT JOIN master.definitions_dev_cats dca ON (dca.Fid = dcl.family)
WHERE
    nh.pres_id = VIDEO_PACKET_LOSS_TX_PID
    AND ld.device = %s
    AND nh.collection_time BETWEEN %s
    AND %s