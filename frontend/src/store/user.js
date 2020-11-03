import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router, { resetRouter } from '@/router'

const actions = {
    // user login
    login({ commit }, userInfo) {
      cconsole.log('set info')
      const { username, password } = userInfo
      cconsole.log('set info')
      return new Promise((resolve, reject) => {
        login({ username: username.trim(), password: password }).then(response => {
          const { data } = response
          commit('SET_TOKEN', "JWT " + data.token)
          setToken(data.token)
          resolve()
        }).catch(error => {
          console.log('login err')
          reject(error)
        })
      })
    }
}