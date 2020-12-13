<template>
  <div class="Select">
    <h1>Select Dataset</h1>
    <el-select v-model="dataId" placeholder="Select DataSet" style="display:block;margin:30px auto" @change="previewDataset()">
      <el-option
        v-for="item in datasets"
        :key="item.id"
        :label="item.name"
        :value="item.id"
      >
        <span style="float: left">{{ item.name }}</span>
      </el-option>
    </el-select>
    <el-table
      :data="preview"
      border
    >
      <el-table-column
        v-for="head in header"
        :key="head.index"
        :prop="head.label"
        :label="head.label"
      />
    </el-table>
    <el-button type="primary" style="display:block;margin:20px auto" :disabled="disabled" @click="onSubmit">NEXT</el-button>
  </div>
</template>

<script>
import { getDataSets, postDataSet, getColumn } from '@/api/column'

export default {
  data() {
    return {
      // Dataset
      datasets: [],
      dataId: '',
      preview: [{}, {}, {}, {}, {}],
      header: [],
      ShowTable: false,
      disabled: true
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
      getColumn(this.dataId).then(response => {
        this.header = response.data.header
        var header_arr = response.data.header
        var len = header_arr.length
        var previewdata = response.data.heads
        for (var i = 0; i < 5; i++) {
          var row = {}
          for (var j = 0; j < len; j++) {
            row[header_arr[j].label] = previewdata[header_arr[j].label][i]
          }
          this.$set(this.preview, i, row)
        }
        this.ShowTable = true
        this.disabled = false
      }).catch(error => {
        console.log(error)
      })
    },
    getName(id) {
      for (var i = 0; i < this.datasets.length; i++) {
        if (this.datasets[i].id === id) { return this.datasets[i].name }
      }
    },
    onSubmit() {
      postDataSet({ 'data_id': this.dataId, 'name': this.getName(this.dataId) }).then(response => {
        this.$message('Success!')
        this.$router.push({ path: '/newjob/columns', query: { job_id: response.data.data.id, data_id: this.dataId }})
        this.dataset = {}
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>

<style>
 .Select{
   margin: 30px
 }
 .el-table{
   margin:auto;
   width:75%
 }
</style>
