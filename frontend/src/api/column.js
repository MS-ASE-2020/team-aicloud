import request from '@/utils/request'

export function getColumn(id) {
  return request({
    url: '/data/' + String(id) + '/',
    method: 'get'
  })
}

export function postColumn(jobId, data) {
  return request({
    url: '/job/' + String(jobId) + '/',
    method: 'put',
    data: data,
    // TODO: set asynchronous request later
    timeout: 100000
  })
}

export function getDataSets() {
  return request({
    url: '/data/',
    method: 'get'
  })
}

export function deleteDataSets(id) {
  return request({
    url: '/data/' + String(id) + '/',
    method: 'delete'
  })
}

export function postDataSet(data) {
  return request({
    url: '/job/',
    method: 'post',
    data: data
  })
}
