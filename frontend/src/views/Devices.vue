<template>
    <div class="devices">
        <DevicesTable/>
    </div>
</template>

<script>
import DevicesTable from '@/components/DevicesTable.vue'
export default {
    name: 'Device',
  components: {
    DevicesTable
  }
}
</script>