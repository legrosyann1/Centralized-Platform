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
    name:"FormLogin",

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

      axios
        .post(this.$store.state.endpoints.obtainJWT, {
          "username": this.username,
          "password": this.password
        })
        .then((response) => {
          this.$store.commit('updateToken', response.data.token);
          this.$store.commit('setAuthUser', {
            "authUser": this.username,
            "isAuthenticated": true
          });
          this.$router.push({name: 'Home'})
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