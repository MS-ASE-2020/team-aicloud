<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="150px" :label-position="left">
      <el-form-item label="Model">
        <el-select v-model="form.model" placeholder="Select your model" @change="AddParam()">
          <el-option
            v-for="item in models"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <span style="float: left">{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <div v-if="Selected">
      <el-form-item label="Parameter Set">
      </el-form-item>
      <el-form-item
        v-for="param in parameters"
        :label="param.label"
        :key="param.label"
        >
        <el-input v-model="param.value" type="textarea" />
        <el-tooltip class="item" effect="dark" placement="right-start">
          <i class="el-icon-info"></i>
          <div slot="content">{{param.intro}}</div>
        </el-tooltip>
      </el-form-item>
      </div>
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
      Selected: false,
      models: [{
        label: 'Linear Fit',
        value: '1'
      }],
      parameters: [{
        label: 'latest_n',
        intro: '用序列中latest_n项做预测',
        type: 'int',
        value: ''
      },
      {
        label: 'add_std_factor',
        type: 'double',
        intro: '控制训练中的标准差在预测结果中的比例',
        value: ''
      }],
      form: {
        model: '',
        parameter: []
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
    },
    AddParam() {
      this.Selected = true
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>
