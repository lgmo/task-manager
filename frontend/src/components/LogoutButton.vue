<template>
  <v-btn
    color="error"
    variant="text"
    class="logout-btn"
    @click="handleLogout"
  >
    <v-icon start>mdi-logout</v-icon>
    Sair
  </v-btn>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const route = useRoute()
const  { logout } = useAuth()

const handleLogout = async () => {
  const response = await logout()
  window.location.href = response.logoutUrl || '/';
}
</script>

<style scoped>
.logout-btn {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
}
</style>