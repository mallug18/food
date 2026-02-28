<template>
  <div class="auth-page">
    <!-- Left Panel -->
    <div class="auth-left">
      <div class="auth-left-inner">
        <RouterLink to="/" class="back-home">← Back to Home</RouterLink>
        <div class="auth-illustration">
          <div class="illus-orb illus-orb-1"></div>
          <div class="illus-orb illus-orb-2"></div>
          <div class="illus-icon"><img src="/favicon.png" alt="Logo" style="width: 48px; height: 48px; object-fit: contain;" /></div>
          <h2>Welcome back!</h2>
          <p>Log in to share food, request donations, and track your impact in the community.</p>
          <div class="auth-stats">
            <div class="auth-stat"><span class="auth-stat-num">10K+</span><small>Meals Shared</small></div>
            <div class="auth-stat"><span class="auth-stat-num">500+</span><small>Donors</small></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Panel - Form -->
    <div class="auth-right">
      <div class="auth-form-card">
        <div class="form-header">
          <RouterLink to="/" class="form-logo"><img src="/favicon.png" alt="Logo" style="width: 24px; height: 24px; margin-right: 8px; vertical-align: middle;" />WasteFood</RouterLink>
          <h1>Sign In</h1>
          <p>Continue your mission to reduce food waste</p>
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="field-wrap">
            <label>Email Address</label>
            <div class="input-group">
              <span class="input-icon">📧</span>
              <input
                v-model="email"
                type="email"
                placeholder="you@example.com"
                autocomplete="email"
                required
              />
            </div>
          </div>

          <div class="field-wrap">
            <div class="label-row" style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
              <label style="margin-bottom: 0;">Password</label>
              <RouterLink to="/forgot-password" class="forgot-link" style="font-size: 0.85rem; color: #10b981; font-weight: 500; text-decoration: none;">Forgot Password?</RouterLink>
            </div>
            <div class="input-group">
              <span class="input-icon">🔒</span>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                autocomplete="current-password"
                required
              />
              <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <div v-if="errorMsg" class="form-error">
            <span>⚠️</span> {{ errorMsg }}
          </div>

          <button type="submit" class="btn-submit" :disabled="isLoading">
            <span v-if="isLoading" class="btn-spinner"></span>
            <span v-else>Sign In →</span>
          </button>

          <p class="form-switch">
            Don't have an account?
            <RouterLink to="/register">Create one free</RouterLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const { signIn } = useAuth();
const router = useRouter();
const email = ref('');
const password = ref('');
const errorMsg = ref('');
const isLoading = ref(false);
const showPassword = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  errorMsg.value = '';
  try {
    await signIn(email.value, password.value);
    router.push({ name: 'dashboard' });
  } catch (error) {
    errorMsg.value = error.message;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
}

/* Left decorative panel */
.auth-left {
  display: none;
  width: 45%;
  background: linear-gradient(135deg, #0a0f1e 0%, #0f2027 40%, #1a3a2a 100%);
  position: relative;
  overflow: hidden;
  padding: 2rem;
}
@media (min-width: 900px) { .auth-left { display: flex; align-items: center; justify-content: center; } }

.auth-left-inner { position: relative; z-index: 2; padding: 2rem; }
.back-home {
  display: inline-block;
  color: rgba(248,250,252,0.6);
  text-decoration: none;
  font-size: 0.9rem;
  margin-bottom: 3rem;
  transition: color 0.2s;
}
.back-home:hover { color: #34d399; }

.illus-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.25;
}
.illus-orb-1 { width: 400px; height: 400px; background: #10b981; top: -100px; left: -100px; animation: float 8s ease-in-out infinite; }
.illus-orb-2 { width: 300px; height: 300px; background: #6366f1; bottom: -50px; right: -50px; animation: float 10s ease-in-out infinite reverse; }

.auth-illustration .illus-icon { font-size: 4rem; margin-bottom: 1.5rem; animation: float 5s ease-in-out infinite; display: block; }
.auth-illustration h2 { color: #f8fafc; font-size: 2rem; margin-bottom: 0.75rem; }
.auth-illustration p { color: rgba(248,250,252,0.65); font-size: 1rem; line-height: 1.7; margin-bottom: 2rem; }
.auth-stats { display: flex; gap: 2rem; }
.auth-stat { display: flex; flex-direction: column; }
.auth-stat-num { font-size: 1.75rem; font-weight: 800; background: linear-gradient(135deg, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.auth-stat small { color: rgba(248,250,252,0.55); font-size: 0.85rem; }

/* Right form panel */
.auth-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  background: #f8fafc;
  min-height: 100vh;
}

.auth-form-card {
  width: 100%;
  max-width: 440px;
  animation: fadeInUp 0.6s ease both;
}

.form-header { margin-bottom: 2.5rem; }
.form-logo { text-decoration: none; font-size: 1.2rem; font-weight: 800; color: #10b981; display: block; margin-bottom: 1.5rem; }
.form-header h1 { font-size: 2rem; color: #0f172a; margin-bottom: 0.5rem; }
.form-header p { color: #64748b; }

.auth-form { display: flex; flex-direction: column; gap: 0; }
.field-wrap { margin-bottom: 1.25rem; }
.field-wrap label { display: block; font-weight: 600; font-size: 0.9rem; color: #374151; margin-bottom: 0.5rem; }
.input-group { position: relative; display: flex; align-items: center; }
.input-icon { position: absolute; left: 0.9rem; font-size: 1rem; pointer-events: none; z-index: 1; }
.input-group input {
  width: 100%;
  padding: 0.9rem 1rem 0.9rem 2.75rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
  font-size: 1rem;
  color: #0f172a;
  transition: all 0.3s ease;
  outline: none;
  font-family: 'Inter', sans-serif;
}
.input-group input:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.15);
}
.input-group input::placeholder { color: #94a3b8; }
.toggle-pw {
  position: absolute;
  right: 0.9rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.25rem;
  line-height: 1;
}

.form-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #dc2626;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.btn-submit {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
  font-family: 'Inter', sans-serif;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(16,185,129,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  margin-top: 0.25rem;
}
.btn-submit:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(16,185,129,0.4); }
.btn-submit:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }

.btn-spinner {
  width: 20px; height: 20px;
  border: 2.5px solid rgba(255,255,255,0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

.form-switch {
  text-align: center;
  color: #64748b;
  font-size: 0.9rem;
  margin-top: 1.25rem;
}
.form-switch a { color: #10b981; font-weight: 600; text-decoration: none; }
.form-switch a:hover { text-decoration: underline; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-18px); }
}
</style>