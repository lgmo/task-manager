<script setup>
defineOptions({
  meta: {
    requiresAuth: true
  }
});

import TasksList from '@/components/TasksList.vue'
import LogoutButton from '@/components/LogoutButton.vue'
</script>

<template>
  <v-container>
    <tasks-list />
    <logout-button />
  </v-container>
</template>

