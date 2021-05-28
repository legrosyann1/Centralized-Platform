<template>
  <div class="mx-auto">
    <v-row>
      <v-col>
        <h2 class="text-h4 mb-2">{{ this.$route.name }}</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col 
        cols=12 md=6 
        v-for="(task, key) in tasks"
        v-bind:key="key"
      >
        <v-card elevation="2" >
          <v-row class="mx-auto">
            <v-card-title>
              {{ task.title }}
            </v-card-title>
            <v-switch
              v-model="task.enabled"
              color="success"
              @change="saveSchedule(task, false)"
            ></v-switch>
          </v-row>
          <v-text-field 
            :disabled="!task.enabled"
            label='Schedule'
            :value="task.time"
            class="mx-5 mb-4"
            v-if="!task.enabled"
          ></v-text-field>
          <v-text-field 
            :disabled="!task.enabled"
            v-model=task.change_time
            :value="task.change_time"
            label='Schedule'
            class="mx-5 mb-4"
            :placeholder="task.time"
            v-else
            @change="change=true"
          ></v-text-field>
          <v-row>
            <span class="red--text lighten-2 text-caption ml-8 mt-n3" v-if="!valid">
              Follow the format: mm-hh-dd-mm<br>where d=dayofweek, m=dayofmonth and **=all
            </span>
            <v-spacer></v-spacer>
            <v-card-actions class="mr-5" v-if="change">
              <v-btn
                color="primary"
                text
                @click="saveSchedule(task, true)"
              >
                Save
              </v-btn>
              <v-btn
                color="red"
                text
                @click="cancelSchedule(task)"
              >
                Cancel
              </v-btn>
            </v-card-actions>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import http from "../plugins/axios.js";
export default {
  name: "TaskScheduler",
  data () {
    return {
      change: false,
      valid: true,
      tasks: [],
    }
  }, 
  
  mounted(){
    this.getSchedules()
  },
  
  methods: {
    validateSched(schedule){
      var times = [schedule.substring(0,2), schedule.substring(3,5), schedule.substring(6,8), schedule.substring(9,11)]
      var limits = [59, 24, 7, 28]
      for (var i=0; i<times.length; i++){
        if (isNaN(times[i]) && times[i] !== '**'){
          return false
        }
        else if (!isNaN(times[i])){
          if (parseInt(times[i]) > limits[i]){
            return false
          }
        }
      }
      return true
    },

    saveSchedule(task, sched){
      if (sched){
        if (this.validateSched(task['change_time'])){
          task['time'] = task['change_time']
          this.valid = true
        } else { 
          this.valid = false
          return 
        }
      }
      var data = JSON.parse(JSON.stringify(task))
      delete data['change_time']
      delete data['created_at']
      console.log(data)
      console.log(this.tasks)
      http
        .put('/tasks/' + data.id + '/', data)
        .then(function (response) {
          this.change = false
          console.log(response)
        })
        .catch((e) => {
          console.log(e);
        });
    },

    cancelSchedule(task){
      this.change = false
      this.valid = false
      task['change_time'] = ''
    },

    getSchedules(){
      var vm = this
      http
        .get('/tasks')
        .then(function (response) {
          for (var i=0; i<response.data.length; i++){
            var task = response.data[i]
            task['change_time'] = ''
            vm.tasks.push(task)
          }
          console.log(vm.tasks)
        })
        .catch((e) => {
          console.log(e);
        });
    }
  },
};
</script>