<template>
  <el-form label-position="left" label-width="150px">
    <el-form-item label="ID">
      <span>{{ id }}</span>
    </el-form-item>
    <el-form-item label="Features" v-if="HasFeature">
      <el-select v-model="feature_indexs" multiple placeholder="Select features" >
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
    <el-form-item label="AutoTune">
      <el-switch v-model="auto_tune">
      </el-switch>
    </el-form-item>
    <el-form-item label="Max Eval">
      <el-input v-model="max_eval" type="number" placeholder="调参搜索的次数" style="width:200px"></el-input>
    </el-form-item>
    <el-form-item label="Predict Length">
      <el-input v-model="next_k_predicition" type="number" placeholder="预测的天数" style="width:200px"></el-input>
    </el-form-item>
    <el-form-item label="Metrics">
      <el-select v-model="eval_metrics" multiple placeholder="Select Metrics">
        <el-option
          v-for="item in METRICS"
          :key=item
          :label=item
          :value=item
        >
          <span style="float: left">{{item}}</span>
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Model">
      <el-select v-model="model_name" placeholder="Select Model" @change="AddParam()">
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
    <div v-if="Selected && auto_tune === false">
      <el-form-item label="Parameter Set">
      </el-form-item>
      <el-form-item
        v-for="param in parameters"
        :label="param.label"
        :key="param.label"
      >
        <el-input 
          v-model="param.val" 
          type="number" 
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
        <el-button size="mini" round @click="onSubmit">SET{{index}}</el-button>
      </el-form-item>
    </div>
    <div v-if="Selected && auto_tune">
      <el-form-item label="Parameter Set">
      </el-form-item>
      <el-form-item
        v-for="param in parameters"
        :label="param.label"
        :key="param.label"
      >
      <el-input v-model="param.low" type="number" placeholder=param.low style="width:200px"></el-input>
        <b inline>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>
      <el-input v-model="param.high" type="number" placeholder=param.high style="width:200px"></el-input>
      <el-tooltip class="item" effect="dark" placement="right-start">
        <i class="el-icon-info"></i>
        <div slot="content">{{param.intro}}</div>          
      </el-tooltip>
      </el-form-item>
      <el-form-item>
        <el-button size="mini" round @click="onSubmit">SET{{index}}</el-button>
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
      //const
    METRICS: [
    'mse','rmse','nrmse', 'me','mae','mad','gmae','mdae','mpe','mape','mdape','smape','smdape','maape','mase','std_ae',
    'std_ape','rmspe','rmdspe','rmsse','inrse','rrse','mre','rae','mrae','mdrae','gmrae','mbrae','umbrae','mda','bias','r2_score'],
      //
      auto_tune: false,
      HasFeature: false,
      Selected: false,
      index: 1,
      //
      models: [],
      parameters: [],

      //
      max_eval: 0,
      next_k_predicition: 0,
      eval_metrics: [],
      model_name: '',
      feature_indexs: []
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
    generatePost() {
      this.index = this.index + 1
        let post = {}
        post['model_name'] = this.model_name
        post['feature_indexs'] = '[' + String(this.feature_indexs) + ']'
        post['max_eval'] = this.max_eval
        post['next_k_prediction'] = this.next_k_predicition
        post['auto_tune'] = this.auto_tune
        post['eval_metrics'] = this.eval_metrics
        let hyper_params = []
        if(this.auto_tune) {
          for(var i=0; i<this.parameters.length; i++) {
            let param = {}
            param['name'] = this.parameters[i].label
            param['type'] = this.parameters[i].type
            param['low'] = this.parameters[i].low
            param['high'] = this.parameters[i].high
            hyper_params.push(param)
          }
        }
        else {
          for(var i=0; i<this.parameters.length; i++) {
            let param = {}
            param['name'] = this.parameters[i].label
            param['type'] = this.parameters[i].type
            param['val'] = this.parameters[i].val
            hyper_params.push(param)
          }
        }        
        post['hyper_params'] = hyper_params
        return post
    },
    onSubmit() {
      this.$confirm('Apply this Settings to All Series', 'Apply All', {
        confirmButtonText: 'YES',
        cancelButtonText: 'NO',
        type: 'info',
        center: true
      }).then( () => {
        this.$emit('setDone', this.id, true, this.generatePost())
      }).catch( () => {
        this.$emit('setDone', this.id, false, this.generatePost())
      })
    },
    AddParam() {
      getParams(this.model_name).then(response => {
        var resdata = response.data.data
        for(var i=0; i<resdata.length; i++) {
          resdata[i]['low'] = 0
          resdata[i]['high'] = 10 * resdata[i].val
        }
        this.parameters = resdata
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
