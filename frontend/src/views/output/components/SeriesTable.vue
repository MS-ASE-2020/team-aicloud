<template>
  <div>
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
    <el-button icon="el-icon-download" type="primary" style="display: block; margin: 10px auto" circle @click="download()" />
  </div>
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
    download() {
      download().then(res => {
        var blob = new Blob([res], {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8"})
        var Temp = document.createElement("a")
        Temp.href = window.URL.createObjectURL(blob)
        Temp.download =new Date().getTime()+'excel'
        document.body.append(Temp)
        Temp.click()
      })
    },
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
        plotdata['hisLength'] = element.ts_history['history'].length
        plotdata['predictions'] = element.ts_history['history']
        plotdata['predictions'] = plotdata['predictions'].concat(element.predictions)
        plotdata['timestamps'] = element.ts_history['timestamp']
        plotdata['timestamps'] = plotdata['timestamps'].concat(element.timestamps)
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
