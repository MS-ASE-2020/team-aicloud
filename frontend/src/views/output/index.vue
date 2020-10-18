<template>
  <div>
    <el-table
      :data="tableData"
      style="width: 100%"
    >
      <el-table-column
        prop="date"
        label="Timestamp"
        width="180"
      />
      <el-table-column
        prop="value"
        label="Value"
        width="180"
      />
    </el-table>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>
  </div>
</template>

<script>
import LineChart from './components/LineChart'

export default {
  components: {
    LineChart
  },
  data() {
    return {
      tableData: [{
        date: '2020-10-17',
        value: '10'
      }, {
        date: '2020-10-18',
        value: '20'
      }, {
        date: '2020-10-19',
        value: '30'
      }, {
        date: '2016-10-20',
        value: '40'
      }],
      lineChartData: {
        expectedData: [100, 120, 161, 134, 105, 160, 165],
        actualData: [120, 82, 91, 154, 162, 140, 145]
      }
    }
  }
}
</script>
