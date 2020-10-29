<template>
  <div>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column label="Time" sortable prop="time">
      </el-table-column>
      <el-table-column label="Value" width="110" align="center" prop="val">
      </el-table-column>
    </el-table>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>
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
      list: [],
      listLoading: true,
      lineChartData: {
        expectedData: [100, 120, 161, 134, 105, 160, 165],
        actualData: [120, 82, 91, 154, 162, 140, 145]
      }
    }
  },
  created() {
    this.fetchdata()
  },
  methods: {
    fetchdata() {
      this.listLoading = true
      getList().then(response => {
        var resdata = JSON.parse(JSON.stringify(response.data))
        this.list = resdata.predicted
        //console.log(this.list)
        this.listLoading = false
      })
    }
  }
}
</script>
