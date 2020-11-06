import request from '@/utils/request'

export function getModels(params) {
  return request({
    url: '/model/',
    method: 'get',
    params
  })
}

export function getParams(model_name) {
    return request({
        url: '/model/' + String(model_name),
        method: 'get',
    })
}

export function postParams(data) {
    return request({
        url: '/model/',
        method: 'post',
        data: data
    })
}
