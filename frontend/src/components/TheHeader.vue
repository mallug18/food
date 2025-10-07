<template>
  <header>
    <nav>
      <RouterLink to="/" class="logo">WasteFood</RouterLink>

      <div v-if="!userSession" class="nav-links">
        <a href="/#home" @click.prevent="scrollToSection('home')">Home</a>
        <a href="/#about" @click.prevent="scrollToSection('about')">About Us</a>
        <a href="/#contact" @click.prevent="scrollToSection('contact')">Contact</a>
      </div>
      
      <div v-else class="nav-links">
        <RouterLink to="/dashboard">Dashboard</RouterLink>
        <RouterLink to="/my-donations">My Donations</RouterLink>
      </div>

      <div class="auth-links">
        <template v-if="userSession">
          <a href="#" @click.prevent="handleLogout" class="nav-button-outline">Logout</a>
        </template>
        <template v-else>
          <RouterLink to="/login" class="nav-button">Login</RouterLink>
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
header {
  background-color: rgba(118, 130, 107, 0.753);
  color: #ffffff;
  border-bottom: 1px solid #eee;
  /* --- CHANGED --- */
  /* Only apply vertical padding to the full-width header */
  padding: 0.5rem 0;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  /* --- CHANGED: These lines now match your body's .section-container --- */
  max-width: 1100px; /* Was 1200px */
  margin: 0 auto;     /* Was 0.5px. This properly centers the nav. */
  padding: 0 1rem;   /* Added side padding to match body content on mobile. */
}

.logo {
  font-weight: bold;
  font-size: 1.5rem;
  text-decoration: none;
  color: #42b983;
  /* --- CHANGED --- */
  margin-left: 0; /* Removed margin, as parent padding now handles spacing. */
}

.nav-links, .auth-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links a, .auth-links a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a:hover, .auth-links a:hover {
  color: #42b983;
}

.nav-links .router-link-exact-active {
  color: #42b983;
  border-bottom: 2px solid #42b983;
}

.nav-button {
  background-color: #42b983;
  color: white !important;
  padding: 8px 16px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-button:hover {
  background-color: #36a473;
}

.nav-button-outline {
  background-color: transparent;
  color: #333 !important;
  padding: 7px 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

/* --- ADDED: Media query to match body's desktop padding --- */
@media (min-width: 769px) {
  nav {
    padding: 0 2rem;
  }
}
</style>