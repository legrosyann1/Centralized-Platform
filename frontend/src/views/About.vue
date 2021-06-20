<template>
  <div class="about">
    <v-img
      alt="Portrait"
      class="mt-1"
      position="20% 50%"
      src="../assets/Portrait_wide.png"
      aspect-ratio="1.5"
      contain
      height="480"
    >
      <v-row align="center" class="fill-height">
        <v-spacer></v-spacer>
        <v-col cols="12" md="7">
          <v-container>
            <v-card elevation="8" width="600">
              <v-row justify="center">
                <v-card-title id="font" class="font-weight-medium text--primary">My Project</v-card-title>
              </v-row>
              <v-card-text class="text-justify text--primary mt-n3">{{intro}}</v-card-text>
              <v-card-text class="text-justify text--primary mt-n6">{{body}}</v-card-text>
              <v-row class="ml-4 mt-n2">
                <p class="text--primary font-weight-medium text-md-body-2 mr-3">Contact:</p>
                <span class="text--primary font-weight-regular text-body-2 mr-3">{{email}}</span>
                <v-btn :href="linkedin" class="mt-n2" icon>
                  <v-icon color="primary">
                    mdi-linkedin
                  </v-icon>
                </v-btn>
              </v-row>
            </v-card>
          </v-container>
        </v-col>
      </v-row>
    </v-img>
  </div>
</template>

<script>
export default {
  name: 'About',
  data() {
    return {
      intro: "Hello my name is Yann Legros. I'm a fourth year Telecommuciations Engineer student in Universitat Politècnica de Catalunya (UPC) and this is my thesis project.",
      body: "The purpose of this porject is to simplify the maintenance and management of a scattered network infraestructure. This is accomplished through all the different functionalities offered in this platform which centralizes and automates the operations that take part in a network.",
      email: "legrosyann1@gmail.com",
      linkedin: "https://www.linkedin.com/in/yann-legros-borgu%C3%B1%C3%B3-b373781b2/"
    }
  },
}
</script>

<style>
#font {
  font-family: 'Georgia';
  font-size: 40px;
}
</style>