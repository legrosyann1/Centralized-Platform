<template>
  <div class="mx-auto">
    <v-row>
      <v-col>
        <h2 class="text-h4 mt-2 animacion marge">{{ this.$route.name }}</h2>
      </v-col>
      <v-col cols="auto" class="mr-14">
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
          class="elevation-1 animacion mx-3 text-body-2"
          show-select
          dense
          item-key="name"
          :loading="loading"
          loading-text="Loading... Please wait"
          :single-expand="singleExpand"
          :expanded.sync="expanded"
          show-expand
        >
          <!-- set status -->
          <template v-slot:[`item.status`]="{ item }">
              <v-btn
                :id="item"
                @click="dialogStatus(item)"
                icon
              >
                <v-icon small color="green darken-1" v-if="item['status'] === 'stable'">mdi-check-circle-outline</v-icon>
                <v-icon small color="orange darkne-2" v-if="item['status'] === 'unstable'">mdi-alert-circle-outline</v-icon>
                <v-icon small color="red" v-if="item['status'] === 'critical'">mdi-alert-circle</v-icon>
              </v-btn>
          </template>

          <!-- Change date format -->
          <template v-slot:[`item.sw_end_of_life`]="{ item }">
            {{ item.sw_end_of_life.substr(0, 10) }}
          </template>
          <template v-slot:[`item.hw_end_of_life`]="{ item }">
            {{ item.hw_end_of_life.substr(0, 10) }}
          </template>

          <!-- Icon to select columns to display -->
          <template v-slot:[`header.data-table-expand`]="">
            <v-btn
              @click="dialog_costumHeaders = true"
              icon
              id="v-step-6"
            >
              <v-icon small color="primary">mdi-pencil</v-icon>
            </v-btn>
          </template>
          

          <!-- Expand to show logical partitions -->
          <template v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length">
              <div v-if="item.logic_partition.length > 0">
                <div class="text-h6 mt-6">Logical Partitions</div>
                  <v-row class="ma-3">
                    <v-chip
                      class="ma-2"
                      label
                      v-for="partition in item.logic_partition" 
                      :key="partition.id"
                    >
                      {{ partition.name }}
                    </v-chip>
                  </v-row>
                </div>
              <div v-else class="text-body-2 mt-3">This device doesn't have any logical partition</div>
              <v-btn
                class="mb-3"
                small
                color="success"
                @click="editPartitions(item)"
              >
                <v-icon left>
                  mdi-pencil
                </v-icon>
                Edit
              </v-btn>
              <DeviceDetail v-bind:device="item"></DeviceDetail>
            </td>
          </template>

          <!--  when you click on any icon, one dialog is showed  -->
          <template #[`item.actions`]="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" v-bind="attrs" v-on="on" icon>
                  <v-icon small :id="item" @click="dialogActions(item)"
                    >mdi-tools</v-icon
                  >
                </v-btn>
              </template>
              <span>Quick actions</span>
            </v-tooltip>

            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" class="mx-n3" v-bind="attrs" v-on="on" icon>
                  <v-icon small :id="item" @click="databaseActions(item)"
                    >mdi-database-search-outline</v-icon
                  >
                </v-btn>
              </template>
              <span>Database actions</span>
            </v-tooltip>

            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" v-bind="attrs" v-on="on" icon>
                  <v-icon small :id="item" @click="dialogComments(item)"
                    >mdi-comment-text</v-icon
                  >
                </v-btn>
              </template>
              <span>Comments</span>
            </v-tooltip>
          </template>
        </v-data-table>

        <template #[`item.data-table-expand`]="{expand, isExpanded, item}">
          <v-icon @click.stop="expand(!isExpanded)" :color="item.logic_partition.length === 0? 'secondary' : 'primary'" id="v-step-7">
            $expand
          </v-icon>
        </template>

        <!-- Dialog for Costumizing Columns -->
        <v-dialog v-model="dialog_costumHeaders" max-width="700px">
          <v-card class="mx-auto">
            <v-card-title>
              <h2 class="title">Choose headers to be displayed</h2>
            </v-card-title>
            <v-divider></v-divider>
            <v-chip-group column multiple class="mx-5 mt-3" v-model="selected_headers" max="9">
              <template v-for="(col, index) in list_headers" >
                <v-chip filter outlined v-bind:key="index" v-if="col.value !== 'actions' && col.value !== 'data-table-expand'">
                  {{ col.text }}
                </v-chip>
              </template>
            </v-chip-group>
            <v-card-actions>
              <v-card-text v-if="selected_headers.length === 9" color="red" class="text-caption">
                Can't select more than 9 items
              </v-card-text>
              <v-spacer></v-spacer>
              <v-btn small color="primary" class="mb-3" @click="changeHeaders">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Dialog for Status -->
        <v-dialog v-model="dialog_status" max-width="350px">
          <v-card>
            <v-alert border="bottom" color="blue-grey" dark align="center">
              What is the status of this device?
            </v-alert>
            <v-card-actions class="mt-n3">
              <v-spacer></v-spacer>
              <v-btn color="green" @click="setStatus('stable')">Stable</v-btn>
              <v-btn color="orange darken-1" @click="setStatus('unstable')">Unstable</v-btn>
              <v-btn color="red" @click="setStatus('critical')">Critical</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
            <v-spacer></v-spacer>
          </v-card>
        </v-dialog>

        <!-- Dialog for quick actions -->
        <v-dialog v-model="dialog_actions" max-width="500px">
          <v-card>
            <v-list>
              <v-list-item>
                <v-list-item-title> QUICK ACTIONS </v-list-item-title>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list>
              <v-list-item>
                <v-list-item-action>
                  <v-checkbox color="primary"></v-checkbox>
                </v-list-item-action>
                <v-list-item-title>Ping</v-list-item-title>
              </v-list-item>
            </v-list>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="dialog_actions = false">Run</v-btn>
              <v-btn @click="dialog_actions = false" color="red">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Dialog for database actions -->
        <v-dialog v-model="dialog_DB" max-width="500px">
          <v-card>
            <v-list>
              <v-list-item>
                <v-list-item-title> DATABASE ACTIONS </v-list-item-title>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list-group :value="true" no-action sub-group>
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title>
                    Select the backup date/s</v-list-item-title
                  >
                </v-list-item-content>
              </template>

              <v-list-item v-for="dates in backup_dates" v-bind:key="dates">
                <template v-slot:default="{ active }">
                  <v-list-item-action>
                    <v-checkbox
                      :input-value="active"
                      color="primary"
                    ></v-checkbox>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title>{{ dates }}</v-list-item-title>
                  </v-list-item-content>
                </template>
              </v-list-item>
            </v-list-group>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="dialog_DB = false">Download</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- dialog for comments -->
        <v-dialog v-model="dialog_comments" max-width="500px">
          <v-card>
            <v-list>
              <v-list-item>
                <v-list-item-title> COMMENTS </v-list-item-title>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <template v-if="comment_text.length != 0">
              <v-data-table
                :headers="header_comment"
                :items="comment_text"
                hide-default-header
                hide-default-footer
                class="elevation-1"
              >
                <template v-slot:[`item.user`]="{ item }">
                  <v-avatar color="indigo" size="30">
                    <span class="white--text headline">{{
                      item.user.substr(0, 1)
                    }}
                    </span>
                  </v-avatar>
                </template>
              
                <template v-slot:[`item.delete`]="{ item }">
                  <v-icon v-if="item.delete === $store.state.authProfile.user.username" @click="deleteComment(item)">mdi-close-circle-outline</v-icon>
                </template>

                <template v-slot:[`item.comment`]="{ item }">
                  <v-edit-dialog
                    :return-value.sync="item.comment"
                    large
                    persistent
                    @save="updateComment(item)"
                    v-if="item.delete === $store.state.authProfile.user.username"
                  >
                    <div>{{ item.comment }}</div>
                    <template v-slot:input>
                      <v-text-field
                        v-model="item.comment"
                        :rules="[v => (v || '' ).length <= 200 || 'Description must be 200 characters or less']"
                        counter
                        maxlength="200"
                      ></v-text-field>
                    </template>
                  </v-edit-dialog>
                  <div v-else>{{ item.comment }}</div>
                </template>
              </v-data-table>
            </template>
            <v-form v-model="isCommentValid">
            <v-list class="mt-5">
              <v-list-item>
                <v-textarea
                  v-model="comment"
                  solo
                  name="input-7-4"
                  label="Insert your comment"
                  :rules="[v => (v || '' ).length <= 200 || 'Description must be 200 characters or less']"
                  counter
                ></v-textarea>
              </v-list-item>
            </v-list>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" :disabled="!isCommentValid" @click.stop="insertComment()"
                >Add comment</v-btn
              >
            </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    
    <v-row>
      <!-- dialog for partitions -->
      <v-dialog
        v-model="dialog_partitions"
        max-width="400px"
      >
        <v-card>
          <v-card-title>
            <span class="headline">Edit partitions</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-combobox
                  v-model="partitions"
                  label="Add or delete logical partitions"
                  multiple
                  chips
                ></v-combobox>
                <v-btn
                  class="ma-2"
                  color="success"
                  @click="updatePartitions"
                >
                  Save
                </v-btn>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-row>

    <v-row>
      <!-- Export buttons to excel/pdf -->
      <v-col cols="auto" class="ml-10">
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
import DeviceDetail from "./DeviceDetail.vue";

export default {
  name: "DevicesTable",
  store,
  components: {
    DeviceDetail,
  },
  data() {
    return {
      title: "Devices",
      current_device: null,
      backup_dates: ["2019-11-02", "2020-01-03", "2020-01-05"],
      excel: [],
      comment: "",
      comment_text: [],
      system_uptime_update: "",
      dialog_DB: false,
      dialog_actions: false,
      dialog_comments: false,
      dialog_status: false,
      dialog_partitions: false,
      dialog_costumHeaders: false,
      isCommentValid: false,
      search: "",
      singleSelect: false,
      selected: [],
      list_headers: [
        { text: "Name", value: "name" },
        { text: "IP address", value: "ip_address" },
        { text: "MAC address", value: "mac_address" },
        { text: "Serial Num.", value: "serial_number" },
        { text: "Creation Time", value: "create_time" },
        { text: "Updated Time", value: "updated_device_time" },
        { text: "Zone", value: "zone" },
        { text: "Area", value: "area"},
        { text: "Group", value: "group"},
        { text: "Mode", value: "mode"},
        { text: "Status", value: "status"},
        { text: "Manufacturer", value: "manufacturer" },
        { text: "Operating Sys.", value: "operating_system" },
        { text: "SW version", value: "sw_version" },
        { text: "FQDN", value: "fqdn" },
        { text: "Contact Person", value: "contact_person" },
        { text: "SW End of Life", value: "sw_end_of_life" },
        { text: "HW End of Life", value: "hw_end_of_life" },
        { text: "Actions", align: "center" , sortable: false, value: "actions" },
        { text: '', sortable: false, value: 'data-table-expand' }
      ],
      headers: [
        { text: "Name", value: "name" },
        { text: "IP address", value: "ip_address" },
        { text: "Zone", value: "zone" },
        { text: "Area", value: "area"},
        { text: "Group", value: "group"},
        { text: "Mode", value: "mode"},
        { text: "Status", value: "status", align: "center"},
        { text: "SW End of Life", value: "sw_end_of_life" },
        { text: "HW End of Life", value: "hw_end_of_life" },
        { text: "Actions", align: "center" , sortable: false, value: "actions" },
        { text: '', sortable: false, value: 'data-table-expand' }
      ],
      header_comment: [
        { text: 'user', value: 'user'},
        { text: 'comment', value: 'comment' },
        { text: 'delete', align: 'end' ,value: 'delete' },
      ],
      selected_headers: [0,1,6,7,8,9,10,16,17],
      items: [],
      loading: false,
      loading_pdf: false,
      loading_excel: false,
      error: false,
      errorMessage: "",
      expanded: [],
      singleExpand: false,
      partitions: [],
    };
  },
  mounted() {
    this.animation();
    this.getDevices();
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
        var devices = [];
        if (vm.selected.length == 0) {
          for (let i=0; i<vm.items.length; i++){
            let device = vm.items[i]
            delete device['actions']
            devices.push(device);
          }
          data_xls = XLSX.utils.json_to_sheet(devices);
        } else {
          for (let i=0; i<vm.selected.length; i++){
            let device = vm.selected[i]
            delete device['actions']
            devices.push(device);
          }
          data_xls = XLSX.utils.json_to_sheet(devices);
        }
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, data_xls, 'Devices');
        XLSX.writeFile(workbook, 'Devices.xlsx')
        vm.loading_excel = false
      } 
      
      else if (value == true){
        vm.loading_pdf = true;
        var columns = [];
        var data = [];
        for (var j = 0; j < vm.headers.length - 2; j++) {
          columns.push(vm.headers[j].text);
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
            2: { halign: "center" },
            3: { halign: "center" },
            4: { halign: "center" },
            5: { halign: "center" },
            6: { halign: "center" },
          },
        });
        doc.setPage(pageNumber);
        doc.save("Devices.pdf");
        vm.loading_pdf = false;
      }
    },
    
    listDevices(devices) {
      var list_devices = [];
      for (var i = 0; i < devices.length; i++) {
        var device = []
        for (var j = 0; j < this.headers.length-2; j++){
          if (this.headers[j].value == 'hw_end_of_life' || this.headers[j].value == 'sw_end_of_life'){
            device.push(devices[i][this.headers[j].value].substring(0,10) + ' ' + devices[i][this.headers[j].value].substring(11,16))
          }else {
            device.push(devices[i][this.headers[j].value])
          }
        }
        list_devices.push(device);
      }
      return list_devices;
    },

    getDevices: function () {
      var vm = this;
      (vm.loading = true),
        http
          .get("/devices")
          .then(function (response) {
            console.log(response.data)
            vm.items = response.data;
            //store.commit("listDevices", vm.items);
            vm.items.forEach((element) => {
              element.actions = element.id;
              if (element.hw_end_of_life == null) {
                var date = new Date(new Date(2021,0,1).getTime() + Math.random() * (new Date().getTime() - new Date(2021,0,1).getTime()))
                element.hw_end_of_life = date.toISOString();
              }
              if (element.sw_end_of_life == null) {
                var date_sw = new Date(
                  +new Date() + Math.floor(Math.random() * 15000000000)
                );
                element.sw_end_of_life = date_sw.toISOString();
              }
            });
            vm.loading = false;
          })
          .catch((e) => {
            console.log(e);
            vm.error = true;
            vm.errorMessage = 'Update Failed';
            vm.loading = false;
          });
      
    },

    changeHeaders(){
      var vm = this;
      vm.headers = [];
      vm.selected_headers.sort(function(a, b){return a-b});
      for(var i=0; i<vm.selected_headers.length; i++){
        vm.headers.push(vm.list_headers[vm.selected_headers[i]]);
      }
      vm.headers.push(vm.list_headers[vm.list_headers.length - 2]);
      vm.headers.push(vm.list_headers[vm.list_headers.length - 1]);
      vm.dialog_costumHeaders = false;
    },

    insertComment() {     
      var vm = this;
      http
        .post("/devicesComments/", {"user": this.$store.state.authProfile.user.username, "comment": vm.comment, "device": vm.current_device.id})
        .then(function (response) {
          var data = response.data;
          data["delete"] = data.user;
          vm.comment_text.push(data);
        })
        .catch((e) => {
          console.log(e);
          vm.error = true;
          vm.errorMessage = 'Error commenting';
        });
      vm.comment = '';
    },

    updateComment(item) {     
      var vm = this;
      var user = this.$store.state.authProfile.user.username; 
      http
        .put("/devicesComments/" + item.id + "/", {"user": user, "comment": item.comment, "device": vm.current_device.id})
        .then(function (response) {
          for(var i=0; i<vm.comment_text.length; i++){
            if (vm.comment_text[i].id === response.data.id){
              vm.comment_text[i].comment = item.comment;
            }
          }
        })
        .catch((e) => {
          console.log(e);
          vm.error = true;
          vm.errorMessage = 'Error updating comment';
        });
      vm.comment = '';
    },

    deleteComment(item) {     
      var vm = this;
      http
        .delete("/devicesComments/" + item.id + "/")
        .then(function () {
          for(var i=0; i<vm.comment_text.length; i++){
            if (vm.comment_text[i].id === item.id){
              vm.comment_text.splice(i,1);
            }
          }
        })
        .catch((e) => {
          console.log(e);
          vm.error = true;
          vm.errorMessage = 'Error deleting comment';
        });
    },

    setStatus(status){
      var vm = this
      vm.current_device['status'] = status;
      let id = vm.current_device['id']
      delete vm.current_device.actions;
      http
        .put("/devices/" + id + '/', vm.current_device)
        .then(function (response) {
          vm.current_device = response.data
          for(var i=0; i<vm.items.length; i++){
            if (vm.items[i].id === response.data.id){
              vm.items[i].status = response.data.status;
            }
          }
        })
        .catch((e) => {
          console.log(e);
          vm.error = true;
          vm.errorMessage = 'Error changing status';
        });
      vm.dialog_status = false;
    },

    dialogActions(value) {
      this.dialog_actions = true;
      this.current_device = value;
    },

    dialogStatus(value) {
      this.dialog_status = true;
      this.current_device = value;
    },

    databaseActions(value) {
      this.dialog_DB = true;
      this.current_device = value;
    },

    dialogComments(value) {
      var vm = this;
      vm.comment = '';
      vm.comment_text = [];
      this.current_device = value;
      
      http
        .get("/devicesComments")
        .then(function (response) {
          response.data.forEach((element) => {
            if (element.device == value.id) {
              element["delete"] = element.user;
              vm.comment_text.push(element);
            }
          });
        })
        .catch((e) => {
          console.log(e);
          this.error = true;
          vm.errorMessage = 'Error obtaining comments';
        });
      vm.dialog_comments = true;
    },

    editPartitions(item) {
      this.partitions = []
      this.current_device = item
      item.logic_partition.forEach(element => {
        this.partitions.push(element.name)
      });
      this.dialog_partitions = true;
    },

    updatePartitions(){
      var data = []
      this.partitions.forEach(element => {
        data.push({name: element})
      });
      var vm = this
      http.post("/devices/" + vm.current_device.id + '/logical_partitions/', data)
        .then(function (response) {
          vm.current_device.logic_partition = response.data
        })
        .catch((e) => {
          console.log(e);
          this.error = true;
          vm.errorMessage = 'Error updating partitions';
        });
      vm.dialog_partitions = false;
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