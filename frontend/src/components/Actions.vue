<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="logs"
      :items-per-page="5"
      :loading="loading_logs"
      class="elevation-1 mt-2"
      @click:row="dialogLog"
    >
      <template #[`item.created_at`]="{item}">
        {{ formatDate(item.created_at) }}
      </template>
    </v-data-table>

    <!-- dialog results Log --->
    <v-dialog v-model="dialog_log" width="500">
      <v-card>
        <v-card-title class="text-h6 grey lighten-2">
          Result
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="mt-4">
          The result of {{selectedLog.action.name}} is
          <v-icon small>mdi-arrow-right-thick</v-icon>
          {{selectedLog.result}}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" outlined class="mt-n4 mb-2" @click="dialog_log = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-btn
      class="animacion mt-6"
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
          <v-form v-model="valid_device">
            <v-autocomplete
              chips
              clearable
              multiple
              small-chips
              :items="devices"
              :rules="rules"
              v-model="selectedDevices"
              :loading="loading"
            ></v-autocomplete>
          </v-form>
          <v-btn color="primary" :disabled="valid_device" class="mr-2" @click="steps = 2">
            Continue
          </v-btn>
          <v-btn color="primary" outlined @click="dialog = false">
            Cancel
          </v-btn>
        </v-stepper-content>

        <!-- STEP 2 -->
        <v-stepper-step :complete="steps > 2" step="2">
          Choose the action to perform
        </v-stepper-step>
        <v-stepper-content step="2">
          <v-form v-model="valid_action">
            <v-autocomplete
              chips
              clearable
              multiple
              small-chips
              :items="actions"
              item-text="name"
              :rules="rules"
              v-model="selectedActions"
              :loading="loading_actions"
            ></v-autocomplete>
          </v-form>
          <v-btn color="primary" :disabled="valid_action" @click="steps = 3">
            Continue
          </v-btn>
          <v-btn color="primary" class="mx-2" outlined @click="steps = 1">
            Back
          </v-btn>
          <v-btn color="primary" outlined @click="dialog=false">
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
            <v-list-item-content>- {{ device }}</v-list-item-content>
          </v-list-item>
          Actions to perform
          <v-list-item v-for="action in selectedActions" v-bind:key="action">
            <v-list-item-content>- {{ action }}</v-list-item-content>
          </v-list-item>
          <div class="mt-2">
            <v-btn color="primary" @click="doAction">
              Confirm and run
            </v-btn>
            <v-btn color="primary" class="mx-2" outlined @click="steps = 2">
              Back
            </v-btn>
            <v-btn color="primary" outlined @click="dialog = false">
              Cancel
            </v-btn>
          </div>
        </v-stepper-content>
      </v-stepper>
    </v-dialog>
    <template v-for="(response, index) in responses">
      <v-snackbar :key="index" min-width="800" v-model="dialog_result" multi-line timeout="-1" app light class="mb-5">
        <v-sheet min-width="450">
          <v-row justify="start">  
            <v-col cols="12" md="1" class="text-center">
              <v-icon color="success" class="mt-2">mdi-checkbox-marked-circle</v-icon>
            </v-col>
            <v-col cols="12" md="9" class="text-center">
              <span>{{response.title}}</span><br>
              <span>{{response.response}}</span>
            </v-col>
            <v-col cols="12" md="1" class="text-center">
              <v-btn color="red" text plain @click="removeResponse(index)">
                Close
              </v-btn>
            </v-col>
          </v-row>
        </v-sheet>
      </v-snackbar>
    </template>
  </div>
</template>

<script>
import http from "../plugins/axios.js";
import store from "../plugins/vuex.js";

export default {
  name: "Actions",
  store,
  data () {
    return {
      headers: [
        {text:'Operation', value: 'action.name'},
        {text:'Playbook', value: 'action.template'},
        {text:'User', value: 'user'},
        {text:'Execution date', value: 'created_at'}
      ],
      rules: [
          value => value.length == 0
      ],
      actions: [],
      devices: [],
      logs: [],
      selectedDevices: [],
      selectedActions: [],
      selectedLog: {'action':''},
      responses: [],
      valid_device: false,
      valid_action: false,
      dialog: false,
      dialog_log: false,
      dialog_result: false,
      steps: 1,
      ws: null,
      loading: false,
      loading_logs: false,
      loading_actions: false,
    }
  },

  mounted (){
    this.initWebsocket();
    this.getLogs()
    this.getDevices();
    this.getActions();
  },

  methods: {
    initWebsocket(){
      var vm = this
      var url = this.$store.state.endpoints.wsBaseUrl + '/actions/'
      vm.ws = new WebSocket(url);
      vm.ws.onmessage = function (response) {
        var resp = JSON.parse(response.data)
        console.log(resp)
        console.log(resp['type'])
        if (resp['type'] == 'ack'){
          if (resp['status'] == 'Accepted'){vm.dialog = false}
        }
        else if (resp['type'] == 'resp'){
          if (resp['status'] == 'successful'){
            vm.dialog_result = true
            var dict = {'title':resp['action'],'response':resp['resp']}
            vm.responses.push(dict)
          }
        }
      }
    },

    getDevices() {
      /*
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
        });*/
      this.devices=['localhost'];
      this.loading = false;
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
      vm.loading_actions = true
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
      this.ws.send(JSON.stringify({actions: this.selectedActions, devices: this.selectedDevices}))
    },

    formatDate(created_at){
      var date = new Date(created_at)
      console.log(date.toLocaleString())
      return date.toLocaleString()
    },

    dialogLog(item){
      this.selectedLog = item
      this.dialog_log = true
    },

    removeResponse(index){
      this.responses.splice(index, 1)
      if (this.responses.length() == 0){
        this.dialog_result = false
      }
    }
  },
}
</script>

<style>

</style>