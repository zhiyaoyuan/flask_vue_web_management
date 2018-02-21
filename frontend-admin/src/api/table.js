import request from '@/utils/request'
import { getToken, setToken, removeToken } from '@/utils/auth'

export function getList(params) {
  return request({
    url: '/user/list',
    method: 'get',
    params: { 'token': getToken() }
  })
}
