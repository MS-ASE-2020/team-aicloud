import request from '@/utils/request'

export function getColumn(params) {
  return request({
      url:'/column/',
      method: 'get',
      params
  })
}

export function postColumn(params) {
  return request({
    url:'/column/',
    method: 'post',
    data:params
  }
  )
}