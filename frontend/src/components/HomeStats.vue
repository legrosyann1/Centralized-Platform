<template>
  <div>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="info"
          icon="mdi-poll"
          title="Devices"
          v-bind:value='devices'
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
        
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="#4CA"
          icon="mdi-gesture-double-tap"
          title="Actions done"
          value="-"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="#BF3"
          icon="mdi-alert-octagon"
          title="Actions incompleted"
          value="-"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          class="v-cards-top animacion"
          color="#789"
          icon="mdi-database-arrow-down"
          title="Downloaded Backups"
          value="-"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <br><br>
    <v-row justify="space-around">
      <v-col cols="12" md="7">
        <v-card class="pa-2 animacion" outlined tile>
          <v-sheet
            class="v-sheet--offset mx-auto"
            color="cyan"
            elevation="12"
            max-width="calc(100% - 32px)"
          >
            <v-sparkline
              :labels="labels"
              :value="value"
              color="white"
              line-width="2"
              padding="16"
            ></v-sparkline>
          </v-sheet>

          <v-card-text class="pt-0">
            <div class="title font-weight-light mb-2">User Registrations</div>
            <div class="subheading font-weight-light grey--text">
              Last Campaign Performance
            </div>
            <v-divider class="my-2"></v-divider>
            <v-icon class="mr-2" small> mdi-clock </v-icon>
            <span class="caption grey--text font-weight-light"
              >last registration 26 minutes ago</span
            >
          </v-card-text>
        </v-card>
      </v-col>
       <v-col cols="12" md="4">
        <MaterialStatsCard
          id = "eol"
          class="v-cards-top animacion"
          width="400px"
          color="#607"
          icon="mdi-lifebuoy"
          title="EOL"
          value="-"
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
    labels: ["12am", "3am", "6am", "9am", "12pm", "3pm", "6pm", "9pm"],
    value: [200, 675, 410, 390, 310, 460, 250, 240],
    devices:'-',
    items_eol:'-',
    loading:true
  }),
  created(){
    this.getMetrics()
  },
  mounted() {
    this.animation();
  },

  methods:{
    getMetrics(){
      var vm = this
      http
        .get("/metrics")
        .then(function (response) {
            console.log(response.data)
            vm.devices = response.data.devices.toString();
            vm.loading = false
        });
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
