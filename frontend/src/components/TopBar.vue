<template>
  <v-app-bar app clipped-left color="primary" dark>
    <v-app-bar-nav-icon 
      v-if="this.$vuetify.breakpoint.mdAndDown && this.$store.state.isAuthenticated" 
      @click.stop="$store.state.drawer = !$store.state.drawer"
    >
    </v-app-bar-nav-icon>
    <div class="d-flex align-center">
      <router-link to="/Home">
        <v-img
          alt="Helios logo"
          class="shrink ml-2 img"
          contain
          src="../assets/logo_white_large.png"
          transition="scale-transition"
          width="130"
        />
      </router-link>
    </div>
    <v-spacer></v-spacer>
    <div>
      <v-btn @click="startTour" v-if="$store.state.isAuthenticated" id="v-step-14" icon>
        <v-icon>mdi-help-circle-outline</v-icon>
      </v-btn>
    </div>
    <div v-if="$store.state.isAuthenticated" class="mr-8 ml-4 text-button">
      <v-icon>mdi-account</v-icon>
      {{ $store.state.authProfile.user.first_name.substring(0,1) }}{{ $store.state.authProfile.user.last_name.substring(0,1) }}
    </div>
    <Logout/>
  </v-app-bar>
</template>

<script>
import Logout from "./Logout.vue";
export default {
  name: "TopBar",
  components: {
    Logout,
  },
  methods: {
    startTour(){
      this.$tours['myTour'].start()
    }
  },
};
</script>