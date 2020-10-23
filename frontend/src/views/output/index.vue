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
        <template slot-scope="scope">
          {{ scope.row.title }}
        </template>
      </el-table-column>
      <el-table-column label="Value" width="110" align="center" prop="value">
        <template slot-scope="scope">
          <span>{{ scope.row.author }}</span>
        </template>
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
      list: [{
                time: '20200821',
                val: 50
            },
            {
                time: '20200821',
                val: 60
            },
    ],
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
        console.log(this.list)
        //this.data = JSON.parse(JSON.stringify(response.data))
        //console.log(this.data)
        //this.list = this.data.predicted
        //console.log(this.list)
        this.listLoading = false
      })
    }
  }
}
</script>
