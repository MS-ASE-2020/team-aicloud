<template>
  <el-form label-position="left" label-width="150px">
    <el-form-item label="ID">
      <span>{{ id }}</span>
    </el-form-item>
    <el-form-item v-if="HasFeature" label="Features">
      <el-select v-model="feature_indexs" multiple placeholder="Select features">
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
      <el-switch v-model="auto_tune" />
    </el-form-item>
    <el-form-item label="Max Eval">
      <el-input v-model="max_eval" type="number" placeholder="调参搜索的次数" style="width:200px" min="1" @change="Check('int', max_eval)" />
    </el-form-item>
    <el-form-item label="Predict Length">
      <el-input v-model="next_k_prediction" type="number" placeholder="预测的天数" style="width:200px" min="1" @change="Check('int', next_k_prediction)" />
    </el-form-item>
    <el-form-item label="Metrics">
      <el-select v-model="eval_metrics" multiple placeholder="Select Metrics">
        <el-option
          v-for="item in METRICS"
          :key="item"
          :label="item"
          :value="item"
        >
          <span style="float: left">{{ item }}</span>
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item v-if="auto_tune === true" label="AutoTune Metrics">
      <el-select v-model="auto_tune_metric" placeholder="Select AutoTune Metrics">
        <el-option
          v-for="item in METRICS"
          :key="item"
          :label="item"
          :value="item"
        >
          <span style="float: left">{{ item }}</span>
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
      <el-form-item label="Parameter Set" />
      <el-form-item
        v-for="param in parameters"
        :key="param.label"
        :label="param.label"
      >
        <el-input
          v-if="param.type==='int'||param.type==='float'"
          v-model="param.val"
          type="number"
          style="width:200px"
          @change="Check(param.type, param.val)"
        />
        <el-select v-if="param.type==='list'" v-model="param.val" style="width:200px" placeholder="Select From List">
          <el-option
            v-for="item in param.valcopy"
            :key="item"
            :label="item"
            :value="item"
          >
            <span style="float: left"> {{ item }}</span>
          </el-option>
        </el-select>
        <el-tooltip class="item" effect="dark" placement="right-start">
          <i class="el-icon-info" />
          <div slot="content">{{ param.intro }}</div>
        </el-tooltip>
      </el-form-item>
      <el-form-item>
        <el-button size="mini" round @click="onSubmit">SET</el-button>
      </el-form-item>
    </div>
    <div v-if="Selected && auto_tune">
      <el-form-item label="Parameter Set" />
      <el-form-item
        v-for="param in parameters"
        :key="param.label"
        :label="param.label"
      >
        <el-input
          v-if="param.type==='int'||param.type==='float'"
          v-model="param.low"
          type="number"
          :placeholder="param.type"
          style="width:200px"
          @change="Check(param.type, param.low)"
        />
        <b v-if="param.type==='int'||param.type==='float'" inline>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>
        <el-input
          v-if="param.type==='int'||param.type==='float'"
          v-model="param.high"
          type="number"
          :placeholder="param.type"
          style="width:200px"
          @change="Check(param.type, param.high)"
        />
        <el-select v-if="param.type==='list'" v-model="param.val" multiple style="width:200px" placeholder="Select From List">
          <el-option
            v-for="item in param.valcopy"
            :key="item"
            :label="item"
            :value="item"
          >
            <span style="float: left"> {{ item }}</span>
          </el-option>
        </el-select>
        <el-tooltip class="item" effect="dark" placement="right-start">
          <i class="el-icon-info" />
          <div slot="content">{{ param.intro }}</div>
        </el-tooltip>
      </el-form-item>
      <el-form-item>
        <el-button size="mini" round @click="onSubmit">SET</el-button>
      </el-form-item>
    </div>
  </el-form>
</template>

<script>
import { getModels, getParams } from '@/api/model'

export default {
  props: {
    id: {
      type: Number,
      required: true
    },
    features: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      // const
      METRICS: [
        'mse', 'rmse', 'nrmse', 'me', 'mae', 'mad', 'gmae', 'mdae', 'mpe', 'mape', 'mdape', 'smape', 'smdape', 'maape', 'mase', 'std_ae',
        'std_ape', 'rmspe', 'rmdspe', 'rmsse', 'inrse', 'rrse', 'mre', 'rae', 'mrae', 'mdrae', 'gmrae', 'mbrae', 'umbrae', 'mda', 'bias', 'r2_score'],
      //
      auto_tune: false,
      HasFeature: false,
      Selected: false,
      //
      models: [],
      parameters: [],
      //
      max_eval: 1,
      next_k_prediction: 1,
      eval_metrics: [],
      auto_tune_metric: '',
      model_name: '',
      feature_indexs: [],
      passCheck: true
    }
  },
  created() {
    this.HasFeature = (this.features.length !== 0)
    this.fetchModels()
  },
  methods: {
    Check(type, str) {
      if (type === 'int') {
        var r = /^\+?[1-9][0-9]*$/
        if (r.test(str) === false) {
          alert('Input positive integer!')
          this.passCheck = false
        } else {
          this.passCheck = true
        }
      } else {
        return true
      }
    },
    fetchModels() {
      getModels().then(response => {
        this.models = response.data.data
      }).catch(err => {
        console.log(err)
      })
    },
    Parseparam(type, val) {
      if (type === 'int') {
        return parseInt(val)
      } else if (type === 'float') {
        return parseFloat(val)
      } else {
        return val
      }
    },
    generatePost() {
      const post = {}
      post['model_name'] = this.model_name
      post['feature_indexs'] = '[' + String(this.feature_indexs) + ']'
      post['max_eval'] = Number(this.max_eval)
      post['next_k_prediction'] = Number(this.next_k_prediction)
      post['auto_tune'] = this.auto_tune
      post['eval_metrics'] = this.eval_metrics
      const hyper_params = []
      if (this.auto_tune) {
        post['auto_tune_metric'] = this.auto_tune_metric
        for (var i = 0; i < this.parameters.length; i++) {
          const param = {}
          param['name'] = this.parameters[i].label
          param['type'] = this.parameters[i].type
          if (param['type'] === 'list') {
            param['choice'] = this.Parseparam('list', this.parameters[i].val)
          } else {
            param['low'] = this.Parseparam(param['type'], this.parameters[i].low)
            param['high'] = this.Parseparam(param['type'], this.parameters[i].high)
          }
          hyper_params.push(param)
        }
      } else {
        for (var idx = 0; idx < this.parameters.length; idx++) {
          const param = {}
          param['name'] = this.parameters[idx].label
          param['type'] = this.parameters[idx].type
          param['val'] = this.Parseparam(param['type'], this.parameters[idx].val)
          hyper_params.push(param)
        }
      }
      post['hyper_params'] = hyper_params
      return post
    },
    onSubmit() {
      if (this.passCheck) {
        this.$confirm('Apply this Settings to All Series', 'Apply All', {
          confirmButtonText: 'YES',
          cancelButtonText: 'NO',
          type: 'info',
          center: true
        }).then(() => {
          this.$emit('setDone', this.id, true, this.generatePost())
        }).catch(() => {
          this.$emit('setDone', this.id, false, this.generatePost())
        })
      } else {
        alert('Input Error!')
      }
    },
    AddParam() {
      getParams(this.model_name).then(response => {
        var resdata = response.data.data
        for (var i = 0; i < resdata.length; i++) {
          if (resdata[i]['type'] === 'int') { resdata[i]['low'] = 1 } else {
            resdata[i]['low'] = 0
          }
          resdata[i]['high'] = 10 * resdata[i].val
          resdata[i]['valcopy'] = resdata[i].val
          if (resdata[i]['type'] === 'list') {
            resdata[i]['val'] = null
          }
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
