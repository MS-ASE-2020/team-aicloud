# Sequence
![](assets/sequence.svg)

1. 13, 16 提交series的feature, model, hyper_param: `/job/job_id/` PATCH 

    Content-Type: application/json
    ```text
    [{"model_name": "LinearFit","hyper_params":{},"ts_id": 1700,"feature_indexs": "[1, 2]"}]
    ```

2. 9 提交job的ts, group_by, target设置: `/job/job_id/` PUT
   index名称参见swagger
3. 查看ts可用的features, groupby_key, groupby_val
   ```
   {
    "features": [],
    "ts_details": [
        {
            "ts_id": 1,
            "groupby_val": "('asiasoutheast', 'FS')",
            "groupby_key": [
                "Region",
                "VMSeries"
            ]
        },
        {
            "ts_id": 2,
            "groupby_val": "('ussouth', 'A')",
            "groupby_key": [
                "Region",
                "VMSeries"
            ]
        }
    ]
   ```
4. 数据集header和预览数据: `/data/data_id/` GET
   ```json
   {
    "data": {
        "id": 2,
        "name": "test_dataset",
        "uuid": "13740a08-1edd-49be-8d3f-1784e79a8e1d",
        "time_created": "2020-11-09T14:52:53.002395+08:00",
        "upload": "/uploads/allRegion_37d_MSDN_vmlevel.csv",
        "related_user": 1
    },
    "header": [
        {
            "index": 0,
            "label": "Region"
        },
        {
            "index": 1,
            "label": "VMSeries"
        },
        {
            "index": 2,
            "label": "ObjectTime"
        },
        {
            "index": 3,
            "label": "sum_PeakDailyCores"
        }
    ],
    "status": 200,
    "heads": {
        "Region": [
            "asiasoutheast",
            "ussouth",
            "ussouth",
            "europewest",
            "asiasoutheast"
        ],
        "VMSeries": [
            "FS",
            "A",
            "D",
            "B",
            "B"
        ],
        "ObjectTime": [
            "2020-08-01 00:00:00.0000000",
            "2020-08-01 00:00:00.0000000",
            "2020-08-01 00:00:00.0000000",
            "2020-08-01 00:00:00.0000000",
            "2020-08-01 00:00:00.0000000"
        ],
        "sum_PeakDailyCores": [
            152,
            1377,
            234,
            11912,
            3866
        ]
    }   
    ```