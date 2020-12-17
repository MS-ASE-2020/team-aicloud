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
5. 模型初始化以及发出训练请求 /job/job_id/ PATCH

不需要调参的请求格式
```json
[
    {
        "model_name": "LinearFit",
        "max_eval": 100,            // 调参搜索的次数
        "next_k_prediction": 5,     // 预测的ts的天数
        "auto_tune": 0,             // 0为不调参
        "eval_metrics":["mse", "rmse"], 
        "hyper_params":[
            {
                "name": "latest_n", 
                "type": "int",
                "val": 5
            },
            {
                "name": "add_std_factor",
                "type": "float",
                "val": 0.5
            }
        ],
        "ts_id": 8797,
        "feature_indexs": "[]"
    }
]
```
需要调参的请求格式
```json
[
    {
        "model_name": "LinearFit",
        "max_eval": 100,
        "next_k_prediction": 5,
        "auto_tune": 1, 
        "eval_metrics":["mse", "rmse"], 
        "hyper_params":[
            {
                "name": "latest_n", 
                "type": "int",
                "low": 1,
                "high": 5
            },
            {
                "name": "add_std_factor",
                "type": "float",
                "low": 0,
                "high": 0.5
            }
        ],
        "ts_id": 8797,
        "feature_indexs": "[]"
    }
]
```

对于是选项的参数
```json
{
    "name": "strategy",
    "type": "list",
    "choice": []
}
```
可选的metrics
```
METRICS = {
    "mse": mse,
    "rmse": rmse,
    "nrmse": nrmse,
    "me": me,
    "mae": mae,
    "mad": mad,
    "gmae": gmae,
    "mdae": mdae,
    "mpe": mpe,
    "mape": mape,
    "mdape": mdape,
    "smape": smape,
    "smdape": smdape,
    "maape": maape,
    "mase": mase,
    "std_ae": std_ae,
    "std_ape": std_ape,
    "rmspe": rmspe,
    "rmdspe": rmdspe,
    "rmsse": rmsse,
    "inrse": inrse,
    "rrse": rrse,
    "mre": mre,
    "rae": rae,
    "mrae": mrae,
    "mdrae": mdrae,
    "gmrae": gmrae,
    "mbrae": mbrae,
    "umbrae": umbrae,
    "mda": mda,
    "bias": bias,
    "r2": r2_score,
}
```
6. get results: job/job_id/job_results/
如果已经执行完毕:
```json
{
    "status": 3,
    "results": [
        {
            "ts_id": 1,
            "results": [
                {
                    "predictions": [
                        234.0,
                        237.0,
                        235.0,
                        233.0,
                        235.0
                    ],
                    "timestamps": [
                        "2020-09-08 00:00:00",
                        "2020-09-09 00:00:00",
                        "2020-09-10 00:00:00",
                        "2020-09-11 00:00:00",
                        "2020-09-12 00:00:00"
                    ],
                    "metrics": {
                        "mse": 110.2,
                        "rmse": 10.497618777608569
                    },
                    "config": {
                        "batch_size_used": 8.0,
                        "epochs_used": 145.0,
                        "loss_used": 0,
                        "lstm_cells_per_layer_used": 6.0,
                        "sample_fold_used": 4.0
                    },
                    "ts_id": 1,
                    "model_name": "LstmLong",
                    "ts_history": {
                        "sum_PeakDailyCores": [
                            227,
                            246,
                            247,
                            249,
                            255,
                            249,
                            246,
                            228,
                            246,
                            246,
                            245,
                            249,
                            235,
                            233,
                            224,
                            230,
                            261,
                            238,
                            242,
                            266,
                            258,
                            226,
                            233,
                            242,
                            236,
                            236,
                            233,
                            260,
                            219,
                            230,
                            235,
                            237,
                            226,
                            227,
                            226,
                            221,
                            222,
                            227
                        ],
                        "ObjectTime": [
                            "8/1/2020",
                            "8/2/2020",
                            "8/3/2020",
                            "8/4/2020",
                            "8/5/2020",
                            "8/6/2020",
                            "8/7/2020",
                            "8/8/2020",
                            "8/9/2020",
                            "8/10/2020",
                            "8/11/2020",
                            "8/12/2020",
                            "8/13/2020",
                            "8/14/2020",
                            "8/15/2020",
                            "8/16/2020",
                            "8/17/2020",
                            "8/18/2020",
                            "8/19/2020",
                            "8/20/2020",
                            "8/21/2020",
                            "8/22/2020",
                            "8/23/2020",
                            "8/24/2020",
                            "8/25/2020",
                            "8/26/2020",
                            "8/27/2020",
                            "8/28/2020",
                            "8/29/2020",
                            "8/30/2020",
                            "8/31/2020",
                            "9/1/2020",
                            "9/2/2020",
                            "9/3/2020",
                            "9/4/2020",
                            "9/5/2020",
                            "9/6/2020",
                            "9/7/2020"
                        ]
                    }
                },
                {
                    "predictions": [
                        237.0,
                        237.0,
                        237.0,
                        237.0,
                        237.0
                    ],
                    "timestamps": [
                        "2020-09-08 00:00:00",
                        "2020-09-09 00:00:00",
                        "2020-09-10 00:00:00",
                        "2020-09-11 00:00:00",
                        "2020-09-12 00:00:00"
                    ],
                    "metrics": {
                        "mse": 160.4,
                        "rmse": 12.66491215919005
                    },
                    "config": {
                        "latest_n": 5
                    },
                    "ts_id": 1,
                    "model_name": "AdaptiveMaxN",
                    "ts_history": {
                        "sum_PeakDailyCores": [
                            227,
                            246,
                            247,
                            249,
                            255,
                            249,
                            246,
                            228,
                            246,
                            246,
                            245,
                            249,
                            235,
                            233,
                            224,
                            230,
                            261,
                            238,
                            242,
                            266,
                            258,
                            226,
                            233,
                            242,
                            236,
                            236,
                            233,
                            260,
                            219,
                            230,
                            235,
                            237,
                            226,
                            227,
                            226,
                            221,
                            222,
                            227
                        ],
                        "ObjectTime": [
                            "8/1/2020",
                            "8/2/2020",
                            "8/3/2020",
                            "8/4/2020",
                            "8/5/2020",
                            "8/6/2020",
                            "8/7/2020",
                            "8/8/2020",
                            "8/9/2020",
                            "8/10/2020",
                            "8/11/2020",
                            "8/12/2020",
                            "8/13/2020",
                            "8/14/2020",
                            "8/15/2020",
                            "8/16/2020",
                            "8/17/2020",
                            "8/18/2020",
                            "8/19/2020",
                            "8/20/2020",
                            "8/21/2020",
                            "8/22/2020",
                            "8/23/2020",
                            "8/24/2020",
                            "8/25/2020",
                            "8/26/2020",
                            "8/27/2020",
                            "8/28/2020",
                            "8/29/2020",
                            "8/30/2020",
                            "8/31/2020",
                            "9/1/2020",
                            "9/2/2020",
                            "9/3/2020",
                            "9/4/2020",
                            "9/5/2020",
                            "9/6/2020",
                            "9/7/2020"
                        ]
                    }
                },
                {
                    "predictions": [
                        237.0,
                        237.0,
                        237.0,
                        237.0,
                        237.0
                    ],
                    "timestamps": [
                        "2020-09-08 00:00:00",
                        "2020-09-09 00:00:00",
                        "2020-09-10 00:00:00",
                        "2020-09-11 00:00:00",
                        "2020-09-12 00:00:00"
                    ],
                    "metrics": {
                        "mse": 160.4,
                        "rmse": 12.66491215919005
                    },
                    "config": {
                        "latest_n": 5
                    },
                    "ts_id": 1,
                    "model_name": "AdaptiveMaxN",
                    "ts_history": {
                        "sum_PeakDailyCores": [
                            227,
                            246,
                            247,
                            249,
                            255,
                            249,
                            246,
                            228,
                            246,
                            246,
                            245,
                            249,
                            235,
                            233,
                            224,
                            230,
                            261,
                            238,
                            242,
                            266,
                            258,
                            226,
                            233,
                            242,
                            236,
                            236,
                            233,
                            260,
                            219,
                            230,
                            235,
                            237,
                            226,
                            227,
                            226,
                            221,
                            222,
                            227
                        ],
                        "ObjectTime": [
                            "8/1/2020",
                            "8/2/2020",
                            "8/3/2020",
                            "8/4/2020",
                            "8/5/2020",
                            "8/6/2020",
                            "8/7/2020",
                            "8/8/2020",
                            "8/9/2020",
                            "8/10/2020",
                            "8/11/2020",
                            "8/12/2020",
                            "8/13/2020",
                            "8/14/2020",
                            "8/15/2020",
                            "8/16/2020",
                            "8/17/2020",
                            "8/18/2020",
                            "8/19/2020",
                            "8/20/2020",
                            "8/21/2020",
                            "8/22/2020",
                            "8/23/2020",
                            "8/24/2020",
                            "8/25/2020",
                            "8/26/2020",
                            "8/27/2020",
                            "8/28/2020",
                            "8/29/2020",
                            "8/30/2020",
                            "8/31/2020",
                            "9/1/2020",
                            "9/2/2020",
                            "9/3/2020",
                            "9/4/2020",
                            "9/5/2020",
                            "9/6/2020",
                            "9/7/2020"
                        ]
                    }
                },
                {
                    "predictions": [
                        237.0,
                        237.0,
                        237.0,
                        237.0,
                        237.0
                    ],
                    "timestamps": [
                        "2020-09-08 00:00:00",
                        "2020-09-09 00:00:00",
                        "2020-09-10 00:00:00",
                        "2020-09-11 00:00:00",
                        "2020-09-12 00:00:00"
                    ],
                    "metrics": {
                        "mse": 160.4,
                        "rmse": 12.66491215919005
                    },
                    "config": {
                        "latest_n": 5
                    },
                    "ts_id": 1,
                    "model_name": "AdaptiveMaxN",
                    "ts_history": {
                        "sum_PeakDailyCores": [
                            227,
                            246,
                            247,
                            249,
                            255,
                            249,
                            246,
                            228,
                            246,
                            246,
                            245,
                            249,
                            235,
                            233,
                            224,
                            230,
                            261,
                            238,
                            242,
                            266,
                            258,
                            226,
                            233,
                            242,
                            236,
                            236,
                            233,
                            260,
                            219,
                            230,
                            235,
                            237,
                            226,
                            227,
                            226,
                            221,
                            222,
                            227
                        ],
                        "ObjectTime": [
                            "8/1/2020",
                            "8/2/2020",
                            "8/3/2020",
                            "8/4/2020",
                            "8/5/2020",
                            "8/6/2020",
                            "8/7/2020",
                            "8/8/2020",
                            "8/9/2020",
                            "8/10/2020",
                            "8/11/2020",
                            "8/12/2020",
                            "8/13/2020",
                            "8/14/2020",
                            "8/15/2020",
                            "8/16/2020",
                            "8/17/2020",
                            "8/18/2020",
                            "8/19/2020",
                            "8/20/2020",
                            "8/21/2020",
                            "8/22/2020",
                            "8/23/2020",
                            "8/24/2020",
                            "8/25/2020",
                            "8/26/2020",
                            "8/27/2020",
                            "8/28/2020",
                            "8/29/2020",
                            "8/30/2020",
                            "8/31/2020",
                            "9/1/2020",
                            "9/2/2020",
                            "9/3/2020",
                            "9/4/2020",
                            "9/5/2020",
                            "9/6/2020",
                            "9/7/2020"
                        ]
                    }
                }
            ]
        },
        {
            "ts_id": 2,
            "results": []
        },
        {
            "ts_id": 3,
            "results": []
        }
    ]
}
```
如果未执行完毕
```json
{
    "status": 2
}
```
status含义
```py
class CmdStatus(models.IntegerChoices):
    CREATED = 0
    UNCOMITTED = 1
    COMITTED = 2
    DONE = 3
    EXCEPTION = 4
```
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> a3fdca86b02bec6864f5feaa4beb84716b088eb9
=======
>>>>>>> 0cf058aa31e58ec462cb3fffdcb1a68a10d252f3
=======
model save的时候会返回保存的路径
1. LstmLong: keras model to pickle object 的时候报错了...用了自带的save_model方法，保存h5py文件
2. Lstm: keras model to pickle object 的时候报错了...用了自带的save_model方法，保存h5py文件
>>>>>>> ffe089630942a637b8d0830b00359781f1d2c51b
