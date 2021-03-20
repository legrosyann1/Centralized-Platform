<template>
  <div class="login">
    <FormLogin/>
  </div>
</template>

<script>
import FormLogin from '@/components/FormLogin.vue'

export default {
  name: 'Login',
  components: {
    FormLogin
  }
}
</script>