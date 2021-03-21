<template>
  <v-app>
    <TopBar/>
    <SideBar v-if="shouldShowSidebar"></SideBar>
    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import TopBar from '@/components/TopBar.vue';
import SideBar from '@/components/SideBar.vue';
import store from './plugins/vuex.js';

export default {
  name: 'App',
  store,

  components: {
    TopBar,
    SideBar,
  },

  computed:{
    shouldShowSidebar(){
      if (this.$store.state.isAuthenticated){
        return this.$route.meta.sidebar!==true;
      }else{
        return this.$route.meta.sidebar!==false;
      }
    }
  }
};
</script>
