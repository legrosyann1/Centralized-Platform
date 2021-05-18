<template>
  <v-app>
    <TopBar/>
    <SideBar v-if="shouldShowSidebar"></SideBar>
    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
    <v-tour name="myTour" :steps="steps" :options="optionsTour" :callbacks="callbacksTour">
      <template slot-scope="tour">
        <transition name="fade">
          <v-step
            v-if="tour.steps[tour.currentStep]"
            :key="tour.currentStep"
            :step="tour.steps[tour.currentStep]"
            :previous-step="tour.previousStep"
            :next-step="tour.nextStep"
            :stop="tour.stop"
            :skip="tour.skip"
            :is-first="tour.isFirst"
            :is-last="tour.isLast"
            :labels="tour.labels"
          >
          </v-step>
        </transition>
      </template>
    </v-tour>
  </v-app>
</template>

<script>
import TopBar from '@/components/TopBar.vue';
import SideBar from '@/components/SideBar.vue';
import store from './plugins/vuex.js';
import http from "./plugins/axios.js";

export default {
  name: 'App',
  store,
  components: {
    SideBar,
    TopBar,
  },
  data () {
    return {
      optionsTour: {
        useKeyboardNavigation: true,
        enableScrolling: false,
        highlight: true,
        labels: {
          buttonSkip: 'Skip tour',
          buttonPrevious: 'Previous',
          buttonNext: 'Next',
          buttonStop: 'Finish'
        }
      },
      callbacksTour: {
        onStart: this.startStepCallback,
        onPreviousStep: this.previousStepCallback,
        onNextStep: this.nextStepCallback,
      },
      steps: [
        {
          target: '#v-step-0',
          content: 'Lets start the Tour of <strong>Helios</strong>!<br>This is the menu (you can use the keyboard arrows to control the Tour).',
        },
        {
          target: '#v-step-1',
          content: 'In the Home page we find statistics about Helios'
        },
        {
          target: '#v-step-2',
          content: 'Total amount of devices in inventory'
        },
        {
          target: '#v-step-3',
          content: 'This section helps us manage Changes'
        },
        {
          target: '#v-step-4',
          content: 'New changes can be scheduled here'
        },
        {
          target: '#v-step-5',
          content: 'We find the inventory in the Devices section'
        },
        {
          target: '#v-step-6',
          content: 'You can change the fields displayed by clicking here',
          params: {highlight: false}
        },
        {
          target: '#v-step-7',
          content: 'You can add partitions and view the full details of the device',
          params: {highlight: false}
        },
        {
          target: '#v-step-8',
          content: 'You can perform diferent actions to devices in this section'
        },
        {
          target: '#v-step-9',
          content: 'This page connects to Ansible Tower'
        },
        {
          target: '#v-step-10',
          content: 'Characteristics about addressing in the network can be found in this section'
        },
        {
          target: '#v-step-11',
          content: 'You can send automation suggestions in the Email page'
        },
        {
          target: '#v-step-12',
          content: 'Read more about the page here'
        },
        {
          target: '#v-step-13',
          content: 'You can replay the Tour by clicking here'
        },
      ],
      drawerSteps: [0,1,3,5,8,9,10,11,12],
      drawerName: ['None', 'Home', 'Change Management', 'Devices', 'Operations Center', 'Tower Manager', 'Network Addressing', 'Email', 'About']
    }
  },
  computed:{
    shouldShowSidebar(){
      if (this.$store.state.isAuthenticated){
        return this.$route.meta.sidebar!==true;
      }else{
        return this.$route.meta.sidebar!==false;
      }
    }
  },
  methods: {
    previousStepCallback (currentStep) {   
      var index = this.drawerSteps.indexOf(currentStep)
      if (index != -1 && currentStep != 1){
        this.$router.push({name: this.drawerName[index-1]})
      }
      
      if (this.$vuetify.breakpoint.mdAndDown){
        if(this.drawerSteps.includes(currentStep-1)){
            this.$store.commit('stateDrawer', true);
        }else{
          this.$store.commit('stateDrawer', false);
        }          
      }
    },
    nextStepCallback (currentStep) {
      var index = this.drawerSteps.indexOf(currentStep+1)
      if (index != -1){
        this.$router.push({name: this.drawerName[index]})
      }

      if(this.$vuetify.breakpoint.mdAndDown){
        if(this.drawerSteps.includes(currentStep+1)){
          this.$store.commit('stateDrawer', true);
        }else{
          this.$store.commit('stateDrawer', false);
        }   
      }
    },
    startStepCallback () {   
      var vm = this;
      if(this.$vuetify.breakpoint.mdAndDown) {
        this.$store.commit('stateDrawer', true)
      }
      var profile = this.$store.state.authProfile;
      if (profile.viewTour == true){
        this.$store.commit('stateTour', false);
        profile.viewTour = false;

        http
          .put("/users/" + profile.id + "/", profile)
          .then(function (response) {
            vm.$store.commit('setAuthProfile', {
                "authProfile": response.data,
                "isAuthenticated": true
              });
          })
          .catch((e) => {
            console.log(e);
          });
      }
    }
  }
};
</script>

<style>
.v-tour__target--highlighted {
  box-shadow: 0 0 0 10px rgba(19, 2, 99, 0.4);
}
</style>
