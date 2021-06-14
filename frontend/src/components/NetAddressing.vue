<template>
  <div class="mx-auto">
    <v-row>
      <v-col>
        <h2 class="text-h4 mb-6 animacion marge">{{ this.$route.name }}</h2>
      </v-col>
      <v-col cols="auto" class="mr-16">
        <v-text-field
          class="marge animacion"
          id="search"
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12">
        <v-data-table
          v-model="selected"
          :search="search"
          :headers="headers"
          :items="items"
          :items-per-page="10"
          :single-select="singleSelect"
          class="elevation-1 animacion mx-3"
          show-select
          item-key="name"
          :loading="loading"
          loading-text="Loading... Please wait"
        >

          <!--  Endpoint dialog  -->
          <template v-slot:[`item.actions`]="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" v-bind="attrs" v-on="on" icon id="v-step-12">
                  <v-icon size="20" :id="item" @click="dialogEndpoint(item)"
                    >mdi-lan</v-icon
                  >
                </v-btn>
              </template>
              <span>Add endpoint</span>
            </v-tooltip>
          </template>
        </v-data-table>

        <!-- Dialog for endpoint -->
        <v-dialog v-model="dialog_endpoint" max-width="1000px">
          <v-card>
            <v-list>
              <v-list-item>
                <v-list-item-title> SELECT ENDPOINT </v-list-item-title>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list>
              <v-list-item>
                <v-spacer></v-spacer>
                <v-autocomplete
                  clearable
                  item-text="network_address"
                  :items="items"
                  v-model="endpoint"
                  class="mb-5"
                  return-object
                  @change="addEndpoint()"
                ></v-autocomplete>
                <v-spacer></v-spacer>
              </v-list-item>
            </v-list>
            <v-container>
              <v-row no-gutters>
                <template v-for="(fields, index) in endpoints">
                  <v-col :key="index" class="my-3 text-center">
                    <template v-if="fields != null">{{ fields }}</template>
                  </v-col>
                  <v-responsive
                    v-if="index === 5"
                    :key="`width-${index}`"
                    width="100%"
                  ></v-responsive>
                </template>
              </v-row>
            </v-container>
          </v-card>
        </v-dialog>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  
    <v-row>
      <!-- Export buttons to excel/pdf -->
      <v-col cols="auto" class="marge">
        <v-menu offset-x close-on-content-click>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              v-bind="attrs"
              v-on="on"
              class="animacion"
              small
            >
              Export to
              <v-icon id="exportIcon">mdi-export</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-title>
                <v-btn
                  id="exportPdf"
                  text
                  small
                  depressed
                  @click="exportTo(true)"
                  :loading="loading_pdf"
                  :disabled="loading_pdf"
                >
                  <v-icon> mdi-file-pdf </v-icon>
                  PDF</v-btn
                >
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>
                <v-btn
                  id="exportExcel"
                  small
                  text
                  depressed
                  @click="exportTo(false)"
                  :loading="loading_excel"
                  :disabled="loading_excel"
                >
                  <v-icon> mdi-file-excel </v-icon>
                  EXCEL</v-btn
                >
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="auto">
        <v-alert v-if="error" color="red" dense dismissible type="error" class="mr-10 text-body-2"
          >{{ errorMessage }}</v-alert
        >
      </v-col>
    </v-row>
  </div>
</template>

<script>
import store from "../plugins/vuex.js";
import http from "../plugins/axios.js";
import gsap from "gsap";
import jsPDF from "jspdf";
import "jspdf-autotable";
import XLSX from "xlsx";

export default {
  name: "NetAddressing",
  store,
  data() {
    return {
      title: "Network Addressing",
      network: null,
      dialog_endpoint: false,
      search: "",
      singleSelect: false,
      endpoint: null,
      endpoints: ['Source', 'Zone','FW Source', 'FW Dest', 'Zone', 'Destination', null, null, null, null, null, null],
      selected: [],
      headers: [
        { text: "Network", value: "network_address" },
        { text: "Netmask", value: "netmask" },
        { text: "Vlan", value: "vlan"},
        { text: "VRF", value: "vrf" },
        { text: "Zone", value: "zone" },
        { text: "FW Source", value: "firewall" },
        { text: "", value: "actions", align: "center" , sortable: false},
      ],
      header_endpoints: [
        { text: 'Source', value: 'sourceNet' },
        { text: 'Zone', value: 'sourceZone' },
        { text: 'FW Source', value: 'sourceFW' },
        { text: 'FW Dest', value: 'destFW' },
        { text: 'Zone', value: 'destZone' },
        { text: 'Destination', value: 'destNet' },
      ],
      items: [],
      loading: false,
      loading_pdf: false,
      loading_excel: false,
      error: false,
      errorMessage: '',
    };
  },

  mounted() {
    this.animation();
    this.getNetworks();
  },

  methods: {
    animation() {
      gsap.from(".animacion", {
        duration: 0.3,
        y: -100,
        scale: 0,
        opacity: 0,
        stagger: 0.3,
      });
    },

    exportTo(value) {
      var vm = this;

      if (value == false){
        vm.loading_excel = true
        var data_xls = "";
        if (vm.selected.length == 0) {
          data_xls = XLSX.utils.json_to_sheet(vm.items);
          console.log(vm.items);
        } else {
          data_xls = XLSX.utils.json_to_sheet(vm.selected);
          console.log(vm.selected);
        }
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, data_xls, 'Netowrks');
        XLSX.writeFile(workbook, 'Networks.xlsx')
        vm.loading_excel = false
      } 
      
      else if (value == true){
        vm.loading_pdf = true;
        var columns = [];
        var data = [];
        for (var i = 0; i < vm.headers.length - 1; i++) {
          columns.push(vm.headers[i].text);
        }
        if (vm.selected.length == 0) {
          data = vm.listDevices(vm.items);
        } else if (vm.selected.length != 0) {
          data = vm.listDevices(vm.selected);
        }
        var doc = new jsPDF();
        var pageNumber = doc.internal.getNumberOfPages();
        doc.autoTable({
          head: [columns],
          body: data,
          headStyles: {
            halign: "center",
          },
          styles: {
            fontSize: 7,
            lineWidth: 1,
            lineColor: [1, 148, 196],
            cellPaddin: 5,
            fontStyle: "bold",
            font: "helvetica",
          },
          columnStyles: {
            1: { halign: "center" },
            2: { halign: "center", cellWidth: 30},
            3: { halign: "center", cellWidth: 30},
            4: { halign: "center" },
            5: { halign: "center" },
            6: { halign: "center" },
          },
        });
        doc.setPage(pageNumber);
        doc.save("Networks.pdf");
        vm.loading_pdf = false;
      }
    },

    listDevices(devices) {
      var list_devices = [];
      for (var i = 0; i < devices.length; i++) {
        var device = []
        for (var j = 0; j < this.headers.length - 1; j++){
          device.push(devices[i][this.headers[j].value])
        }
        list_devices.push(device);
      }
      return list_devices;
    },

    getNetworks() {
      var vm = this;
      vm.loading = true
      http
        .get("/networks")
        .then(function (response) {
          vm.items = response.data;
          console.log(response.data)
          vm.loading = false;
        })
        .catch((e) => {
          console.log(e);
          vm.errorMessage = 'Update failed'
          vm.error = true;
          vm.loading = false;
        });
    },

    addEndpoint(){
      this.endpoints[11] = this.endpoint.network_address.concat('/',this.endpoint.netmask);
      if (this.endpoint.zone !== ''){
        this.endpoints[10] = this.endpoint.zone;
      }
      if (this.endpoint.fw_source !== ''){
        this.endpoints[9] = this.endpoint.firewall;
      }
    },

    dialogEndpoint: function (value) {
      this.dialog_endpoint = true;
      this.network = value;
      this.endpoints[6] = value.network_address.concat('/',value.netmask);
      if (value.zone !== ''){
        this.endpoints[7] = value.zone;
      }
      if (value.fw_source !== ''){
        this.endpoints[8] = value.firewall;
      }
    },
  },
};
</script>


<style>
.marge {
  padding-left: 5%;
}
#exportPdf {
  background: rgb(235, 16, 0);
  color: white;
}
#exportExcel {
  background: rgb(1, 114, 58);
  color: white;
}
#exportIcon {
  margin-left: 10px;
}
</style>