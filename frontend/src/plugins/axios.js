import axios from "axios";
import store from '../plugins/vuex.js';

var jwt = 'JWT ' + store.state.jwt
const http = axios.create({
  baseURL: store.state.endpoints.baseUrl,
  headers: {
    "Content-type": "application/json",
    "Authorization": jwt
  }
});

http.interceptors.request.use(function (response) {
  // Return a successful response back to the calling service
  return response;
}, function (error) {
  // Return any error which is not due to authentication back to the calling service
  if (error.response.status !== 401) {
    return new Promise((resolve, reject) => {
      reject(error);
    });
  }

  // Logout user if token refresh didn't work or user is disabled
  if (error.config.url == '/refresh_token' || error.response.message == 'Account is disabled.') {
    this.$store.commit('removeToken');
    this.$store.commit('setAuthProfile', {
      "authProfile": {},
      "isAuthenticated": false
    });
    this.$router.push({ name: 'Login' });
    return new Promise((resolve, reject) => {
      reject(error);
    });
  }

  // Try request again with new token
  axios
    .post(this.$store.state.endpoints.obtainJWT, {
      "username": this.$store.state.authProfile.user.username,
      "password": this.$store.state.authProfile.user.password
    })
    .then((response) => {
      this.$store.commit('updateToken', response.data.token);
      http.defaults.headers.common['Authorization'] = response.data.token;
      return response;
    })
    .catch((error) => {
      this.$store.commit('removeToken');
      this.$store.commit('setAuthProfile', {
        "authProfile": {},
        "isAuthenticated": false
      });
      this.$router.push({name: 'Login'})
      Promise.reject(error);
    })
});

export default http
