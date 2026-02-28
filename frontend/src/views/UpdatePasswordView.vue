<template>
  <div class="auth-page">
    <!-- Left Panel -->
    <div class="auth-left">
      <div class="auth-left-inner">
        <div class="auth-illustration">
          <div class="illus-orb illus-orb-1"></div>
          <div class="illus-orb illus-orb-2"></div>
          <div class="illus-icon">🔐</div>
          <h2>Secure Your Account</h2>
          <p>Please enter your new password below. Make sure it's something strong and memorable.</p>
        </div>
      </div>
    </div>

    <!-- Right Panel - Form -->
    <div class="auth-right">
      <div class="auth-form-card">
        <div class="form-header">
          <RouterLink to="/" class="form-logo">🌿 WasteFood</RouterLink>
          <h1>Update Password</h1>
          <p>Enter your new password to regain access to your account.</p>
        </div>

        <Transition name="fade-slide" mode="out-in">
          <div v-if="success" key="success" class="success-state">
            <div class="success-icon">🎉</div>
            <h3>Password Updated!</h3>
            <p>Your password has been successfully changed.</p>
            <RouterLink to="/login" class="btn-submit" style="text-decoration: none; margin-top: 1.5rem;">Go to Login →</RouterLink>
          </div>

          <form v-else key="form" @submit.prevent="handleUpdate" class="auth-form">
            
            <div class="field-wrap">
              <label>New Password</label>
              <div class="input-group">
                <span class="input-icon">🔒</span>
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Min 6 characters"
                  required
                />
                <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
              <div class="pw-strength" v-if="password">
                <div class="pw-bars">
                  <div v-for="i in 4" :key="i" class="pw-bar" :style="{ background: i <= passwordStrength.score ? passwordStrength.color : '#e2e8f0' }"></div>
                </div>
                <span :style="{ color: passwordStrength.color }">{{ passwordStrength.label }}</span>
              </div>
            </div>

            <div v-if="errorMsg" class="form-error">
              <span>⚠️</span> {{ errorMsg }}
            </div>

            <button type="submit" class="btn-submit" :disabled="isLoading || password.length < 6">
              <span v-if="isLoading" class="btn-spinner"></span>
              <span v-else>Update Password</span>
            </button>
          </form>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuth } from '../stores/auth';

const { updatePassword } = useAuth();
const password = ref('');
const errorMsg = ref('');
const isLoading = ref(false);
const success = ref(false);
const showPassword = ref(false);

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

const handleUpdate = async () => {
  if (password.value.length < 6) return;
  isLoading.value = true;
  errorMsg.value = '';
  try {
    await updatePassword(password.value);
    success.value = true;
  } catch (error) {
    errorMsg.value = error.message || 'Failed to update password. Your reset link may have expired.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Re-using identical structural styles from ForgotPassword/Register */
.auth-page { display: flex; min-height: 100vh; background: #fff; }

.auth-left {
  flex: 1; background: linear-gradient(135deg, #0a0f1e 0%, #1a3a2a 100%);
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden; padding: 2rem;
}
.auth-left-inner { max-width: 480px; width: 100%; position: relative; z-index: 2; margin-top: -3rem; }

.auth-illustration { text-align: center; }
.illus-orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.3; }
.illus-orb-1 { width: 300px; height: 300px; background: #10b981; top: -50px; left: -50px; animation: float 8s ease-in-out infinite; }
.illus-orb-2 { width: 250px; height: 250px; background: #6366f1; bottom: -100px; right: -50px; animation: float 6s ease-in-out infinite reverse; }
.illus-icon { font-size: 4rem; margin-bottom: 1.5rem; animation: float 4s ease-in-out infinite; }
.auth-illustration h2 { color: #fff; font-size: 2.5rem; margin-bottom: 1rem; }
.auth-illustration p { color: rgba(255,255,255,0.8); font-size: 1.1rem; line-height: 1.6; }

@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }

.auth-right {
  flex: 1; display: flex; align-items: center; justify-content: center;
  padding: 2rem; position: relative;
}
.auth-form-card { max-width: 440px; width: 100%; }
.form-header { margin-bottom: 2.5rem; }
.form-logo { display: inline-block; font-size: 1.25rem; font-weight: 800; color: #10b981; text-decoration: none; margin-bottom: 1.5rem; }
.form-header h1 { color: #0f172a; font-size: 2rem; margin-bottom: 0.5rem; }
.form-header p { color: #64748b; font-size: 1rem; }

.auth-form { display: flex; flex-direction: column; gap: 1.5rem; }
.field-wrap label { display: block; font-weight: 600; font-size: 0.9rem; color: #374151; margin-bottom: 0.5rem; }
.input-group {
  display: flex; align-items: center; border: 1.5px solid #e2e8f0;
  border-radius: 12px; background: #f8fafc; transition: all 0.3s ease; overflow: hidden; position: relative;
}
.input-group:focus-within { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.12); }
.input-icon { padding: 0 0.85rem; font-size: 1.1rem; }
.input-group input {
  flex: 1; padding: 0.85rem 2.5rem 0.85rem 0; border: none;
  background: transparent; outline: none; font-size: 1rem; font-family: 'Inter', sans-serif;
  color: #0f172a; width: 100%;
}
.toggle-pw { position: absolute; right: 0.8rem; background: none; border: none; cursor: pointer; font-size: 1.1rem; opacity: 0.6; transition: opacity 0.3s ease; }
.toggle-pw:hover { opacity: 1; }

.pw-strength { display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem; }
.pw-bars { display: flex; gap: 0.3rem; }
.pw-bar { width: 44px; height: 4px; background: #e2e8f0; border-radius: 2px; transition: background 0.4s ease; }
.pw-strength span { font-size: 0.8rem; font-weight: 600; }

.btn-submit {
  width: 100%; padding: 1rem; background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border: none; border-radius: 12px; font-size: 1rem; font-weight: 700;
  cursor: pointer; transition: all 0.3s ease; display: flex; justify-content: center; align-items: center; min-height: 52px;
  box-shadow: 0 4px 14px rgba(16,185,129,0.25);
}
.btn-submit:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(16,185,129,0.4); }
.btn-submit:disabled { opacity: 0.7; cursor: not-allowed; }
.btn-spinner { width: 22px; height: 22px; border: 2.5px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.form-error { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; color: #dc2626; font-size: 0.9rem; }

/* Success state */
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-10px); }
.success-state { text-align: center; padding: 2rem 0; }
.success-icon { font-size: 4rem; margin-bottom: 1rem; }
.success-state h3 { font-size: 1.5rem; color: #0f172a; margin-bottom: 0.5rem; }
.success-state p { color: #475569; margin-bottom: 1.5rem; line-height: 1.6; }

@media (max-width: 900px) {
  .auth-page { flex-direction: column; padding-top: 72px; }
  .auth-left { padding: 3rem 1.5rem; flex: none; min-height: 40vh; }
}
</style>
