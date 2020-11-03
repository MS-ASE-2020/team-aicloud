const { config } = require('@vue/test-utils')
const Mock = require('mockjs')

const models = [{
    name: 'Linear Fit',
    }]

const params = [{
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
  }]

module.exports = [
  //get models
  {
    url: '/models',
    type: 'get',
    response: config => {
      return {
        models: models
      }
    }
  },
  //post models
  {
      url: '/models',
      type: 'post',
      response : config => {
          console.log(config)
          return {
              code: 20000
          }
      }
  },
  //get params
  {
      url: '/params',
      type: 'get',
      response : config => {
          return {
              code: 20000,
              params: params
          }
      }
  },
  //post params
  {
      url: '/params',
      type: 'post',
      response: config => {
          console.log(config)
          return {
              code: 20000
          }
      }
  }
]