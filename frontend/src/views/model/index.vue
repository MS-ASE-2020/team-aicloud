<template>
  <div class="app-container">
    <el-form ref="form" label-width="150px">
      <el-form-item label="Model">
        <el-select v-model="selected_model" placeholder="Select your model" @change="AddParam()">
          <el-option
            v-for="item in models"
            :key="item"
            :label="item"
            :value="item"
          >
            <span style="float: left">{{ item }}</span>
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
        <el-input v-model="param.val" type="textarea" placeholder=param.val maxlength="150px"></el-input>
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
import { getModels, postModel, getParams, postParams } from '@/api/model'

export default {
  data() {
    return {
      Selected: false,
      models: [],
      parameters: [],
      selected_model: ''
    }
  },
  created() {
    this.fetchModels()
  },
  methods: {
    fetchModels() {
      getModels().then(response => {
        this.models = response.data.data
      }).catch(err => {
        console.log(err)
      })
    },
    onSubmit() {
      postParams(this.parameters)
      this.$message('Start!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },
    AddParam() {
      getParams(this.selected_model).then(response => {
        this.parameters = response.data.data
      }).catch(err => {
        console.log(err)
      })

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
