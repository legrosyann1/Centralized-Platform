<template>
  <div class="operationsCenter">
    <div class="text-h4 mb-6">{{this.$route.name}}</div>
    <Actions/>
  </div>
</template>

<script>
import Actions from '@/components/Actions.vue'
export default {
  name: 'OperationsCenter',
  components: {
    Actions,
  }
}
</script>