<template>
  <v-btn v-if="$store.state.isAuthenticated" @click="logout">Logout</v-btn>
</template>

<script>
import store from '../plugins/vuex.js';

export default {
  name: 'Logout',
  store,
  methods: {
    logout() {
      this.$tours['myTour'].stop()
      this.$store.commit('setAuthProfile', {
          "authProfile": null,
          "isAuthenticated": false
      });
      this.$store.commit('removeToken');
      this.$store.commit('stateTour', null);
      this.$router.push({name: 'Login'})
    }
  }
}
</script>