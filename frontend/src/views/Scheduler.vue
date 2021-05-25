<template>
  <div class="scheduler">
    <TaskScheduler/>
  </div>
</template>

<script>
import TaskScheduler from '@/components/TaskScheduler.vue'
export default {
  name: 'Scheduler',
  components: {
    TaskScheduler
  }
}
</script>