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
          <RouterLink to="/requests" class="nav-item-with-badge">
            Requests <span v-if="pendingRequestsCount > 0" class="badge-dot"></span>
          </RouterLink>
          <RouterLink to="/my-donations">My Donations</RouterLink>
        </div>

        <div class="auth-links">
          <template v-if="userSession">
            <div class="user-dropdown-container">
              <div class="user-pill" @click="toggleProfileDropdown">
                <img v-if="userProfilePic" :src="userProfilePic" class="nav-profile-pic" />
                <div v-else class="nav-profile-pic-placeholder">
                  {{ getInitial(userEmail) }}
                </div>
              </div>

              <!-- Dropdown Menu -->
              <Transition name="dropdown-fade">
                <div v-if="isProfileDropdownOpen" class="profile-dropdown" v-click-outside="closeProfileDropdown">
                  <div class="dropdown-header">
                    <strong>{{ userFullName || 'User' }}</strong>
                    <span>{{ userSession.user.email }}</span>
                  </div>
                  <div class="dropdown-body">
                    <RouterLink to="/dashboard" @click="closeProfileDropdown">
                      <span class="dd-icon">❖</span> Dashboard
                    </RouterLink>
                    <RouterLink to="/profile-settings" @click="closeProfileDropdown">
                      <span class="dd-icon">👤</span> Profile Settings
                    </RouterLink>
                    <RouterLink to="/update-password" @click="closeProfileDropdown">
                      <span class="dd-icon">🔑</span> Reset Password
                    </RouterLink>
                  </div>
                  <div class="dropdown-footer">
                    <a href="#" @click.prevent="handleLogout" class="logout-link">
                      <span class="dd-icon">🚪</span> Logout
                    </a>
                  </div>
                </div>
              </Transition>
            </div>
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
        <RouterLink to="/requests" @click="closeMobileMenu" class="nav-item-mobile-badge">
          Requests <span v-if="pendingRequestsCount > 0" class="badge-dot-mobile">{{ pendingRequestsCount }}</span>
        </RouterLink>
        <RouterLink to="/my-donations" @click="closeMobileMenu">My Donations</RouterLink>
        <RouterLink to="/profile-settings" @click="closeMobileMenu">Profile Settings</RouterLink>
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
import { supabase } from '../supabase';
import apiClient from '@/api';

const { userSession, signOut } = useAuth();
const router = useRouter();

const isMobileMenuOpen = ref(false);
const isScrolled = ref(false);
const isProfileDropdownOpen = ref(false);
const userFullName = ref('');
const pendingRequestsCount = ref(0);

const userEmail = computed(() => {
  if (!userSession.value) return '';
  const email = userSession.value.user?.email || '';
  return email.split('@')[0];
});

const userProfilePic = computed(() => {
  return userSession.value?.user?.user_metadata?.avatar_url || null;
});

const getInitial = (name) => {
  return name ? name.charAt(0).toUpperCase() : 'U';
};

const fetchUserProfile = async () => {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (session) {
      const response = await apiClient.get('/api/profile', {
        headers: { Authorization: `Bearer ${session.access_token}` },
      });
      userFullName.value = response.data.username;
    }
  } catch (error) {
    console.error("Failed to fetch full name:", error);
  }
};

const fetchPendingRequestsCount = async () => {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (session) {
      const response = await apiClient.get('/api/incoming-requests', {
        headers: { Authorization: `Bearer ${session.access_token}` },
      });
      pendingRequestsCount.value = response.data.filter(req => req.status === 'pending').length;
    }
  } catch (error) {
    console.error("Failed to fetch pending requests:", error);
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  if (userSession.value) {
    fetchUserProfile();
    fetchPendingRequestsCount();
  }
  // Listen for request approvals to update count
  window.addEventListener('request-approved', fetchPendingRequestsCount);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('request-approved', fetchPendingRequestsCount);
});

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

const toggleProfileDropdown = () => { isProfileDropdownOpen.value = !isProfileDropdownOpen.value; };
const closeProfileDropdown = () => { isProfileDropdownOpen.value = false; };

// Click outside directive (simplified)
const vClickOutside = {
  mounted: (el, binding) => {
    el.clickOutsideEvent = event => {
      if (!(el == event.target || el.contains(event.target) || event.target.closest('.user-pill'))) {
        binding.value();
      }
    };
    document.body.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted: el => {
    document.body.removeEventListener('click', el.clickOutsideEvent);
  },
};

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
  background:rgba(10, 15, 30, 0.85);
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

.nav-item-with-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.badge-dot {
  width: 8px;
  height: 8px;
  background-color: #ef4444;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
  animation: pulse 2s infinite;
}

.nav-item-mobile-badge {
  display: flex !important;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.badge-dot-mobile {
  background-color: #ef4444;
  color: #fff;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.1rem 0.5rem;
  border-radius: 9999px;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
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

.user-dropdown-container {
  position: relative;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.6rem 0.25rem 0.25rem;
  cursor: pointer;
}
.nav-profile-pic {
  width: 36px; height: 36px; border-radius: 50%; object-fit: cover;
  border: 2px solid transparent; transition: all 0.2s;
}
.nav-profile-pic:hover, .user-pill:hover .nav-profile-pic { border-color: #3b82f6; transform: scale(1.05); }
.nav-profile-pic-placeholder {
  width: 36px; height: 36px; border-radius: 50%; background: #2563eb;
  color: white; display: flex; align-items: center; justify-content: center;
  font-weight: bold; transition: all 0.2s;
}
.user-pill:hover .nav-profile-pic-placeholder { background: #1d4ed8; transform: scale(1.05); }

/* Dropdown styling */
.profile-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 240px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.12);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  z-index: 1000;
}

.dropdown-fade-enter-active, .dropdown-fade-leave-active { transition: all 0.2s ease; }
.dropdown-fade-enter-from, .dropdown-fade-leave-to { opacity: 0; transform: translateY(-10px); }

.dropdown-header {
  padding: 1rem;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}
.dropdown-header strong { display: block; color: #0f172a; font-size: 0.95rem; margin-bottom: 0.1rem; }
.dropdown-header span { color: #64748b; font-size: 0.8rem; }

.dropdown-body {
  padding: 0.5rem 0;
}
.dropdown-body a {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.65rem 1rem; color: #334155;
  text-decoration: none; font-size: 0.9rem; font-weight: 500;
  transition: background 0.2s;
}
.dropdown-body a:hover { background: #f1f5f9; color: #0f172a; }
.dd-icon { font-size: 1.1rem; width: 20px; text-align: center; }

.dropdown-footer {
  padding: 0.5rem 0;
  border-top: 1px solid #f1f5f9;
}
.logout-link {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.65rem 1rem; color: #ef4444;
  text-decoration: none; font-size: 0.9rem; font-weight: 500;
  transition: background 0.2s;
}
.logout-link:hover { background: #fef2f2; }

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