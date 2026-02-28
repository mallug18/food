<template>
  <div class="auth-page">
    <!-- Left Panel -->
    <div class="auth-left">
      <div class="auth-left-inner">
        <RouterLink to="/login" class="back-home">← Back to Login</RouterLink>
        <div class="auth-illustration">
          <div class="illus-orb illus-orb-1"></div>
          <div class="illus-orb illus-orb-2"></div>
          <div class="illus-icon">🔑</div>
          <h2>Reset Password</h2>
          <p>Don't worry, it happens to the best of us. Enter your email and we'll send you a link to reset your password.</p>
        </div>
      </div>
    </div>

    <!-- Right Panel - Form -->
    <div class="auth-right">
      <div class="auth-form-card">
        <div class="form-header">
          <RouterLink to="/" class="form-logo"><img src="/favicon.png" alt="Logo" style="width: 24px; height: 24px; margin-right: 8px; vertical-align: middle;" />WasteFood</RouterLink>
          <h1>Forgot Password</h1>
          <p>We'll email you instructions to reset your password.</p>
        </div>

        <Transition name="fade-slide" mode="out-in">
          <div v-if="emailSent" key="success" class="success-state">
            <div class="success-icon">📬</div>
            <h3>Check your email!</h3>
            <p>If an account exists for <strong>{{ email }}</strong>, you will receive a password reset link shortly.</p>
            <p class="spam-note">Don't forget to check your spam folder.</p>
            <button class="btn-outline-green" @click="emailSent = false">Send again</button>
          </div>

          <form v-else key="form" @submit.prevent="handleReset" class="auth-form">
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

            <div v-if="errorMsg" class="form-error">
              <span>⚠️</span> {{ errorMsg }}
            </div>

            <button type="submit" class="btn-submit" :disabled="isLoading">
              <span v-if="isLoading" class="btn-spinner"></span>
              <span v-else>Send Reset Link →</span>
            </button>
          </form>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuth } from '../stores/auth';

const { resetPassword } = useAuth();
const email = ref('');
const errorMsg = ref('');
const isLoading = ref(false);
const emailSent = ref(false);

const handleReset = async () => {
  if (!email.value) return;
  isLoading.value = true;
  errorMsg.value = '';
  try {
    await resetPassword(email.value);
    emailSent.value = true;
  } catch (error) {
    errorMsg.value = error.message || 'Failed to send reset email. Please try again.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Re-using LoginView styles for the split screen */
.auth-page { display: flex; min-height: 100vh; background: #fff; }

.auth-left {
  flex: 1; background: linear-gradient(135deg, #0a0f1e 0%, #1a3a2a 100%);
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden; padding: 2rem;
}
.auth-left-inner { max-width: 480px; width: 100%; position: relative; z-index: 2; }
.back-home {
  display: inline-block; color: rgba(255,255,255,0.7); text-decoration: none;
  font-size: 0.9rem; margin-bottom: 3rem; transition: color 0.3s;
}
.back-home:hover { color: #fff; }

.auth-illustration { text-align: center; }
.illus-orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.3; }
.illus-orb-1 { width: 300px; height: 300px; background: #10b981; top: -50px; left: -50px; animation: float 8s ease-in-out infinite; }
.illus-orb-2 { width: 250px; height: 250px; background: #6366f1; bottom: 0; right: -50px; animation: float 6s ease-in-out infinite reverse; }
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
  border-radius: 12px; background: #f8fafc; transition: all 0.3s ease; overflow: hidden;
}
.input-group:focus-within { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.12); }
.input-icon { padding: 0 0.85rem; font-size: 1.1rem; }
.input-group input {
  flex: 1; padding: 0.85rem 0.85rem 0.85rem 0; border: none;
  background: transparent; outline: none; font-size: 1rem; font-family: 'Inter', sans-serif;
  color: #0f172a; width: 100%;
}

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
.success-state h3 { font-size: 1.5rem; color: #0f172a; margin-bottom: 1rem; }
.success-state p { color: #475569; margin-bottom: 0.5rem; line-height: 1.6; }
.spam-note { color: #94a3b8; font-size: 0.85rem; margin-top: 1rem; margin-bottom: 2rem !important; }

.btn-outline-green {
  padding: 0.6rem 1.25rem; border: 1.5px solid #10b981; background: transparent;
  color: #10b981; border-radius: 9999px; font-weight: 600; cursor: pointer;
  transition: all 0.3s ease; font-family: 'Inter', sans-serif;
}
.btn-outline-green:hover { background: rgba(16,185,129,0.1); }

@media (max-width: 900px) {
  .auth-page { flex-direction: column; padding-top: 72px; }
  .auth-left { padding: 3rem 1.5rem; flex: none; min-height: 40vh; }
}
</style>
