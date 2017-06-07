<template>
  <div>
    <User queryType="group" :gid="$route.params.id"></User>
  </div>
</template>

<script>
import User from '../common/User';
export default {
  components: {User},
  props: ['id']
}
</script>

<style scoped>
</style>