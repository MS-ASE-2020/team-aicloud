<template>
  <el-form label-position="left" label-width="150px">
    <el-form-item label="ID">
      <span>{{ id }}</span>
    </el-form-item>
    <el-form-item label="Features" v-if="HasFeature">
      <el-select v-model="post.feature_indexs" multiple placeholder="Select features" >
        <el-option
          v-for="(item, index) in features"
          :key="index"
          :label="item"
          :value="index"
        >
          <span style="float: left">{{ item }}</span>
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Model">
      <el-select v-model="post.model_name" placeholder="Select your model" @change="AddParam()">
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
        <el-input 
          v-model="param.val" 
          type="textarea" 
          placeholder=param.val 
          style="width:200px"
        >
        </el-input>
        <el-tooltip class="item" effect="dark" placement="right-start">
          <i class="el-icon-info"></i>
          <div slot="content">{{param.intro}}</div>          
        </el-tooltip>
      </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit" :disable="DisableButton">Submit</el-button>
    </el-form-item>
    </div>
  </el-form>
</template>

<script>
import { getModels, getParams } from '@/api/model'

export default {
  props: {
    id: Number,
    features: Array
  },
  data() {
    return {
      HasFeature: false,
      DisableButton: false,
      Selected: false,
      models: [],
      features: [],
      parameters: [],
      post: {
        model_name: '',
        feature_indexs: []
      }
    }
  },
  created() {
    this.HasFeature = (this.features.length != 0) ? true : false 
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
      if(!this.DisableButton){
        let post = {}
        post['model_name'] = this.post.model_name
        post['feature_indexs'] = '[' + String(this.post.feature_indexs) + ']'
        post['ts_id'] = this.id
        let hyper_params = {}
        for(var i=0; i<this.parameters.length; i++) {
          hyper_params[this.parameters[i].label] = this.parameters[i].val
        }
        post['hyper_params'] = hyper_params
        this.$emit('setDone', post)
        this.DisableButton = true
      }      
    },
    AddParam() {
      getParams(this.post.model_name).then(response => {
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
