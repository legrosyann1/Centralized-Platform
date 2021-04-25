<template>
  <div class="mt-14" v-if="!isAuthenticated">
    <v-form lazy-validation>
      <v-container>
        <!--v-row>
          <v-spacer></v-spacer>
          <v-col cols="auto">
            <v-img class= "animacion" src="../assets/logo_large.png" width="270px"></v-img>
            <br>
          </v-col>
          <v-spacer></v-spacer>
        </v-row-->
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="10" sm="6">
            <v-text-field
              class= "animacion"
              v-model="username"
              label="Username"
              outlined
              required
              @keyup.enter="authenticate"
            ></v-text-field>
          </v-col>
          <v-spacer></v-spacer>
        </v-row>
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="10" sm="6">
            <v-text-field
              class= "animacion"
              :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
              v-model="password"
              label="Password"
              outlined
              required
              :type="show ? 'text' : 'password'"
              @click:append="show = !show"
              @keyup.enter="authenticate"
            ></v-text-field>
          </v-col>
          <v-spacer></v-spacer>
        </v-row>
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="auto">
            <v-btn  class="animacion" color="success" v-on:click="authenticate">LOGIN</v-btn>
          </v-col>
          <v-spacer></v-spacer>
        </v-row>
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="auto">
            <p v-if="error" id="error">Error in login</p>
          </v-col>
          <v-spacer></v-spacer>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script>
import axios from 'axios';
import gsap from 'gsap';

export default {
  name:"LoginForm",
  data() {
    return {
      username: 'yannlegros',
      password: 'Irlanda15',
      show: false,
      error: false,
      isAuthenticated: false,
    }
  },

  mounted() {
    this.animation();
  },

  methods: {
    animation (){
      gsap.from('.animacion',{
        duration: .3,
        y: -100,
        scale: 0,
        opacity:0,
        stagger:0.3
      })
    },

    authenticate(){
      var vm = this;
      axios
        .post(this.$store.state.endpoints.obtainJWT, {
          "username": vm.username,
          "password": vm.password
        })
        .then((response) => {
          this.$store.commit('updateToken', response.data.token);
          
          const base = {
            baseURL: this.$store.state.endpoints.baseUrl,
            headers: {
              Authorization: `JWT ${this.$store.state.jwt}`,
              'Content-Type': 'application/json'
            },
          }
          const axiosInstance = axios.create(base)
            axiosInstance({
              url: "/users",
              method: "get",
              params: {}
            })
            .then(function (response){
              var profiles = response.data;
              var profile = null
              profiles.forEach((element) => {
                if (element.user.username == vm.username){
                  profile = element
                }
              })
              profile.user['password'] = vm.password;
              vm.$store.commit('setAuthProfile', {
                "authProfile": profile,
                "isAuthenticated": true
              });
              vm.$router.push({name: 'Home'})
            })
        })
        .catch((error) => {
          console.log(error);
          this.error = true;
        })
    }
  }
}
</script>

<style>
#error{
  color:#ff4a96;
}
</style>