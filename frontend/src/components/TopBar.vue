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
    <div v-if="$store.state.isAuthenticated">
      <v-menu 
        offset-y
        open-on-hover
        close-on-content-click
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn 
            text 
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-account</v-icon>
            {{ $store.state.authUser.username}}
          </v-btn>
        </template>
        <v-list>
          <v-list-item
          v-for="(item, index) in items_btn"
          :key="index">
            <v-list-item-title>
              <v-btn
                text 
                @click="click_btn(item)"
                right
              >
              {{ item.title }}
              </v-btn>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
  </v-app-bar>
</template>

<script>
export default {
  name: "TopBar",
  data() {
    return{
      items_btn: [{ title: "Preferences" }, { title: "Logout" }]
    }
    
  },
  methods: {
    click_btn(item){
      if(item.title == 'Logout'){
        this.$store.commit('setAuthUser', {
          "authUser": null,
          "isAuthenticated": false
        });
        this.$store.commit('removeToken');
        this.$router.push({name: 'Login'})
      }
    }
  },
};
</script>