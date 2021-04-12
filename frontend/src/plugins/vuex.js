import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

var apiBaseUrl = 'http://127.0.0.1:8000/api/';

export default new Vuex.Store({
  state: {
    authUser: {},
    isAuthenticated: false,
    jwt: localStorage.getItem('token'),
    drawer: null,
    endpoints: {
      obtainJWT: apiBaseUrl + 'obtain_token',
      refreshJWT: apiBaseUrl + 'refresh_token',
      baseUrl: apiBaseUrl,
    },
    totaldevices: null,
  },
  mutations: {
    setAuthUser(state, {
      authUser,
      isAuthenticated
    }) {
      Vue.set(state, 'authUser', authUser)
      Vue.set(state, 'isAuthenticated', isAuthenticated)
    },
    updateToken(state, newToken) {
      // TODO: For security purposes, take localStorage out of the project.
      localStorage.setItem('token', newToken);
      state.jwt = newToken;
    },
    removeToken(state) {
      // TODO: For security purposes, take localStorage out of the project.
      localStorage.removeItem('token');
      state.jwt = null;
    }
  }
})