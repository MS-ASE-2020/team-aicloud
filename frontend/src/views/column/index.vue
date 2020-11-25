<template>
  <div>
    <h1 style="margin: 20px">Divide Dataset</h1>
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Timestamp">
        <el-select v-model="form.timestamp_indexs" placeholder="Select Column" @change="removeTs()">
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
        <el-select v-model="form.target_indexs" placeholder="Selct Column" @change="removeVal()">
          <el-option
            v-for="item in valcolumns"
            :key="item.index"
            :label="item.label"
            :value="item.index"
          >
            <span style="float: left">{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="GroupBy">
        <el-select v-model="form.groupby_indexs" multiple placeholder="Select Columns">
          <el-option
            v-for="item in filtercolumns"
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
import { getColumn, postColumn } from '@/api/column'

export default {
  data() {
    return {
      // Job
      jodId: '',
      // Column
      columns: [],
      valcolumns: [],
      filtercolumns: [],
      form: {
        timestamp_indexs: '',
        target_indexs: '',
        groupby_indexs: []
      }
    }
  },
  created() {
    this.jodId = this.$route.query.job_id
    this.fetchColumns()
  },
  methods: {
    removeTs() {
      this.valcolumns = [...this.columns]
      for (var i = 0; i < this.valcolumns.length; i++) {
        if (this.valcolumns[i].index === this.form.timestamp_indexs) {
          this.valcolumns.splice(i, 1)
        }
      }
      this.form.groupby_indexs = []
      this.form.target_indexs = ''
    },
    removeVal() {
      this.filtercolumns = [...this.valcolumns]
      for (var i = 0; i < this.filtercolumns.length; i++) {
        if (this.filtercolumns[i].index === this.form.target_indexs) {
          this.filtercolumns.splice(i, 1)
        }
      }
      this.form.groupby_indexs = []
    },
    fetchColumns() {
      getColumn(this.$route.query.data_id).then(response => {
        this.columns = [...response.data.header]
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      const form_data = {}
      form_data['timestamp_indexs'] = '[' + this.form.timestamp_indexs.toString() + ']'
      form_data['target_indexs'] = '[' + this.form.target_indexs.toString() + ']'
      form_data['groupby_indexs'] = '[' + this.form.groupby_indexs.toString() + ']'
      postColumn(this.jodId, form_data).then(response => {
        console.log(response)
        this.$message('Success!')
        this.$router.push({ path: '/job/models', query: { job_id: this.jodId }})
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>
