<template>
  <div>
    <h3>Select Dataset</h3>
    <el-select v-model="data" placeholder="Select DataSet" @change="previewDataset()">
      <el-option
        v-for="item in datasets"
        :key="item.id"
        :label="item.name"
        :value="item"
      >
        <span style="float: left">{{ item.name }}</span>
      </el-option>
    </el-select>
    <el-table
      :data="preview"
      style="width: 100%"
    >
      <el-table-column
        v-for="head in header"
        :key="head.index"
        :prop=head.label
        :label=head.label
      >
      </el-table-column>
    </el-table> 
    <el-button type="primary" @click="onSubmit">Submit</el-button>
  </div>
</template>

<script>
import { getDataSets, postDataSet, getColumn } from '@/api/column'

export default {
  data() {
    return {
      //Dataset
      datasets: [],
      data: {},
      preview: [{}, {}, {}, {}, {}],
      header: [],
      ShowTable: false
    }
  },
  created() {
    this.fetchDataSet()
  },
  methods: {
    fetchDataSet() {
      getDataSets().then(response => {
        this.datasets = response.data
      }).catch(err => {
        console.log(err)
      })
    },
    previewDataset() {
      getColumn(this.data.id).then(response => {
        this.header = response.data.header
        var header_arr = response.data.header
        var len = header_arr.length
        var previewdata = response.data.heads
        for(var i=0; i<5; i++) {
          var row = {}
          for(var j=0; j<len; j++) {
            row[header_arr[j].label] = previewdata[header_arr[j].label][i] 
          }
          this.$set(this.preview, i, row)
        }
        this.ShowTable = true
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      postDataSet({'data_id': this.data.id, 'name': this.data.name}).then(response => {
        this.$message('Success!')
        this.$router.push({path: '/job/columns', query: {job_id: response.data.data.id, data_id: this.data.id}})
      }).catch(err => {
        console.log(err)
      })      
    }
  }
}
</script>
