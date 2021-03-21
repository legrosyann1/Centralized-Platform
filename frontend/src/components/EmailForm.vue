<template>
  <div class="container">
    <v-form v-model="isValid">
      <h1 class="text-h4 mb-8 mt-4 animacion">Request new Automation</h1>
      <v-text-field class="mb-2" label="Subject" v-model="subject" prepend-icon="mdi-email" :rules="inputRules"></v-text-field>
      <v-textarea class="mb-4" label="Body" v-model="body" prepend-icon="mdi-pencil" :rules="inputRules"></v-textarea>
      <v-file-input chips multiple label="File input" v-model="files"></v-file-input>
      <v-dialog v-model="received" color="grey lighten-1" max-width="600px">
        <template v-slot:activator="{ on, attrs }">
          <v-btn :disabled="!isValid" @click="sendEmail" v-bind="attrs" v-on="on">Send</v-btn>
        </template>
        <v-card>
          <v-card-title id="result_container"></v-card-title>
        </v-card>
      </v-dialog>
    </v-form>
  </div>
</template>

<script>
//import axios from "../plugins/axios.js";

export default {
  name: 'EmailForm',
  data () {
    return {
      subject: '',
      body: '', 
      isValid: false,
      received: false,
      ws: null,
      files: null,
      inputRules: [
          value => !!value || 'This field is required'
      ]
    }
  }, 

  methods: {
    sendEmail(){
      console.log(this.subject, this.body);
      console.log(this.files);
      /*
      let formData = new FormData();
      if (this.files){
        for (let file of this.files) {
          formData.append("files", file, file.name);
        }
      }
      formData.append("subject", this.subject);
      formData.append("body", this.body);

      axios
        .post("/email", formData)
        .then(function (response) {
          console.log(response.data);
        })
        .catch((e) => {
          console.log(e);
        });*/
    }
  }    
}
</script>