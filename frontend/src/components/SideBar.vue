<template>
  <v-navigation-drawer
    floating
    clipped
    app
    :expand-on-hover="expand"
    :mini-variant.sync="mini"
    v-model="$store.state.drawer"
  >
    <v-list nav dense v-if="$store.state.isAuthenticated" id="v-step-0">
      <v-list-item
        v-for="route in $router.options.routes"
        v-show="route.meta.sidebar != false"
        :key="route.path"
        link
        :to="route.path"
        :id="route.id"
      >
        <v-list-item-icon>
          <v-icon>{{ route.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title>
          {{ route.name }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
    <v-spacer></v-spacer>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "SideBar",
  data () {
    return {
      mini: !this.$vuetify.breakpoint.mdAndDown,
      expand: !this.$vuetify.breakpoint.mdAndDown,
    }
  }
};
</script>