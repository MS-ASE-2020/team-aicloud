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
      <el-table-column label="Model Donwload">
        <template slot-scope="props">
          <el-button icon="el-icon-download" circle @click="download(props.row.model_id)" />
        </template>
      </el-table-column>
      <el-table-column label="Setting Donwload">
        <template slot-scope="props">
          <el-button icon="el-icon-download" circle @click="downloadsetting(props.row.model_id)" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import LineChart from './LineChart'
import { download, downloadsetting } from '@/api/table'
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
      metricName: [],
      ts_id: 0
    }
  },
  created() {
    this.createTable()
  },
  methods: {
    downloadsetting(model_id) {
      downloadsetting(model_id).then(res => {
        var fileDownload = require('js-file-download')
        fileDownload(res, 'filename.csv')
        var blob = new Blob([res], { type: 'application/json' })
        var Temp = document.createElement('a')
        Temp.href = window.URL.createObjectURL(blob)
        Temp.download = new Date().getTime()
        document.body.append(Temp)
        Temp.click()
      })
    },
    download(model_id) {
      download(model_id).then(res => {
        console.log(res)
        var blob = new Blob([res], { type: 'application/octet-stream' })
        var Temp = document.createElement('a')
        Temp.href = window.URL.createObjectURL(blob)
        Temp.download = new Date().getTime()
        document.body.append(Temp)
        Temp.click()
      })
    },
    createTable() {
      // Union metric name
      this.ts_id = this.results[0].ts_id
      this.results.forEach(element => {
        const arr = Object.keys(element.metrics)
        this.metricName = this.metricName.concat(arr.filter(v => !this.metricName.includes(v)))
      })
      let i = 0
      this.results.forEach(element => {
        const config = { 'id': i }
        config['model'] = element.model_name// name undefine
        config['model_id'] = element.model_id
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
