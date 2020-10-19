<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="Cycle Type">
        <el-checkbox-group v-model="form.type">
          <el-checkbox label="Daily" name="type" />
          <el-checkbox label="Weekly" name="type" />
          <el-checkbox label="Monthly" name="type" />
          <el-checkbox label="Yearly" name="type" />
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="Holiday">
        <el-input v-model="form.holiday" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Submit</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        type: [],
        holiday: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
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

