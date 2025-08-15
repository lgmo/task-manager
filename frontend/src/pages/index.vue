<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const { login, isAuthenticated } = useAuth();

async function handleLogin() {
  try {
    const response = await login();
    if (response.loginUrl) {
      window.location.href = response.loginUrl;
    }
  } catch (error) {
    console.error('Login failed:', error);
  }
}

onMounted(async () => {
  try {
    if (await isAuthenticated()) {
      router.push('/tasks');
    } else {
      await handleLogin();
    }
  } catch (error) {
    console.error('Auth check failed:', error);
  }
});
</script>