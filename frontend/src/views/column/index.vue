<template>
  <div>
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Timestamp">
        <el-select v-model="form.TimeStamp" placeholder="Select Column">
          <el-option
            v-for="item in columns"
            :key="item"
            :label="item"
            :value="item"
          >
            <span style="float: left">{{ item }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Values">
        <el-select
          v-model="form.Values"
          multiple
          collapse-tags
          placeholder="Selct Column"
        >
          <el-option
            v-for="item in columns"
            :key="item"
            :label="item"
            :value="item"
          >
            <span style="float: left">{{ item }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="GroupBy">
        <el-select v-model="form.GroupBy" placeholder="Select Columns">
          <el-option
            v-for="item in columns"
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
import { getColumn, postColumn } from '@/api/column'

export default {
  data() {
    return {
      columns: [],
      form: {
        TimeStamp: '',
        Values: '',
        GroupBy: []
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getColumn().then(response => {
        this.columns = response.data.data
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      postColumn(this.form).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })
      this.$message('Success!')
    }
  }
}
</script>
