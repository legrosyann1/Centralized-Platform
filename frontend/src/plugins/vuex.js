import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//var apiBaseUrl = 'http://127.0.0.1:8000/api/';
var apiBaseUrl = document.location.protocol + '//' + window.location.host.split(':')[0] + ':8000/api'
var wsBaseUrl = 'ws://' + window.location.host.split(':')[0] + ':8000/ws'

export default new Vuex.Store({
  state: {
    authProfile: {},
    isAuthenticated: false,
    jwt: localStorage.getItem('token'),
    drawer: null,
    tour: null,
    endpoints: {
      obtainJWT: apiBaseUrl + '/obtain_token',
      refreshJWT: apiBaseUrl + '/refresh_token',
      baseUrl: apiBaseUrl,
      wsBaseUrl: wsBaseUrl,
    },
  },
  mutations: {
    setAuthProfile(state, {
      authProfile,
      isAuthenticated
    }) {
      Vue.set(state, 'authProfile', authProfile)
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
    },
    stateDrawer(state, drawer){
      state.drawer = drawer
    },
    stateTour(state, tour){
      state.tour = tour
    }
  }
})