<template>
  <div class="select-Column">
    <h1>Divide Dataset</h1>
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Timestamp">
        <el-select v-model="form.timestamp_indexs" placeholder="Select Column" @change="ChangeStatus()">
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
        <el-select v-model="form.target_indexs" placeholder="Select Column" @change="ChangeStatus()">
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
        <el-select v-model="form.groupby_indexs" multiple placeholder="Select Columns">
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
        <el-button type="primary" :disabled="disabled" @click="onSubmit">NEXT</el-button>
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
      disabled: true,
      form: {
        timestamp_indexs: null,
        target_indexs: null,
        groupby_indexs: []
      }
    }
  },
  created() {
    this.jodId = this.$route.query.job_id
    this.fetchColumns()
  },
  methods: {
    InputCheck() {
      return (this.form.timestamp_indexs !== this.form.target_indexs) && !this.form.groupby_indexs.includes(this.form.timestamp_indexs) && !this.form.groupby_indexs.includes(this.form.target_indexs)
    },
    ChangeStatus() {
      this.disabled = this.form.timestamp_indexs === null || this.form.target_indexs === null
    },
    fetchColumns() {
      getColumn(this.$route.query.data_id).then(response => {
        this.columns = [...response.data.header]
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      if (this.InputCheck()) {
        const form_data = {}
        form_data['timestamp_indexs'] = '[' + this.form.timestamp_indexs.toString() + ']'
        form_data['target_indexs'] = '[' + this.form.target_indexs.toString() + ']'
        form_data['groupby_indexs'] = '[' + this.form.groupby_indexs.toString() + ']'
        postColumn(this.jodId, form_data).then(response => {
          console.log(response)
          this.$message('Success!')
          this.$router.push({ path: '/newjob/models', query: { job_id: this.jodId }})
        }).catch(error => {
          console.log(error)
        })
      } else {
        alert('Conflict selection!')
        this.form.timestamp_indexs = null
        this.form.target_indexs = null
        this.disabled = true
        this.form.groupby_indexs = []
      }
    }
  }
}
</script>

<style>
  .select-Column{
    margin: 30px
  }
</style>
