<template>
  <div>
    <br>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="info"
          icon="mdi-poll"
          title="Devices"
          :value='devices'
          sub-icon="mdi-clock"
          sub-text="Just Updated"
          id="v-step-2"
        />
      </v-col>
        
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="#4CA"
          icon="mdi-gesture-double-tap"
          title="Actions completed"
          :value="actions"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="#BF3"
          icon="mdi-alarm-light"
          title="EOL"
          :value="eol"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          id = "eol"
          class="v-cards-top animacion"
          width="400px"
          color="#607"
          icon="mdi-account-multiple"
          title="Users"
          :value="users"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row justify="space-around" class="mx-10">
      <v-col cols="12" md="5" lg="5">
        <MaterialStatsCard
          id = "eol"
          class="v-cards-top animacion"
          color="#607"
          icon="mdi-alarm-check"
          title="Sheduled tasks"
          :value="tasks"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
      <v-col cols="12" md="5" lg="5">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="#789"
          icon="mdi-alert-circle"
          title="Untracked device changes"
          :value="changes"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
    </v-row>
  </div>
</template>


<script>
import MaterialStatsCard from "./MaterialStatsCard";
import gsap from "gsap";
import http from "../plugins/axios.js";
export default {
  name: "HomeStats",
  components: {
    MaterialStatsCard,
  },
data: () => ({
    devices:'-',
    eol:'-',
    actions:'-',
    users:'-',
    tasks:'-',
    changes:'-',
    loading:true
  }),
  created(){
    this.getMetrics()
  },
  mounted() {
    this.animation();
    if(this.$store.state.tour == true){
      this.$tours['myTour'].start()
    }
  },

  methods:{
    getMetrics(){
      var vm = this
      http
        .get("/metrics")
        .then(function (response) {
            console.log(response.data)
            vm.parseData(response.data)
            vm.loading = false
        });
    },
    
    parseData(data){
      this.devices = data['devices'].toString()
      this.eol = (data['devicesHWEndOfLife'] + data['devicesSWEndOfLife']).toString()
      this.actions = data['actionsCompleted'].toString()
      this.users = data['users'].toString()
      this.tasks = data['enabledTasks'].toString()
      this.changes = data['untrackedChanges'].toString()
    },

    animation() {
      gsap.from(".animacion", {
        duration: 0.3,
        y: -100,
        scale: 0,
        opacity: 0,
        stagger: 0.3,
      });
    },
  },
};

</script>

<style>
.v-cards-top {
  margin-top: 60px;
}
.v-sheet--offset {
    top: -20px;
    position: relative;
  }
</style>
