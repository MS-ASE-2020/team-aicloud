<template>
  <div>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading Metrics"
      border
      fit
      highlight-current-row
    >
      <el-table-column label="ID" sortable prop="ts_id">
      </el-table-column>
      <el-table-column label="MSE" width="110" align="center" prop="mse">
      </el-table-column>
      <el-table-column label="RMSE" width="110" prop="rmse">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import LineChart from './components/LineChart'
import { getList } from '@/api/table'
export default {
  components: {
    LineChart
  },
  data() {
    return {
      job_id: '',
      list: [],
      listLoading: true,
      lineChartData: {
        timestamps: [],
        datalists: [],
        legend: []
      }
    }
  },
  created() {
    this.fetchdata()
  },
  methods: {
    fetchdata() {
      this.listLoading = true
      this.job_id = this.$route.query.job_id
      var resdata = [
          {
        "predictions": [
            236,
            238,
            240,
            242,
            244
        ],
        "timestamps": [
            "2020-09-08 00:00:00",
            "2020-09-09 00:00:00",
            "2020-09-10 00:00:00",
            "2020-09-11 00:00:00",
            "2020-09-12 00:00:00"
        ],
        "metrics": {
            "mse": 255.0,
            "rmse": 15.968719422671311
        },
        "config": {
            "latest_n": 5,
            "add_std_factor": 0
        },
        "ts_id": 8797
    },
    {
        "predictions": [
            237,
            238,
            240,
            242,
            244
        ],
        "timestamps": [
            "2020-09-08 00:00:00",
            "2020-09-09 00:00:00",
            "2020-09-10 00:00:00",
            "2020-09-11 00:00:00",
            "2020-09-12 00:00:00"
        ],
        "metrics": {
            "mse": 255.0,
            "rmse": 15.968719422671311
        },
        "config": {
            "latest_n": 5,
            "add_std_factor": 0
        },
        "ts_id": 8797
    }
        ]
        this.lineChartData.timestamps = resdata[0].timestamps
        for(var i = 0; i< resdata.length; i++) {
          this.lineChartData.legend.push('')
          this.lineChartData.datalists.push([])
          this.list.push({})
          //
          let row = {}
          row['ts_id'] = resdata[i].ts_id
          row['mse'] = resdata[i].metrics.mse
          row['rmse'] = resdata[i].metrics.rmse
          this.$set(this.list, i, row)
          //
          let predlist = []
          predlist = resdata[i].predictions
          this.$set(this.lineChartData.datalists, i, predlist)
          //
          let str = 'ts' + String(row['ts_id'])
          this.$set(this.lineChartData.legend, i, str)
        }
        this.listLoading = false
    //   getList(this.job_id).then(response => {
    //     //var resdata = response.data
    //     var resdata = [
    //       {
    //     "predictions": [
    //         236,
    //         238,
    //         240,
    //         242,
    //         244
    //     ],
    //     "timestamps": [
    //         "2020-09-08 00:00:00",
    //         "2020-09-09 00:00:00",
    //         "2020-09-10 00:00:00",
    //         "2020-09-11 00:00:00",
    //         "2020-09-12 00:00:00"
    //     ],
    //     "metrics": {
    //         "mse": 255.0,
    //         "rmse": 15.968719422671311
    //     },
    //     "config": {
    //         "latest_n": 5,
    //         "add_std_factor": 0
    //     },
    //     "ts_id": 8797
    // }
    //     ]
    //     this.lineChartData.timestamps = resdata[0].timestamps
    //     for(var i = 0; i< resdata.length; i++) {
    //       this.lineChartData.length.push('')
    //       this.lineChartData.datalists.push([])
    //       this.list.push({})
    //       //
    //       let row = {}
    //       row['ts_id'] = resdata[i].ts_id
    //       row['mse'] = resdata[i].metrics.mse
    //       row['rmse'] = resdata[i].metrics.rmse
    //       this.$set(this.list, i, row)
    //       //
    //       let predlist = []
    //       predlist = resdata[i].preditions
    //       this.$set(this.lineChartData.datalists, i, predlist)
    //       //
    //       let str = 'ts' + String(row['ts_id'])
    //       this.$set(this.lineChartData.legend, i, str)
    //     }
    //     console.log(this.list)
    //     console.log(this.lineChartData)
    //     this.listLoading = false
    //   })
    }
  }
}
</script>
