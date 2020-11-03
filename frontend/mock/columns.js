const Mock = require('mockjs')

const columns = [
    {
        label: 'feature1',
        value: 1
    },
    {
        label: 'feature2',
        value: 2
    }
]

module.exports = [
  //get columns
  {
    url: '/select/column',
    type: 'get',
    response: config => {
      return {
        columns: columns
      }
    }
  },
  //post result
  {
      url: '/select/column',
      type: 'post',
      response : config => {
          console.log(config)
          return {
              code: 20000
          }
      }
  }
]