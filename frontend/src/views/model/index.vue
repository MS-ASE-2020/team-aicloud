<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="150px">
      <el-form-item label="Model">
        <el-select v-model="form.model" placeholder="Select your model" @change="AddParam()">
          <el-option
            v-for="item in models"
            :key="item.name"
            :label="item.name"
            :value="item.name"
          >
            <span style="float: left">{{ item.name}}</span>
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
import {getModels, postModel, getParams, postParams} from '@/api/model'

export default {
  data() {
    return {
      Selected: false,
      models: [],
      parameters: [],
      form: {
        model: '',
        parameter: []
      }
    }
  },
  created() {
      this.fetchModels()
  },
  methods: {
    fetchModels() {
      getModels().then(response => {
        console.log(response)
        this.models = response.data.models
      }).catch( err => {
        console.log(err)
      })
    },
    onSubmit() {
      for(var param in this.parameters){
        this.form.parameter.push({
          'name':param.name,
          'value':param.value
        })
      }
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
      postModel(this.form.model).then(response => {
        console.log(response)
      }).catch(err =>
      console.log(err))

      getParams().then(response => {
        this.parameters = response.data.params
      }).catch(err =>{
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
