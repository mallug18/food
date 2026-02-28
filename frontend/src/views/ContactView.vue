<template>
  <div class="contact-page">
    <!-- Hero -->
    <section class="contact-hero">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="hero-content section-wrap">
        <span class="section-badge">📬 Get In Touch</span>
        <h1>We'd Love to <span class="grad-text">Hear From You</span></h1>
        <p>Whether you have a question, want to partner with us, or just want to say hello — reach out!</p>
      </div>
    </section>

    <!-- Main content -->
    <section class="contact-body">
      <div class="section-wrap contact-grid">
        <!-- Form -->
        <div class="contact-form-wrap">
          <h2>Send a Message</h2>

          <Transition name="success-fade" mode="out-in">
            <div v-if="sent" class="success-state" key="success">
              <div class="success-icon">🎉</div>
              <h3>Message Sent!</h3>
              <p>Thank you for reaching out. We'll get back to you within 24 hours.</p>
              <button @click="sent = false" class="send-again">Send Another</button>
            </div>

            <form v-else key="form" @submit.prevent="handleSubmit" class="form-inner">
              <div class="field-wrap">
                <label>Your Name</label>
                <div class="input-row">
                  <span>👤</span>
                  <input v-model="form.name" type="text" placeholder="Full name" required />
                </div>
              </div>
              <div class="field-wrap">
                <label>Email Address</label>
                <div class="input-row">
                  <span>📧</span>
                  <input v-model="form.email" type="email" placeholder="you@example.com" required />
                </div>
              </div>
              <div class="field-wrap">
                <label>Subject</label>
                <div class="input-row">
                  <span>💬</span>
                  <input v-model="form.subject" type="text" placeholder="What's this about?" required />
                </div>
              </div>
              <div class="field-wrap">
                <label>Message</label>
                <div class="input-row textarea-row">
                  <span>📝</span>
                  <textarea v-model="form.message" rows="5" placeholder="Tell us more…" required></textarea>
                </div>
              </div>
              <button type="submit" class="submit-btn" :disabled="sending">
                <span v-if="sending" class="spin-ring"></span>
                <template v-else><span>🚀</span> Send Message</template>
              </button>
            </form>
          </Transition>
        </div>

        <!-- Info cards -->
        <div class="info-side">
          <div v-for="info in contactInfo" :key="info.label" class="info-card">
            <div class="info-icon">{{ info.icon }}</div>
            <div>
              <h4>{{ info.label }}</h4>
              <p>{{ info.value }}</p>
            </div>
          </div>

          <div class="map-placeholder">
            <iframe
              src="https://maps.google.com/maps?q=Bengaluru,Karnataka,India&output=embed"
              width="100%"
              height="220"
              style="border:0; border-radius:12px;"
              allowfullscreen=""
              loading="lazy"
            ></iframe>
          </div>

          <div class="social-row">
            <a href="#" class="social-chip">𝕏 Twitter</a>
            <a href="#" class="social-chip">📸 Instagram</a>
            <a href="#" class="social-chip">💼 LinkedIn</a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({ name: '', email: '', subject: '', message: '' });
const sending = ref(false);
const sent = ref(false);

const contactInfo = [
  { icon: '📧', label: 'Email', value: 'contact@wastefood.com' },
  { icon: '📍', label: 'Address', value: '123 Tech Park, Bengaluru, Karnataka, India' },
  { icon: '⏰', label: 'Response Time', value: 'We typically reply within 24 hours' },
];

async function handleSubmit() {
  sending.value = true;
  // Simulate sending (replace with real API call if needed)
  await new Promise(r => setTimeout(r, 1500));
  sending.value = false;
  sent.value = true;
  form.value = { name: '', email: '', subject: '', message: '' };
}
</script>

<style scoped>
.contact-page { padding-top: 72px; background: #f8fafc; }

/* Hero */
.contact-hero {
  position: relative; overflow: hidden;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a2a4a 100%);
  padding: 5rem 1.5rem 4rem; text-align: center;
}
.orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.2; }
.orb-1 { width: 400px; height: 400px; background: #6366f1; top: -100px; right: -80px; animation: float 9s ease-in-out infinite; }
.orb-2 { width: 300px; height: 300px; background: #10b981; bottom: -80px; left: -60px; animation: float 7s ease-in-out infinite reverse; }
.hero-content { position: relative; z-index: 1; }

.section-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.35rem 1rem; background: rgba(16,185,129,0.15);
  border: 1px solid rgba(16,185,129,0.3); border-radius: 9999px;
  color: #34d399; font-size: 0.8rem; font-weight: 600;
  letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 1.25rem;
}
.contact-hero h1 { color: #f8fafc; font-size: clamp(1.8rem, 5vw, 3rem); margin-bottom: 1rem; }
.contact-hero p { color: rgba(248,250,252,0.7); font-size: 1.05rem; max-width: 520px; margin: 0 auto; line-height: 1.7; }
.grad-text { background: linear-gradient(135deg, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

/* Body */
.contact-body { padding: 4rem 1.5rem; }
.section-wrap { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem; }
.contact-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
}
@media (min-width: 900px) { .contact-grid { grid-template-columns: 1.3fr 1fr; } }

/* Form */
.contact-form-wrap { background: #fff; border-radius: 20px; padding: 2.5rem; box-shadow: 0 4px 24px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; }
.contact-form-wrap h2 { color: #0f172a; margin-bottom: 1.75rem; font-size: 1.5rem; }

.field-wrap { margin-bottom: 1.25rem; }
.field-wrap label { display: block; font-weight: 600; font-size: 0.9rem; color: #374151; margin-bottom: 0.5rem; }
.input-row { display: flex; align-items: center; border: 1.5px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #f8fafc; transition: all 0.3s ease; }
.input-row:focus-within { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.12); }
.input-row span { padding: 0 0.85rem; font-size: 1rem; background: transparent; }
.input-row input, .input-row textarea {
  flex: 1; padding: 0.85rem 0.85rem 0.85rem 0;
  border: none; background: transparent; outline: none;
  font-size: 0.95rem; font-family: 'Inter', sans-serif; color: #0f172a;
  resize: none;
}
.input-row input::placeholder, .input-row textarea::placeholder { color: #94a3b8; }
.textarea-row { align-items: flex-start; }
.textarea-row span { padding-top: 0.9rem; }

.submit-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  width: 100%; padding: 1rem;
  background: linear-gradient(135deg, #10b981, #059669); color: #fff;
  border: none; border-radius: 12px; font-size: 1rem; font-weight: 700;
  font-family: 'Inter', sans-serif; cursor: pointer; min-height: 52px;
  transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(16,185,129,0.3);
}
.submit-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(16,185,129,0.4); }
.submit-btn:disabled { opacity: 0.75; cursor: not-allowed; }

.spin-ring { width: 20px; height: 20px; border: 2.5px solid rgba(255,255,255,0.35); border-top-color: #fff; border-radius: 50%; animation: spin 0.7s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Success */
.success-fade-enter-active, .success-fade-leave-active { transition: all 0.4s ease; }
.success-fade-enter-from { opacity: 0; transform: scale(0.9); }
.success-fade-leave-to { opacity: 0; transform: scale(1.05); }

.success-state { text-align: center; padding: 2.5rem 1.5rem; }
.success-icon { font-size: 4rem; margin-bottom: 1rem; animation: bounce 1s ease; }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
.success-state h3 { color: #0f172a; font-size: 1.5rem; margin-bottom: 0.5rem; }
.success-state p { color: #64748b; margin-bottom: 1.5rem; line-height: 1.6; }
.send-again {
  padding: 0.65rem 1.5rem; border: 1.5px solid #10b981; background: transparent;
  color: #10b981; border-radius: 9999px; font-size: 0.9rem; font-weight: 600;
  cursor: pointer; font-family: 'Inter', sans-serif; transition: all 0.3s ease;
}
.send-again:hover { background: #10b981; color: #fff; }

/* Info side */
.info-side { display: flex; flex-direction: column; gap: 1.25rem; }

.info-card {
  display: flex; align-items: flex-start; gap: 1rem;
  background: #fff; padding: 1.25rem 1.5rem;
  border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0; transition: all 0.3s ease;
}
.info-card:hover { transform: translateY(-3px); box-shadow: 0 10px 28px rgba(0,0,0,0.08); border-color: rgba(16,185,129,0.2); }
.info-icon { font-size: 1.75rem; flex-shrink: 0; }
.info-card h4 { color: #0f172a; font-size: 0.9rem; margin-bottom: 0.25rem; }
.info-card p { color: #64748b; font-size: 0.9rem; margin: 0; }

.map-placeholder { border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }

.social-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.social-chip {
  padding: 0.5rem 1rem; border-radius: 9999px;
  background: #fff; border: 1.5px solid #e2e8f0;
  color: #374151; text-decoration: none; font-size: 0.85rem; font-weight: 500;
  transition: all 0.3s ease;
}
.social-chip:hover { border-color: #10b981; color: #10b981; background: rgba(16,185,129,0.06); }

@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-18px); } }

@media (max-width: 768px) {
  .contact-hero { padding: 4rem 1rem 3rem; }
  .contact-hero h1 { font-size: 2.25rem; }
  .contact-body { padding: 3rem 1rem; }
  .contact-form-wrap { padding: 1.5rem; }
  .info-side { margin-top: 1rem; }
}
</style>