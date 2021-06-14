<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="logs"
      :items-per-page="5"
      :loading="loading_logs"
      class="elevation-1"
    >
      <template #item.updated_at="{value}">
        {{ formatDate(value) }}
      </template>
    </v-data-table>
    <v-btn
      class="animacion"
      color="primary"
      @click="steps=1; dialog=true"
    >
      New action
    </v-btn>
    <v-dialog v-model="dialog" width="800">
      <v-stepper v-model="steps" vertical class="animacion">
        <!-- STEP 1 -->
        <v-stepper-step :complete="steps > 1" step="1">
          Select device or group to perform the action
          <small>You can choose to execute the action in a single device or in group</small>
        </v-stepper-step>
        <v-stepper-content step="1">
          <v-autocomplete
            chips
            clearable
            multiple
            small-chips
            :items="devices"
            v-model="selectedDevices"
            :loading="loading"
          ></v-autocomplete>
          <v-btn color="primary" @click="steps = 2">
            Continue
          </v-btn>
          <v-btn @click="dialog = false" text>
            Cancel
          </v-btn>
        </v-stepper-content>

        <!-- STEP 2 -->
        <v-stepper-step :complete="steps > 2" step="2">
          Choose the action to perform
        </v-stepper-step>
        <v-stepper-content step="2">
          <v-autocomplete
            chips
            clearable
            multiple
            small-chips
            :items="actions"
            v-model="selectedActions"
            :loading="loading_actions"
          ></v-autocomplete>
          <v-btn color="primary" @click="steps = 3">
            Continue
          </v-btn>
          <v-btn text @click="dialog=false">
            Cancel
          </v-btn>
        </v-stepper-content>

        <!-- STEP 3 -->
        <v-stepper-step :complete="steps > 3" step="3">
          Summary
        </v-stepper-step>
        <v-stepper-content step="3">
          Devices affected
          <v-list-item v-for="device in selectedDevices" v-bind:key="device">
            <v-list-item-content>
              <v-list-item-text>{{ device }}</v-list-item-text>
            </v-list-item-content>
          </v-list-item>
          Actions to perform
          <v-list-item v-for="action in selectedActions" v-bind:key="action">
            <v-list-item-content>
              <v-list-item-text>{{ action }}</v-list-item-text>
            </v-list-item-content>
          </v-list-item>
          <v-btn color="primary" @click="doAction">
            Confirm and run
          </v-btn>
          <v-btn text @click="dialog = false">
            Cancel
          </v-btn>
        </v-stepper-content>
      </v-stepper>
    </v-dialog>
    <v-snackbar v-model="dialog_result" timeout="10000" app light class="mb-5">
      <div class="text-center" id="result_container">
        <v-icon color="success" class="ml-1">mdi-checkbox-marked-circle</v-icon>
      </div>
    </v-snackbar>
  </div>
</template>

<script>
import http from "../plugins/axios.js";

export default {
  name: "Actions",
  store,
  data () {
    return {
      headers: [
        {text:'Operation', value: 'action.name'},
        {text: 'Playbook', value: 'action.template'},
        {text:'User', value: 'user'},
        {text: 'Execution date', value: 'updated_at'}
      ],
      actions: [],
      devices: [],
      logs: [],
      selectedDevices: [],
      selectedActions: [],
      dialog: false,
      dialog_result: true,
      steps: 1,
      ws: null,
      loading_logs: false,
      loading_actions: false,
    }
  },

  created (){
    this.getLogs()
    this.getDevices();
    this.getActions();
    this.initWebsocket();
  },

  methods: {
    initWebsocket(){
      var vm = this
      var url = this.$store.state.endpoints.wsBaseUrl + '/actions/'
      vm.ws = new WebSocket(url);
      vm.ws.onmessage = function (resp) {
        console.log(resp.data);
        vm.dialog_result = true
        var res_container = document.getElementById('result_container')
        res_container.innerHTML += '<span>' + resp.data + '</span>'
      }
    },

    getDevices() {
      var vm = this;
      vm.loading = true
      http
        .get("/devices")
        .then(function (response) {
          response.data.forEach(element => {
            element.text = element.name + ' - ' + element.ip_address
            element.value = element.ip_address               
          });
          vm.devices = response.data
          vm.loading = false
        })
        .catch((e) => {
          console.log(e);
          vm.loading = false
        });
    },

    getLogs() {
      var vm = this;
      (vm.loading_logs = true),
        http
          .get("/logActions")
          .then(function (response) {
            vm.logs = response.data;
            vm.loading_logs = false
          })
          .catch((e) => {
            console.log(e);
            vm.loading_logs = false
          });
    },

    getActions() {
      var vm = this;
      vm.loading = true
      http
        .get("/actions")
        .then(function (response) {
          vm.actions = response.data
          vm.loading_actions = false
        })
        .catch((e) => {
          console.log(e);
          vm.loading_actions = false
        });
    },

    doAction(){
      console.log(this.selectedDevices)
      console.log(this.selectedActions)
      this.dialog = false
      //this.ws.send(JSON.stringify({actions: ['ping'], devices: ['8.8.8.8']}))
      this.ws.send(JSON.stringify({actions: this.selectedActions, devices: this.selectedDevices}))
    },

    formatDate(updated_at){
      var date = new Date(updated_at)
      return date.toLocaleString()
    },
  },
}
</script>