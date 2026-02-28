<template>
  <header :class="{ 'scrolled': isScrolled }">
    <nav class="nav-inner">
      <!-- Logo -->
      <RouterLink to="/" class="logo">
        <img src="/favicon.png" alt="WasteFood Logo" class="logo-icon" />
        <span class="logo-text">Waste<span class="logo-accent">Food</span></span>
      </RouterLink>

      <!-- Desktop Nav -->
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
            <div class="user-pill">
              <span class="user-dot"></span>
              <span>{{ userEmail }}</span>
            </div>
            <a href="#" @click.prevent="handleLogout" class="btn-nav-outline">Logout</a>
          </template>
          <template v-else>
            <RouterLink to="/login" class="btn-nav-ghost">Login</RouterLink>
            <RouterLink to="/register" class="btn-nav-solid">Get Started</RouterLink>
          </template>
        </div>
      </div>

      <!-- Hamburger -->
      <button
        class="hamburger"
        :class="{ 'is-open': isMobileMenuOpen }"
        @click="toggleMobileMenu"
        aria-label="Toggle navigation"
      >
        <span></span><span></span><span></span>
      </button>
    </nav>

    <!-- Mobile Menu -->
    <div class="mobile-menu" :class="{ 'is-open': isMobileMenuOpen }">
      <template v-if="!userSession">
        <a href="/#home" @click.prevent="closeMenuAndScrollTo('home')">Home</a>
        <a href="/#about" @click.prevent="closeMenuAndScrollTo('about')">About Us</a>
        <a href="/#contact" @click.prevent="closeMenuAndScrollTo('contact')">Contact</a>
      </template>
      <template v-else>
        <RouterLink to="/dashboard" @click="closeMobileMenu">Dashboard</RouterLink>
        <RouterLink to="/my-donations" @click="closeMobileMenu">My Donations</RouterLink>
      </template>
      <div class="mobile-auth">
        <template v-if="userSession">
          <a href="#" @click.prevent="handleLogout" class="btn-nav-outline" style="width:100%;text-align:center;">Logout</a>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn-nav-ghost" @click="closeMobileMenu">Login</RouterLink>
          <RouterLink to="/register" class="btn-nav-solid" @click="closeMobileMenu">Get Started</RouterLink>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const { userSession, signOut } = useAuth();
const router = useRouter();

const isMobileMenuOpen = ref(false);
const isScrolled = ref(false);

const userEmail = computed(() => {
  if (!userSession.value) return '';
  const email = userSession.value.user?.email || '';
  return email.split('@')[0];
});

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(() => window.addEventListener('scroll', handleScroll));
onUnmounted(() => window.removeEventListener('scroll', handleScroll));

const toggleMobileMenu = () => { isMobileMenuOpen.value = !isMobileMenuOpen.value; };
const closeMobileMenu = () => { isMobileMenuOpen.value = false; };

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
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: all 0.4s ease;
  padding: 0;
}

/* Transparent state */
header:not(.scrolled) {
  background:rgba(6, 2, 44, 0.347);
}

/* Scrolled → glassmorphism */
header.scrolled {
  background: rgba(10, 15, 30, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.nav-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 72px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-weight: 800;
  font-size: 1.4rem;
  transition: transform 0.3s ease;
}
.logo:hover { transform: scale(1.05); }
.logo-icon { width: 32px; height: 32px; object-fit: contain; }
.logo-text { color: #f8fafc; }
.logo-accent {
  background: linear-gradient(135deg, #10b981, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Desktop nav */
.desktop-nav {
  display: none;
  align-items: center;
  gap: 2rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.nav-links a {
  color: rgba(248, 250, 252, 0.85);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  position: relative;
  transition: color 0.3s ease, background 0.3s ease;
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 50%;
  width: 0;
  height: 2px;
  background: #10b981;
  border-radius: 2px;
  transform: translateX(-50%);
  transition: width 0.3s ease;
}

.nav-links a:hover { color: #fff; }
.nav-links a:hover::after { width: 70%; }
.nav-links .router-link-exact-active { color: #10b981; }
.nav-links .router-link-exact-active::after { width: 70%; }

/* Auth links */
.auth-links {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.85rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 9999px;
  color: #10b981;
  font-size: 0.85rem;
  font-weight: 500;
}
.user-dot {
  width: 6px; height: 6px;
  background: #10b981;
  border-radius: 50%;
  animation: breathe 2s ease-in-out infinite;
}
@keyframes breathe {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.7); }
}

.btn-nav-ghost {
  color: rgba(248, 250, 252, 0.85) !important;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}
.btn-nav-ghost:hover { color: #1ad52198 !important; background: rgba(255,255,255,0.08); }

.btn-nav-solid {
  color: #fff !important;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0.55rem 1.25rem;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 9999px;
  transition: all 0.3s ease;
  box-shadow: 0 40px 150px rgba(16, 185, 129, 0.3);
}
.btn-nav-solid:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.45);
}

.btn-nav-outline {
  color: rgba(248, 250, 252, 0.85) !important;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border: 1px solid rgba(5, 75, 14, 0.603);
  border-radius: 8px;
  transition: all 0.3s ease;
}
.btn-nav-outline:hover {
  border-color: rgba(255,255,255,0.5);
  background: rgba(255,255,255,0.08);
}

/* Hamburger */
.hamburger {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 28px;
  height: 22px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
}
.hamburger span {
  display: block;
  width: 100%;
  height: 2px;
  background: #f8fafc;
  border-radius: 2px;
  transition: all 0.35s cubic-bezier(0.645, 0.045, 0.355, 1);
  transform-origin: center;
}
.hamburger.is-open span:nth-child(1) { transform: translateY(10px) rotate(45deg); }
.hamburger.is-open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.hamburger.is-open span:nth-child(3) { transform: translateY(-10px) rotate(-45deg); }

/* Mobile Menu */
.mobile-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  background: rgba(10, 15, 30, 0.98);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  padding: 2rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  transform: translateY(-100%);
  opacity: 0;
  pointer-events: none;
  visibility: hidden;
  transition: transform 0.3s ease, opacity 0.3s ease, visibility 0.3s;
  position: absolute;
  top: 72px;
  left: 0;
  right: 0;
  height: max-content;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
.mobile-menu.is-open { transform: translateY(0); opacity: 1; pointer-events: auto; visibility: visible; }

.mobile-menu a {
  color: rgba(248, 250, 252, 0.85);
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  width: 100%;
  text-align: center;
  border-radius: 8px;
  transition: background 0.2s, color 0.2s;
}
.mobile-menu a:hover { background: rgba(255,255,255,0.07); color: #fff; }

.mobile-auth {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
  width: 100%;
  justify-content: center;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255,255,255,0.08);
}

/* Desktop breakpoint */
@media (min-width: 768px) {
  .desktop-nav { display: flex; }
  .hamburger { display: none; }
  .mobile-menu { display: none !important; }
}
</style>