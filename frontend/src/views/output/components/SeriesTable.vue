<template>
  <el-table
    :data="tableData"
    border
    style="width: 75%; margin: auto;"
  >
    <el-table-column
      prop="model"
      label="Model"
    />
    <el-table-column
      prop="config"
      label="Cofig"
      fit
    />
    <el-table-column label="Metrics">
      <el-table-column
        v-for="item in metricName"
        :key="item"
        :prop="item"
        :label="item"
        sortable
      />
    </el-table-column>
    <el-table-column type="expand">
      <template slot-scope="props">
        <line-chart :chart-data="predictList[props.row.id]" />
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import LineChart from './LineChart'
export default {
  components: {
    LineChart
  },
  props: {
    results: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      tableData: [],
      predictList: [],
      metricName: []
    }
  },
  created() {
    this.createTable()
  },
  methods: {
    createTable() {
      // Union metric name
      this.results.forEach(element => {
        const arr = Object.keys(element.metrics)
        this.metricName = this.metricName.concat(arr.filter(v => !this.metricName.includes(v)))
      })
      let i = 0
      this.results.forEach(element => {
        const config = { 'id': i }
        config['model'] = element.model_name// name undefine
        let str = JSON.stringify(element.config)
        str = str.substring(1, str.length - 1)
        str = str.replace(',', '\n')
        config['config'] = str
        //
        this.metricName.forEach(name => {
          config[name] = element.metrics[name]
        })
        this.tableData.push(config)
        const plotdata = {}
        plotdata['predictions'] = element.predictions
        plotdata['timestamps'] = element.timestamps
        this.predictList.push(plotdata)
        i++
      })
    }
  }
}
</script>

<style>
.el-table{
  margin: 30px;
}
  .el-table .cell {
    white-space: pre-line;
  }
</style>
