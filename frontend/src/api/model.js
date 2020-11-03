import request from '@/utils/request'

export function getModels(params) {
    return request({
        url: '/models',
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

export function getParams(params) {
    return request({
        url: '/params',
        method: 'get',
        params
    })
}

export function postParams(data) {
    return request({
        url: '/params',
        method: 'post',
        data: data
    })
}
