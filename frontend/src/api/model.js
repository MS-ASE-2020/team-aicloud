import request from '@/utils/request'

export function getModels(params) {
    return request({
        url: '/model/',
        method: 'get',
        params
    })
}

export function postModel(data) {
    return request({
        url: '/models',
        method: 'post',
        data: data
    })
}

export function getParams(model_name) {
    return request({
        url: '/model/' + String(model_name),
        method: 'get',
        params: {
            model_name
        }
    })
}

export function postParams(data) {
    return request({
        url: '/params',
        method: 'post',
        data: data
    })
}
