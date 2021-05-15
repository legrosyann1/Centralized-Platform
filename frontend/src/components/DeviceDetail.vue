<template>
  <v-dialog
    v-model="dialog"
    width="800"
    scrollable
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="primary"
        class="mb-3 ml-2"
        v-bind="attrs"
        v-on="on"
        small
      >
        Details
      </v-btn>
    </template>
    <v-tabs>
      <v-tab>Device details</v-tab>
      <v-tab>Interfaces</v-tab>
      <v-tab-item>
        <v-card>
          <v-card-text>
            <v-row>
              <v-col
                cols="6"
                v-for="(value, key) in details_items" 
                v-bind:key="key"
                >
                <v-text-field 
                  disabled
                  :v-model="key"
                  :label="key"
                  :value="value"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="dialog = false"
            >
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card>
          <v-data-table
            :headers="interface_headers"
            :items="interface_items"
            hide-default-footer
            class="elevation-1"
            v-if="interface_items.length != 0"
          >
          </v-data-table>
        <v-card-text v-else>No interfaces found</v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="dialog = false"
            >
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-tab-item>
    </v-tabs>
  </v-dialog>
</template>

<script>
import store from "../plugins/vuex.js";
import http from "../plugins/axios.js";

export default {
  name: "DeviceDetail",
  store,
  props: ['device'],
  data() {
    return {
        dialog: false,
        details_items: [],
        interface_items: null,
        details_except: ['id', 'created_at', 'updated_at', 'logic_partition', 'actions', 'interfaces'],
        interface_headers: [
          { text: "Name", value: "name" },
          { text: "IP Address", value: "ip_address" },
          { text: "Status", value: "status" },
        ],
    }
  },
  mounted(){
    this.showValues()
  },
  methods: {
    showValues() {
      var item = Object.assign({},this.device)
      for (const key in item) {
        if (Object.hasOwnProperty.call(item, key)) {
          if (this.details_except.includes(key)){
            delete item[key]
          }
        }
      }
      this.details_items = item
      this.getInterfaces()
    },

    getInterfaces(){
      var vm = this
      http
        .get('/devices/' + vm.device.id + '/interfaces')
        .then(function (response) {
          vm.interface_items = response.data;
          console.log(vm.interface_items);
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
}
</script>