
<template>
  <div>
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Timestamp">
        <el-select v-model="form.time" placeholder="Select Column">
          <el-option
            v-for="item in columns"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <span style="float: left">{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Value">
        <el-select v-model="form.value" placeholder="Selct Column">
          <el-option
            v-for="item in columns"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <span style="float: left">{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Submit</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {getColumn, postColumn} from '@/api/column'

export default {
  data() {
    return {
      columns: [],
      form : {
        time: '',
        value: ''
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getColumn().then(response => {
        this.columns = response.data.columns
      }).catch(error => {
        console.log(error)
      })
    },
    onSubmit() {
      let respData = {
        "Time": this.form.time,
        "Value": this.form.value
      }
      postColumn(respData).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })
      this.$message('Done!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
  }
}
</script>
