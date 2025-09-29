<template>
  <header>
    <nav>
      <RouterLink to="/" class="logo">WasteFood</RouterLink>

      <!-- Logged-out Links -->
      <div v-if="!userSession" class="nav-links">
        <a href="/#home" @click.prevent="scrollToSection('home')">Home</a>
        <a href="/#about" @click.prevent="scrollToSection('about')">About Us</a>
        <a href="/#contact" @click.prevent="scrollToSection('contact')">Contact</a>
      </div>
      
      <!-- Logged-in Links -->
      <div v-else class="nav-links">
        <RouterLink to="/dashboard">Dashboard</RouterLink>
        <RouterLink to="/my-donations">My Donations</RouterLink>
      </div>

      <div class="auth-links">
        <template v-if="userSession">
          <a href="#" @click.prevent="handleLogout" class="nav-button-outline">Logout</a>
        </template>
        <template v-else>
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/register" class="nav-button">Register</RouterLink>
        </template>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const { userSession, signOut } = useAuth();
const router = useRouter();

const handleLogout = async () => {
  await signOut();
  router.push({ name: 'home' });
};

const scrollToSection = (sectionId) => {
  if (router.currentRoute.value.path === '/') {
    const element = document.getElementById(sectionId);
    if (element) element.scrollIntoView({ behavior: 'smooth' });
  } else {
    router.push({ path: '/', hash: `#${sectionId}` });
  }
};
</script>

<style scoped>
/* Use the same professional styles from our previous conversation */
header { background-color: white; color: #333; padding: 0.5rem; border-bottom: 1px solid #eee; }
nav { display: flex; justify-content: space-between; align-items: center; height: 70px; max-width: 1200px; margin:0.5px; }
.logo { font-weight: bold; font-size: 1.5rem; text-decoration: none; color: #42b983; }
.nav-links, .auth-links { display: flex; align-items: center; gap: 1.5rem; }
.nav-links a, .auth-links a { color: #333; text-decoration: none; font-weight: 500; transition: color 0.3s; }
.nav-links a:hover, .auth-links a:hover { color: #42b983; }
.nav-links .router-link-exact-active { color: #42b983; border-bottom: 2px solid #42b983; }
.nav-button {
  background-color: #42b983; color: white !important; padding: 8px 16px;
  border-radius: 5px; transition: background-color 0.3s;
}
.nav-button:hover { background-color: #36a473; }
.nav-button-outline {
  background-color: transparent; color: #333 !important; padding: 7px 15px;
  border-radius: 5px; border: 1px solid #ccc;
}
</style>