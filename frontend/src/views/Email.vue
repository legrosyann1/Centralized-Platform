<template>
  <div class="about">
    <EmailForm/>
  </div>
</template>

<script>
import EmailForm from '@/components/EmailForm.vue'

export default {
  name: 'Email',
  components: {
    EmailForm,
  }
}
</script>