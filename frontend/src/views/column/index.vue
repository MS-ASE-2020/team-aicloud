<template>
  <div>
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Timestamp">
        <el-select v-model="form.TimeStamp" multiple placeholder="Select Column">
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
        <el-select v-model="form.Values" multiple placeholder="Selct Column">
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
        <el-select v-model="form.groupby_indexs" multiple collapse-tags placeholder="Select Columns">
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
import { getColumn, postColumn, getDataSets, postDataSet } from '@/api/column'

export default {
  data() {
    return {
      //Job
      jodId: '',
      //Column
      columns: [],
      form: {
        TimeStamp: [],
        Values: [],
        groupby_indexs: []
      }
    }
  },
  created() {
    this.jodId = this.$route.query.job_id
    this.fetchColumns()
  },
  methods: {
    fetchColumns() {
      getColumn(this.$route.query.data_id).then(response => {
        this.columns = response.data.header
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      // var form = {}
      // form['TimeStamp'] = String(this.form.TimeStamp)
      // form['Values'] = String(this.form.Values)
      // form['groupby_indexs'] = String(this.form.groupby_indexs)
      postColumn(this.jodId, this.form).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })
      this.$message('Success!')
      this.$router.push({path: '/job/models', query: { job_id:this.jodId }})
    }
  }
}
</script>
