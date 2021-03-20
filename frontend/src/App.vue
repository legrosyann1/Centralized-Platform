<template>
  <v-app>
    <TopBar/>
    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import TopBar from '@/components/TopBar.vue';
import store from './plugins/vuex.js';

export default {
  name: 'App',
  store,

  components: {
    TopBar,
  },

  data: () => ({
    //
  }),
};
</script>
