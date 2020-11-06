import request from '@/utils/request'

export function getDataSets(params) {
  return request({
    url: '/dataset/',
    method: 'get',
    params
  })
}

export function postDataSet(data) {
    return request({
        url: '/dataset/',
        method: 'post',
        data
    })
}