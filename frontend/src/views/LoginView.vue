<template>
  <div class="auth-form">
    <h2>Login to Your Account</h2>
    <input v-model="email" type="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="handleLogin">Login</button>
    <p v-if="errorMsg" class="message">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const { signIn } = useAuth();
const router = useRouter();
const email = ref('');
const password = ref('');
const errorMsg = ref('');

const handleLogin = async () => {
  try {
    await signIn(email.value, password.value);
    router.push({ name: 'dashboard' });
  } catch (error) {
    errorMsg.value = error.message;
  }
};
</script>

<style scoped>
.message {
  text-align: center;
  color: #d9534f;
  margin-top: 1rem;
}
</style>