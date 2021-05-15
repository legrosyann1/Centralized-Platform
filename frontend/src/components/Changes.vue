<template>
  <v-row class="fill-height">
    <v-col>
      <h2 class="text-h4 mb-2">{{ this.$route.name }}</h2>
      <v-sheet height="64">
        <v-toolbar flat>
          <v-btn
            :loading="loading"
            outlined
            color="grey darken-2"
            @click="viewDay(current_date)"
          >
            Today
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small> mdi-chevron-left </v-icon>
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="next">
            <v-icon small> mdi-chevron-right </v-icon>
          </v-btn>
          <v-btn
            :loading="loading"
            color="primary"
            class="mr-2"
            @click="createFutureTask()"
          >
            Create Task
          </v-btn>
          <!-- dialog for new tasks -->
          <v-row justify="center">
            <v-dialog v-model="dialog_future_task" max-width="600px" >
              <v-card>
                <v-card-title>
                  <span class="headline font-weight-bold">NEW TASK</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row class="mb-6">
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field 
                          v-model="future_change_code"
                          label="Change Code"
                          type="text"
                        ></v-text-field>
                      </v-col>

                      <v-col>
                        <v-text-field
                          v-model="start_date"
                          label="Start date"
                          type="date"
                        ></v-text-field>
                      </v-col>

                      <v-col>
                        <v-text-field
                          v-model="start_time"
                          label="Start time"
                          type="time"
                        ></v-text-field>
                      </v-col>

                      <v-col cols="12" sm="6" md="4">
                        <v-autocomplete
                          v-model="type"
                          :items="['Corrective', 'Evolutionary', 'Pre-approved']"
                          label="Type"
                        ></v-autocomplete>
                      </v-col>

                      <v-col>
                        <v-text-field
                          v-model="end_date"
                          label="End date"
                          type="date"
                        ></v-text-field>
                      </v-col>

                      <v-col>
                        <v-text-field
                          v-model="end_time"
                          label="End time"
                          type="time"
                        ></v-text-field>
                      </v-col>

                      <v-col cols="12" sm="8" md="6">
                        <v-text-field
                        v-model='environment'
                          label="Environment"
                          type="text"
                        ></v-text-field>
                      </v-col>

                      <v-col cols="12" sm="8" md="6">
                        <v-text-field
                          v-model="requester"
                          label="Requestor"
                          type="text"
                        ></v-text-field>
                      </v-col>

                      <v-col cols="12" sm="7" md="5">
                        <v-text-field
                          v-model="implementer"
                          label="Implementer"
                          type="text"
                        ></v-text-field>
                      </v-col>

                      <v-col cols="12" sm="6" md="4">
                        <v-autocomplete
                          v-model="state"
                          :items="['Initial', 'Pending', 'Canceled', 'Completed']"
                          label="Task state"
                          required
                        ></v-autocomplete>
                      </v-col>

                      <v-col cols="12" sm="5" md="3">
                        <v-autocomplete
                          v-model="urgent"
                          :items="['Yes', 'No']"
                          label="Urgent"
                          required
                        ></v-autocomplete>
                      </v-col>

                      <v-col cols="12">
                        <v-textarea
                          v-model="description"
                          class="mt-n2"
                          label="Description"
                          type="text"
                        ></v-textarea>
                      </v-col>

                      <v-col cols="12">
                        <v-file-input
                          v-if='!file'
                          label="RFC"
                          @change='files'>
                        </v-file-input>
                        <v-card-text class="mx-n4 mt-n4 mb-n14" v-if='file'>{{file}}
                          <v-btn
                            text
                            @click='downloadFile(selectedEvent)'
                            icon
                          >
                            <v-icon
                              color='primary'
                            >mdi-cloud-download</v-icon>
                          </v-btn>
                        </v-card-text>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions >
                  <v-spacer></v-spacer>
                  <!-- v-if='start_date && end_date && start_time && end_time && future_change_code && implementer' -->
                  <v-btn color="primary" @click="saveFutureTask(selectedEvent)">
                    Save
                  </v-btn>
                  <v-btn color="red" v-if="selectedEvent.task.id" text @click="deleteFutureTask(selectedEvent)">
                    Delete
                  </v-btn>
                  <v-btn
                    color="red" @click="dialog_future_task = false">
                    Close
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
          <v-spacer></v-spacer>
          <v-col cols='7'>
            <v-chip
              v-for='type in type_taskStatus'
              :class="{'red': type === 'Incomplete past task',
              'green':type === 'Task completed',
              'yellow darken-3':type === 'Task created',
              'primary':type === 'Task in progress',
              'grey darken-2':type === 'Task cancelled'}"
              v-bind:key='type'
              class="ma-2"
              small
            >
              {{ type }}
            </v-chip>
          </v-col>
          <v-spacer></v-spacer>
          <v-menu bottom right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                :loading="loading"
                outlined
                color="grey darken-2"
                v-bind="attrs"
                v-on="on"
              >
                <span>{{ typeToLabel[calendar_type] }}</span>
                <v-icon right> mdi-menu-down </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="calendar_type = 'day'">
                <v-list-item-title>Day</v-list-item-title>
              </v-list-item>
              <v-list-item @click="calendar_type = 'week'">
                <v-list-item-title>Week</v-list-item-title>
              </v-list-item>
              <v-list-item @click="calendar_type = 'month'">
                <v-list-item-title>Month</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>
      <v-sheet height="600">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :weekdays="[1, 2, 3, 4, 5, 6, 0]"
          :events="events"
          :event-color="getEventColor"
          :type="calendar_type"
          @click:event="showEvent"
          @click:more="viewDay"
          @click:date="viewDay"
        ></v-calendar>
        <!--v-dialog
          v-model='selectedOpenFuture'
          v-if='selectedOpenFuture'
          :close-on-content-click="false"
          :activator="selectedElement"
          max-width="700"
        >
          <span v-html='selectedEvent.start'></span>
        </v-dialog-->
        <!-- dialog for Automated changes -->
        <v-dialog
          v-model="selectedOpen"
          max-width="700"
        >
          <v-card>
            <v-card-title>
              <span class="headline">Automated Devices Changes</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4" class="mt-5 mb-6" v-show="!selectedEvent.change_code || edit_change_code">
                    <v-text-field
                      margin="20px"
                      v-model="change_code"
                      type="text"
                      color="primary"
                      filled
                      label="Change code"
                    ></v-text-field>
                    <v-checkbox class='mt-n7 mx-auto'
                      v-model="change_code"
                      label="no code"
                      value="no code"
                    ></v-checkbox>
                  </v-col>
                  <v-col cols="12" class="mt-n2 mb-8" v-show="!edit_change_code && selectedEvent.change_code">
                    <v-card-text>
                      <span class="font-weight-bold">Change code: </span
                      ><span v-html="change_code"></span>
                      <v-btn
                        x-small
                        color="primary"
                        class="mx-2"
                        fab
                        @click.stop="edit_change_code = true"
                      >
                        <v-icon> mdi-pencil </v-icon>
                      </v-btn>
                    </v-card-text>
                  </v-col>
                  <v-row>
                    <v-row class="mt-n6 ml-9">
                      <v-col cols='4'>
                        <h2>Device</h2>
                      </v-col>
                      <v-col cols='4'>
                        <h2>Old Info</h2>
                      </v-col>
                      <v-col cols='4'>
                        <h2>New info</h2>
                      </v-col>
                    </v-row>
                    <v-card-text
                      v-for="item in selectedEvent.task"
                      v-bind:key="item"
                    >
                      <v-row class="ml-5">
                        <v-col cols='12' sm='4'>
                          <div>
                            <span class="font-weight-bold">{{ item.device }}</span>
                          </div>
                        </v-col>
                        <v-col cols='12' sm='4'>
                          <div v-for='(key, value) in item.old_info' :key='value'>
                            <span>{{ key }}</span> 
                          </div>
                        </v-col>
                        <v-col cols='12' sm='4'>
                          <div v-for='(key, value) in item.new_info' :key='value'>
                            <span>{{ key }}</span>
                          </div>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-row>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                v-if="change_code"
                color="primary"
                @click.stop="saveChanges(selectedEvent)"
              >
                Save
              </v-btn>
              <v-btn color="red" @click="selectedOpen = false"> Close </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-sheet>
    </v-col>
  </v-row>
</template>


<script>
import http from "../plugins/axios.js";

export default {
  data: () => ({
    // calendar related
    focus: "",
    calendar_type: "month",
    typeToLabel: {
      month: "Month",
      week: "Week",
      day: "Day",
    },
    events: [],
    // New task related
    start_date:'',
    end_date:'',
    start_time:'',
    end_time:'',
    description:'',
    future_change_code:'',
    environment:'',
    type:'',
    urgent:'',
    implementer:'',
    requester:'',
    rfc: undefined,
    file: undefined,
    state:'',
    future_changes: [],
    dialog_future_task: false, 
    parse_type:{'Corrective': 'corrective', 'Evolutionary': 'evolutionary', 'Pre-approved': 'pre-approved'},
    // Created task related
    change_code: "",
    changes: [],
    same_changes:[],
    // other
    type_taskStatus:['Task completed', 'Task created', 'Task in progress', 'Task canceled', 'Incomplete past task'],
    current_date:'',
    selectedEvent: {name: null, start: null, end: null, color: null, timed: null, change_code: null, task: {}},
    loading: false,
    edit_change_code: false,
    selectedElement: null,
    selectedOpen: false,
    selectedOpenFuture: false,
  }),
  mounted() {
    this.getChanges();
    this.loading = true;
  },

  methods: {
    viewDay({ date }) {
      this.focus = date;
      this.calendar_type = "day";
    },
    getEventColor(event) {
      return event.color;
    },

    files(selectedfiles){
      this.rfc = selectedfiles
    },

    buildEvent(name, start, end, color, timed, change_code, task){
      var dict = {};
      dict.name = name;
      dict.start = start;
      dict.end = end;
      dict.color = color;
      dict.timed = timed;
      dict.change_code = change_code;
      dict.task = task;

      return dict
    },

    createFutureTask(){
      this.start_date = '',
      this.end_date = '',
      this.start_time = '',
      this.end_time = '',
      this.description = '',
      this.future_change_code = '',
      this.environment = '',
      this.type = '',
      this.urgent = '',
      this.implementer = '',
      this.requester = '',
      this.rfc = null,
      this.file = undefined,
      this.state = 'Initial',

      this.selectedEvent = {name: null, start: null, end: null, color: null, timed: null, change_code: null, task: {}};
      this.dialog_future_task = true
    },

    downloadFile(event){
      http
      .get("/changes/" + event.task.id + '/downloadFile/', { responseType: 'arraybuffer' })
      .then(function (response) {
          var file = new Blob([response.data])
          var data = URL.createObjectURL(file);
          var a = document.createElement("a");
          a.style = "display: none";
          a.href = data;
          a.download = event.task.rfc;
          document.body.appendChild(a);
          a.click();
          })
    },

    getEvents(changes) {
      var vm = this
      var events = []
      var same = []
      var base_name = 'Automated change - '
      var deviceskeys = Object.keys(changes[0].old_info);
      var group = false

      for(var i = 0; i<changes.length; i++){
        // Prepare event 
        var diff_old = []
        var diff_new = []
        var tasks = []
        var color = 'red'
        for (var x = 0; x < deviceskeys.length; x++) {
          if (changes[i].old_info[deviceskeys[x]] != changes[i].new_info[deviceskeys[x]]) {
            diff_old.push(deviceskeys[x] + ': ' + changes[i].old_info[deviceskeys[x]]);
            diff_new.push(deviceskeys[x] + ': ' + changes[i].new_info[deviceskeys[x]]);
          }
        }
        var start = new Date(changes[i].created_at.substring(0, 10) + " " + changes[i].created_at.substring(11, 16));
        if (changes[i].change_code) {color = 'green'}
        var newtask = {old_info: diff_old, new_info: diff_new, device: changes[i].old_info['name'], id: changes[i].id}
        tasks.push(newtask)
        
        // build event and init data
        var newevent = vm.buildEvent(
          base_name + 'Device ' + changes[i].old_info['name'],
          start, start, color, true, changes[i].change_code, tasks)
        tasks = [];
        diff_old = [];
        diff_new = [];
        
        // push and group event
        var pastevent = events.pop()
        if (pastevent){
          if (pastevent.start == newevent.start){
            var count = 0
            for (x = 0; x < pastevent.task.length; x++){
              if (pastevent.change_code == newevent.change_code){
                count ++;
              }
            }
            if (count == 0 || count == pastevent.task.length){
              pastevent.name = base_name + 'Devices';
              pastevent.task.push(newtask)
              events.push(pastevent)
              group = true
            } else {
              events.push(pastevent)
              events.push(newevent) 
              group = false 
            }
          } else {
            events.push(pastevent)
            events.push(newevent)
            group = false 
          }
        } else {events.push(newevent)}

        // group changes to send the update in case needed
        if (group){
          if (same.length == 0){
            same.push(changes[i-1])
          }
          same.push(changes[i])
        } else {
          if (same.length != 0){
            vm.same_changes.push(same)
            same = []
          }
        }
      }
      var futureevents = vm.getFutureEvents(vm.future_changes)
      vm.events = events.concat(futureevents)
      vm.loading = false;
      console.log(vm.events)
    },

    getFutureEvents(changes){
      this.current_date = new Date()
      const events = []

      for(var i = 0; i<changes.length; i++){
        var name = changes[i].change_code;
        var start = new Date(Date.parse(changes[i].start_date))
        var end = new Date(Date.parse(changes[i].end_date))
        if (changes[i].is_urgent == true){ changes[i].is_urgent = 'Yes' } 
        else{ changes[i].is_urgent = 'No' }
        var task = {
          start_date: changes[i].start_date.substring(0, 10),
          start_time: changes[i].start_date.substring(11, 16),
          end_date: changes[i].end_date.substring(0, 10),
          end_time: changes[i].end_date.substring(11, 16),
          description: changes[i].description,
          environment: changes[i].environment,
          type: Object.keys(this.parse_type).find(key => this.parse_type[key] === changes[i].type),
          urgent: changes[i].is_urgent,
          implementer: changes[i].implementer,
          requester: changes[i].requester,
          rfc: changes[i].rfc,
          state: changes[i].state,
          id: changes[i].id
        }
        var color = null
        if((task.state == 'Initial' || task.state == 'Pending') && this.current_date >= end){
          color = 'red'
        }else if(task.state == 'Completed'){
          color = 'green'
        }else if(task.state == 'Pending'){
          color = 'primary'
        }else if(task.state == 'Canceled'){
          color = 'grey darken-2'
        }else{
          color = 'yellow darken-3'
        }

        // build event
        var newevent = this.buildEvent(name, start, end, color, true, changes[i].change_code, task)
        events.push(newevent)
      }
      return events
    },

    getChanges() {
      var vm = this;
      http
        .get("/devicesChanges")
        .then(function (response) {
          vm.changes = response.data;
          vm.getFutureChanges()
        })
        .catch((e) => {
          console.log(e);
        });
    },
    
    getFutureChanges(){
      var vm = this;
      http
        .get('/changes')
        .then(function (response){
          vm.future_changes = response.data;
          vm.getEvents(vm.changes);
        })
        .catch((e) => {
          console.log(e);
        });
    },
    
    prev() {
      this.$refs.calendar.prev();
    },
    
    next() {
      this.$refs.calendar.next();
    },
    
    deleteFutureTask(event){
      var vm = this
      var id = event.task.id
      http
        .delete('/changes/'+ id + '/')
        .then(function (response){
          console.log(response.data)
          vm.dialog_future_task = false
          vm.getChanges()
        })
    },

    saveFutureTask(event){
      let formData = new FormData();
      if(this.rfc && this.rfc.size != null){
        formData.append("rfc", this.rfc);
      }

      var vm = this
      var types = Object.keys(this.parse_type)
      if(this.urgent == 'yes'){this.urgent = true
      }else{this.urgent = false}
      for(var i=0; i<types.length; i++){
        if(types[i] == this.type){
          this.type = this.parse_type[types[i]]
        }
      }
      formData.append('start_date', this.start_date + 'T' + this.start_time + ':00Z')
      formData.append('end_date', this.end_date + 'T' + this.end_time + ':00Z')
      formData.append('change_code', this.future_change_code)
      formData.append('environment',this.environment)
      formData.append('description',this.description)
      formData.append('type',this.type)
      formData.append('is_urgent',this.urgent)
      formData.append('implementer',this.implementer)
      formData.append('state',this.state)
      formData.append('requester',this.requester)
    
      if(!event.task.id){
        http
        .post("/changes/", formData)
        .then(function (response){
          vm.getChanges()
          console.log(response.data)
        })
      }else{
        http
        .put('/changes/'+ event.task.id + '/', formData)
        .then(function(response){
          vm.getChanges()
          console.log(response.data)
        })
      }
      this.dialog_future_task = false
    },

    saveChanges(event) {
      // no grouping
      if(event.task.length == 1){
        for (var i = 0; i < this.changes.length; i++) {
          if (this.changes[i].id === event.task[0].id) {
            this.changes[i].change_code = this.change_code;
            this.sendChanges(this.changes[i]);
          }
        }
        for(var x = 0; x<this.events.length; x++){
          if(this.events[x].task.id === event.task[0].id){
            this.events[x].color = 'green'
            this.events[x].change_code = this.change_code
          }
        }
      // grouping
      }else{
        // apply update in changes
        var index = null
        loop1: 
          for(var z = 0; z < this.same_changes.length; z++){
            for(var y = 0; y < this.same_changes[z].length; y++){
              if(this.same_changes[z][y].id === event.task[0].id){
                index = z
                break loop1;
              }
            }
          }
        
        for (y = 0; y<this.same_changes[index].length; y++){
          this.same_changes[index][y].change_code = this.change_code;
        }
        http
          .put("/devicesChanges/" + '-1' + '/', this.same_changes[index])
          .then(function (response){
            console.log(response.data)
          })

        // apply update in events
        index = null  
        loop1: 
          for(z = 0; z < this.events.length; z++){
            for(y = 0; y < this.events[z].task.length; y++){
              if(this.events[z].task[y].id === event.task[0].id){
                index = z
                break loop1;
              }
            }
          }
        
        this.events[index].change_code = this.change_code;
        this.events[index].color = 'green'
        
      }
      this.edit_change_code = false;
      this.selectedOpen = false;
    },

    sendChanges(item) {
      try {
        http.put("/devicesChanges/" + item.id + "/", item)
      } catch (e) {
        console.log(e);
      }
    },
    
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = {name: null, start: null, end: null, color: null, timed: null, change_code: null, task: {}}
        if(!event.name.startsWith("Automated change - ")){
          this.type = event.task.type;
          this.start_date = event.task.start_date;
          this.end_date = event.task.end_date;
          this.start_time = event.task.start_time;
          this.end_time = event.task.end_time;
          this.description = event.task.description;
          this.state = event.task.state;
          this.requester = event.task.requester;
          this.file = event.task.rfc
          this.future_change_code = event.change_code;
          this.environment = event.task.environment;
          this.urgent = event.task.urgent
          this.implementer = event.task.implementer,
          
          requestAnimationFrame(() => requestAnimationFrame(() => this.dialog_future_task = true))
          requestAnimationFrame(() => requestAnimationFrame(() => this.selectedEvent = event))
        }else{
          if(event.change_code){
            this.change_code = event.change_code
          }
          this.edit_change_code = false;
          requestAnimationFrame(() => requestAnimationFrame(() => this.selectedOpen = true))
          requestAnimationFrame(() => requestAnimationFrame(() => this.selectedEvent = event))
        }
      };
      open();
      nativeEvent.stopPropagation();
    },
  },
};
</script>