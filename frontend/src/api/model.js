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
        method: 'get'
    })
}

export function postSeries(job_id,data) {
    return request({
        url: '/job/' + String(job_id) + '/',
        method: 'patch',
        data: data,
        // TODO: set asynchronous request later
        timeout: 50000
    })
}

export function fetchSeries(job_id) {
  return request({
    url: '/job/' + String(job_id) + '/ts_details/',
    method: 'get'
  })
}
