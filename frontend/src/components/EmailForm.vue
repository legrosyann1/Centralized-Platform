<template>
  <div class="container">
    <v-form v-model="isValid" class="mx-15">
      <h1 class="text-h4 mb-8 animacion">Request new Automation</h1>
      <v-text-field class="mb-2" label="Subject" v-model="subject" prepend-icon="mdi-email" :rules="inputRules"></v-text-field>
      <v-textarea class="mb-4" label="Body" v-model="body" prepend-icon="mdi-pencil" :rules="inputRules"></v-textarea>
      <v-file-input chips label="File input" v-model="file"></v-file-input>
      <v-btn :disabled="!isValid" @click="sendEmail">Send</v-btn>
    </v-form>
    <v-snackbar v-model="result_dialog" :timeout="2000" app light class="mb-5">
      <div class="text-center success--text" v-if="result">
        Email sent succesfully
        <v-icon color="success" class="ml-1">mdi-checkbox-marked-circle</v-icon>
      </div>
      <div class="text-center red--text" v-else>
        Failed to send Email
        <v-icon color="red" class="ml-1">mdi-close-circle</v-icon>
      </div>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "../plugins/axios.js";

export default {
  name: 'EmailForm',
  data () {
    return {
      subject: '',
      body: '', 
      isValid: false,
      result: null,
      result_dialog: false,
      ws: null,
      file: null,
      inputRules: [
          value => !!value || 'This field is required'
      ]
    }
  }, 

  methods: {
    sendEmail(){
      var vm = this
      vm.isValid = false

      let formData = new FormData();
      if (vm.file){
        formData.append("files", vm.file, vm.file.name);
      }
      formData.append("subject", vm.subject);
      formData.append("body", vm.body);

      axios
        .post("/email", formData)
        .then(function (response) {
          if(response.data == 200){
            vm.result = true;
          }else if(response.data == 500){
            vm.result = false;
          }

          vm.result_dialog = true
          vm.isValid = true
        })
        .catch((e) => {
          console.log(e);
        });
    }
  }    
}
</script>