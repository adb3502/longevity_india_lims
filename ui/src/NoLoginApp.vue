<template>
  <div class="os-root">
    <os-navbar class="no-login-navbar" :no-login="true">
      <template #default="slotProps" v-if="navBarButtons">
        <span v-if="!slotProps.authenticated">
          <os-plugin-views page="no-login" view="navbar" />
        </span>
      </template>
    </os-navbar>

    <os-app-body />
  </div>
</template>

<script>
export default {
  name: 'NoLoginApp',

  props: ['navBarButtons'],

  data() {
    return {
    }
  }
}
</script>

<style scoped>
.os-root {
  height: 100%;
}

.no-login-navbar :deep(button.btn) {
  border: none;
  color: #fff;
  padding: 0.25rem 0.5rem;
  font-weight: bold;
  font-size: 0.8rem;
  min-width: 7rem;
  border-radius: 0.25rem;
  cursor: pointer;
  height: 1.75rem;
  border-radius: 1rem;
}
</style>
