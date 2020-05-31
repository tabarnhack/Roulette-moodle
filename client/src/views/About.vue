<template>
  <div class="about">
    <Info msg="This is an about page" />
  </div>
</template>

<script>
import Info from "@/components/Info.vue"

export default {
  name: "About",
  components: {
    Info,
  }
}
</script>
