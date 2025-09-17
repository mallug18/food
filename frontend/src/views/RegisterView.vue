<template>
  <div class="auth-form">
    <h2>Create a New Account</h2>
    <input v-model="email" type="email" placeholder="Email Address" />
    <input v-model="username" type="text" placeholder="Username (public, min 3 chars)" />
    <input v-model="password" type="password" placeholder="Password (min 6 chars)" />
    <button @click="handleRegister">Create Account</button>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuth } from '../stores/auth';
import { useRouter } from 'vue-router';

const { signUp } = useAuth();
const router = useRouter();
const email = ref('');
const username = ref('');
const password = ref('');
const message = ref('');

const handleRegister = async () => {
  if (!username.value || username.value.length < 3) {
    message.value = "Username must be at least 3 characters.";
    return;
  }
  try {
    await signUp(email.value, password.value, username.value);
    // On success, redirect to the dashboard
    router.push({ name: 'dashboard' }); 
  } catch (error) {
    message.value = error.message;
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