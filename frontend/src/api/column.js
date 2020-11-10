import request from '@/utils/request'

export function getColumn(id) {
  return request({
      url:'/data/' + String(id) + '/',
      method: 'get'
  })
}

export function postColumn(jobId, data) {
  return request({
    url:'/job/' + String(jobId) + '/',
    method: 'put',
    data: data
  })
}

export function getDataSets() {
  return request({
    url: '/data/',
    method: 'get'
  })
}
