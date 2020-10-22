const Mock = require('mockjs')

module.exports = [
  {
    url: '/upload/data',
    type: 'post',
    response: config => {
      return {
        code: 20000
      }
    }
  }
]
