<template>
  <div class="auth-page">
    <!-- Left Panel -->
    <div class="auth-left">
      <div class="auth-left-inner">
        <RouterLink to="/" class="back-home">← Back to Home</RouterLink>
        <div class="auth-illustration">
          <div class="illus-orb illus-orb-1"></div>
          <div class="illus-orb illus-orb-2"></div>
          <div class="illus-icon">🤝</div>
          <h2>Join the movement!</h2>
          <p>Create your free account and start sharing food or finding meals in your community today.</p>
          <div class="perks">
            <div class="perk" v-for="p in perks" :key="p">
              <span class="perk-check">✓</span> {{ p }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Panel - Form -->
    <div class="auth-right">
      <div class="auth-form-card">
        <div class="form-header">
          <RouterLink to="/" class="form-logo">🌿 WasteFood</RouterLink>
          <h1>Create Account</h1>
          <p>Free to join. Start making a difference today.</p>
        </div>

        <form @submit.prevent="handleRegister" class="auth-form">
          <div class="field-wrap">
            <label>Email Address</label>
            <div class="input-group">
              <span class="input-icon">📧</span>
              <input v-model="email" type="email" placeholder="you@example.com" autocomplete="email" required />
            </div>
          </div>

          <div class="field-wrap">
            <label>Username <small>(public, min 3 chars)</small></label>
            <div class="input-group">
              <span class="input-icon">👤</span>
              <input v-model="username" type="text" placeholder="your_name" autocomplete="username" />
            </div>
          </div>

          <div class="field-wrap">
            <label>Password</label>
            <div class="input-group">
              <span class="input-icon">🔒</span>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Min 6 characters"
                autocomplete="new-password"
                required
              />
              <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
            <!-- Password strength -->
            <div class="pw-strength" v-if="password.length > 0">
              <div class="pw-bars">
                <div v-for="i in 4" :key="i"
                  class="pw-bar"
                  :class="{ active: i <= passwordStrength.score }"
                  :style="{ background: i <= passwordStrength.score ? passwordStrength.color : '' }"
                ></div>
              </div>
              <span :style="{ color: passwordStrength.color }">{{ passwordStrength.label }}</span>
            </div>
          </div>

          <div v-if="message" class="form-message" :class="{ error: isError }">
            <span>{{ isError ? '⚠️' : '✅' }}</span> {{ message }}
          </div>

          <button type="submit" class="btn-submit" :disabled="isLoading">
            <span v-if="isLoading" class="btn-spinner"></span>
            <span v-else>Create Account →</span>
          </button>

          <p class="form-switch">
            Already have an account?
            <RouterLink to="/login">Sign in here</RouterLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const { signUp } = useAuth();
const router = useRouter();
const email = ref('');
const username = ref('');
const password = ref('');
const message = ref('');
const isLoading = ref(false);
const isError = ref(false);
const showPassword = ref(false);

const perks = [
  'Free to join — no credit card needed',
  'List surplus food in under 1 minute',
  'Find food available in your area',
  'Approve who receives your donations',
];

const passwordStrength = computed(() => {
  const pw = password.value;
  let score = 0;
  if (pw.length >= 6) score++;
  if (pw.length >= 10) score++;
  if (/[A-Z]/.test(pw) && /[0-9]/.test(pw)) score++;
  if (/[^a-zA-Z0-9]/.test(pw)) score++;
  const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
  const colors = ['', '#ef4444', '#f59e0b', '#3b82f6', '#10b981'];
  return { score, label: labels[score] || 'Weak', color: colors[score] || '#ef4444' };
});

const handleRegister = async () => {
  if (!username.value || username.value.length < 3) {
    message.value = 'Username must be at least 3 characters.';
    isError.value = true;
    return;
  }
  isLoading.value = true;
  message.value = '';
  try {
    await signUp(email.value, password.value, username.value);
    router.push({ name: 'dashboard' });
  } catch (error) {
    message.value = error.message;
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.auth-page { display: flex; min-height: 100vh; }

.auth-left {
  display: none;
  width: 45%;
  background: linear-gradient(135deg, #0a0f1e 0%, #0f2027 40%, #1a2a4a 100%);
  position: relative;
  overflow: hidden;
}
@media (max-width: 900px) {
  .auth-page { flex-direction: column; padding-top: 72px; }
  .auth-left { padding: 3rem 1.5rem; flex: none; min-height: 40vh; }
}
@media (min-width: 900px) { .auth-left { display: flex; align-items: center; justify-content: center; padding: 2rem; } }

.auth-left-inner { position: relative; z-index: 2; padding: 2rem; }
.back-home { display: inline-block; color: rgba(248,250,252,0.6); text-decoration: none; font-size: 0.9rem; margin-bottom: 3rem; transition: color 0.2s; }
.back-home:hover { color: #34d399; }

.illus-orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.25; }
.illus-orb-1 { width: 400px; height: 400px; background: #6366f1; top: -100px; right: -100px; animation: float 9s ease-in-out infinite; }
.illus-orb-2 { width: 300px; height: 300px; background: #10b981; bottom: -80px; left: -50px; animation: float 7s ease-in-out infinite reverse; }

.auth-illustration .illus-icon { font-size: 4rem; margin-bottom: 1.5rem; animation: float 5s ease-in-out infinite; display: block; }
.auth-illustration h2 { color: #f8fafc; font-size: 2rem; margin-bottom: 0.75rem; }
.auth-illustration p { color: rgba(248,250,252,0.65); font-size: 1rem; line-height: 1.7; margin-bottom: 1.5rem; }

.perks { display: flex; flex-direction: column; gap: 0.6rem; }
.perk { color: rgba(248,250,252,0.75); font-size: 0.9rem; display: flex; align-items: center; gap: 0.6rem; }
.perk-check { color: #10b981; font-weight: 800; }

/* Right panel */
.auth-right { flex: 1; display: flex; align-items: center; justify-content: center; padding: 2rem 1.5rem; background: #f8fafc; min-height: 100vh; }
.auth-form-card { width: 100%; max-width: 440px; animation: fadeInUp 0.6s ease both; }

.form-header { margin-bottom: 2rem; }
.form-logo { text-decoration: none; font-size: 1.2rem; font-weight: 800; color: #10b981; display: block; margin-bottom: 1.5rem; }
.form-header h1 { font-size: 2rem; color: #0f172a; margin-bottom: 0.5rem; }
.form-header p { color: #64748b; }

.auth-form { display: flex; flex-direction: column; }
.field-wrap { margin-bottom: 1.25rem; }
.field-wrap label { display: block; font-weight: 600; font-size: 0.9rem; color: #374151; margin-bottom: 0.5rem; }
.field-wrap label small { font-weight: 400; color: #94a3b8; }
.input-group { position: relative; display: flex; align-items: center; }
.input-icon { position: absolute; left: 0.9rem; font-size: 1rem; pointer-events: none; z-index: 1; }
.input-group input {
  width: 100%; padding: 0.9rem 1rem 0.9rem 2.75rem;
  border: 1.5px solid #e2e8f0; border-radius: 12px;
  background: #fff; font-size: 1rem; color: #0f172a;
  transition: all 0.3s ease; outline: none; font-family: 'Inter', sans-serif;
}
.input-group input:focus { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.15); }
.input-group input::placeholder { color: #94a3b8; }
.toggle-pw { position: absolute; right: 0.9rem; background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0.25rem; line-height: 1; }

/* Password strength */
.pw-strength { display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem; }
.pw-bars { display: flex; gap: 0.3rem; }
.pw-bar { width: 44px; height: 4px; background: #e2e8f0; border-radius: 2px; transition: background 0.4s ease; }
.pw-strength span { font-size: 0.8rem; font-weight: 600; }

.form-message {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.75rem 1rem; border-radius: 10px;
  font-size: 0.9rem; margin-bottom: 1rem;
  background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46;
}
.form-message.error { background: #fef2f2; border-color: #fecaca; color: #dc2626; }

.btn-submit {
  width: 100%; padding: 1rem; margin-top: 0.25rem;
  background: linear-gradient(135deg, #10b981, #059669); color: #fff;
  font-size: 1rem; font-weight: 700; font-family: 'Inter', sans-serif;
  border: none; border-radius: 12px; cursor: pointer;
  transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(16,185,129,0.3);
  display: flex; align-items: center; justify-content: center; min-height: 52px;
}
.btn-submit:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(16,185,129,0.4); }
.btn-submit:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }

.btn-spinner {
  width: 20px; height: 20px;
  border: 2.5px solid rgba(255,255,255,0.4);
  border-top-color: #fff; border-radius: 50%;
  animation: spin 0.7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

.form-switch { text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 1.25rem; }
.form-switch a { color: #10b981; font-weight: 600; text-decoration: none; }
.form-switch a:hover { text-decoration: underline; }

@keyframes fadeInUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-18px); } }
</style>