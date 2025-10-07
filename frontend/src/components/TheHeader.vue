<template>
  <header>
    <nav>
      <RouterLink to="/" class="logo">WasteFood</RouterLink>

      <div class="desktop-nav">
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
      </div>

      <button class="hamburger-menu" @click="toggleMobileMenu" aria-label="Open navigation menu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </button>
    </nav>

    <div class="mobile-nav-menu" :class="{ 'is-open': isMobileMenuOpen }">
      <template v-if="!userSession">
        <a href="/#home" @click.prevent="closeMenuAndScrollTo('home')">Home</a>
        <a href="/#about" @click.prevent="closeMenuAndScrollTo('about')">About Us</a>
        <a href="/#contact" @click.prevent="closeMenuAndScrollTo('contact')">Contact</a>
      </template>
      
      <template v-else>
        <RouterLink to="/dashboard" @click="closeMobileMenu">Dashboard</RouterLink>
        <RouterLink to="/my-donations" @click="closeMobileMenu">My Donations</RouterLink>
      </template>

      <hr class="menu-divider" />
      <div class="mobile-auth-links">
        <template v-if="userSession">
          <a href="#" @click.prevent="handleLogout" class="nav-button-outline">Logout</a>
        </template>
        <template v-else>
          <RouterLink to="/login" class="nav-button" @click="closeMobileMenu">Login</RouterLink>
          <RouterLink to="/register" class="nav-button" @click="closeMobileMenu">Register</RouterLink>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const { userSession, signOut } = useAuth();
const router = useRouter();

// --- NEW: State for mobile menu ---
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const handleLogout = async () => {
  closeMobileMenu();
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

const closeMenuAndScrollTo = (sectionId) => {
  closeMobileMenu();
  scrollToSection(sectionId);
};
</script>

<style scoped>
header {
  background-color: white; /* Changed for better contrast with menu */
  color: #333;
  border-bottom: 1px solid #eee;
  padding: 0.5rem 0;
  position: relative; /* Needed for absolute positioning of mobile menu */
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1rem;
}

.logo {
  font-weight: bold;
  font-size: 1.5rem;
  text-decoration: none;
  color: #42b983;
  margin-left: 0;
}

/* --- Wrapper for all desktop navigation links --- */
.desktop-nav {
  display: none; /* Hidden by default, shown on desktop */
  align-items: center;
  gap: 1.5rem;
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
  text-align: center;
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
  text-align: center;
}

/* --- Hamburger Menu Styles --- */
.hamburger-menu {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 2rem;
  height: 2rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
}

.hamburger-menu:focus {
  outline: none;
}

.hamburger-menu .bar {
  width: 2rem;
  height: 0.25rem;
  background: #333;
  border-radius: 10px;
  transition: all 0.3s linear;
}

/* --- Mobile Menu Styles --- */
.mobile-nav-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  background: white;
  position: absolute;
  top: 80px; /* Height of the header */
  left: 0;
  width: 100%;
  padding: 1.5rem 0;
  border-bottom: 1px solid #eee;
  transform: translateY(-150%); /* Start off-screen */
  transition: transform 0.3s ease-in-out;
  opacity: 0;
}

.mobile-nav-menu.is-open {
  transform: translateY(0); /* Slide into view */
  opacity: 1;
}

.mobile-nav-menu a {
  color: #333;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;
}

.menu-divider {
  width: 80%;
  border: 0;
  border-top: 1px solid #eee;
  margin: 0.5rem 0;
}
.mobile-auth-links {
  display: flex;
  gap: 1rem;
}


/* --- DESKTOP STYLES (Breakpoint at 769px) --- */
@media (min-width: 769px) {
  nav {
    padding: 0 2rem;
  }
  
  .desktop-nav {
    display: flex; /* Show desktop nav container */
  }

  .hamburger-menu {
    display: none; /* Hide hamburger on desktop */
  }
  
  .mobile-nav-menu {
    display: none; /* Hide mobile menu on desktop */
  }
}
</style>