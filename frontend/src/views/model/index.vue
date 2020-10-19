<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Model">
        <el-select v-model="form.model" placeholder="Select your model">
          <el-option
            v-for="item in models"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <span style="float: left">{{ item.label }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="param1">
        <el-input v-model="form.param1" type="textarea" />
      </el-form-item>
      <el-form-item label="param2">
        <el-input v-model="form.param2" type="textarea" />
      </el-form-item>
      <el-form-item label="param3">
        <el-input v-model="form.param3" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Train</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      models: [{
        label: 'Prophet',
        value: '1'
      }
      ],
      form: {
        model: '',
        param1: '',
        param2: '',
        param3: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.$message('Start!')
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

<style scoped>
.line{
  text-align: center;
}
</style>
