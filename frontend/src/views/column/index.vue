<template>
  <div>
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Select Dataset">
        <el-select v-model="select_dataset" placeholder="Select DataSet" @change="fetchColumns()">
          <el-option
            v-for="item in datasets"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
            <span style="float: left">{{ item.name }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Timestamp">
        <el-select v-model="form.TimeStamp" placeholder="Select Column">
          <el-option
            v-for="item in columns"
            :key="item.index"
            :label="item.label"
            :value="item.index"
          >
            <span style="float: left">{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Values">
        <el-select v-model="form.Values" placeholder="Selct Column">
          <el-option
            v-for="item in columns"
            :key="item.index"
            :label="item.label"
            :value="item.index"
          >
            <span style="float: left">{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="GroupBy">
        <el-select v-model="form.GroupBy" multiple collapse-tags placeholder="Select Columns">
          <el-option
            v-for="item in columns"
            :key="item.index"
            :label="item.label"
            :value="item.index"
          >
            <span style="float: left">{{ item.label }}</span>
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
import { getColumn, postColumn, getDataSets } from '@/api/column'

export default {
  data() {
    return {
      //Job
      jodId: 1,
      //Dataset
      datasets: [{
     "id": 1,
     "name": "test_dataset",
     "uuid": "13740a08-1edd-49be-8d3f-1784e79a8e1d",
     "time_created": "2020-11-09T14:52:53.002395+08:00",
     "upload": "/uploads/allRegion_37d_MSDN_vmlevel.csv",
     "related_user": 1
      }],
      select_dataset: '',
      //Column
      columns: [],
      form: {
        TimeStamp: '',
        Values: '',
        GroupBy: []
      }
    }
  },
  created() {
    this.fetchDataSet()
  },
  methods: {
    fetchDataSet() {
      getDataSets().then(response => {
        //this.datasets = response.data
      }).catch(err => {
        console.log(err)
      })
    },
    fetchColumns() {
      getColumn(this.select_dataset).then(response => {
        this.columns = response.data.header
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      postColumn(this.jodId, this.form).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })
      this.$message('Success!')
      this.$router.push({path: '/job/models'})
    }
  }
}
</script>
