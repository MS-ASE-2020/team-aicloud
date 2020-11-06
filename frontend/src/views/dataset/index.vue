
<template>
  <div>
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Select Dataset">
        <el-select v-model="data" placeholder="Selct DataSet">
          <el-option
            v-for="item in datasets"
            :key="item"
            :label="item"
            :value="item"
          >
            <span style="float: left">{{ item }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Submit</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getDataSets, postDataSet } from '@/api/dataset'

export default {
  data() {
    return {
      datasets: [],
      data: ''
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getDataSets().then(response => {
        this.datasets = response.data.data
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      postDataSet(this.data).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })
      this.$message('Success!')
    }
  }
}
</script>
