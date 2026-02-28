<template>
  <div class="home-page">
    <!-- ═══ HERO SECTION ═══════════════════════════════════════ -->
    <section class="hero" id="home">
      <!-- Animated gradient orbs -->
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>

      <!-- Floating food emojis -->
      <div class="floating-emojis" aria-hidden="true">
        <span v-for="(emoji, i) in floatingEmojis" :key="i" class="float-emoji"
          :style="{ left: emoji.x + '%', animationDelay: emoji.delay + 's', animationDuration: emoji.dur + 's', fontSize: emoji.size + 'rem' }">
          {{ emoji.char }}
        </span>
      </div>

      <!-- Slideshow overlay -->
      <div class="hero-bg-slide"
        :style="{ backgroundImage: `url('${backgroundImages[currentImageIndex]}')` }"
      ></div>

      <div class="hero-content">
        <div class="hero-badge animate-fade-up">
          🌱 Fighting Food Waste in India
        </div>
        <h1 class="hero-title animate-fade-up delay-200">
          <span class="line">Reduce Waste,</span>
          <span class="line gradient-text">Share Abundance</span>
        </h1>
        <p class="hero-subtitle animate-fade-up delay-400">
          Connect with your community to share surplus food and fight hunger.<br />
          Your small contribution can make a <strong>big difference</strong>.
        </p>
        <div class="hero-actions animate-fade-up delay-500">
          <RouterLink to="/register" class="btn-primary">
            🚀 Join Our Mission
          </RouterLink>
          <a href="#about" @click.prevent="scrollTo('about')" class="btn-outline-white">
            Learn More ↓
          </a>
        </div>

        <!-- Scroll indicator -->
        <div class="scroll-indicator animate-fade-up delay-700">
          <div class="scroll-dot"></div>
        </div>
      </div>
    </section>

    <!-- ═══ STATS SECTION ══════════════════════════════════════ -->
    <section class="stats-section">
      <div class="section-wrap">
        <div class="stats-grid">
          <div v-for="(stat, i) in stats" :key="i" class="stat-card" :style="{ animationDelay: (i * 0.15) + 's' }">
            <div class="stat-icon">{{ stat.icon }}</div>
            <div class="stat-number">
              <AnimatedCounter :target="stat.value" :suffix="stat.suffix" :duration="2500" />
            </div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ HOW IT WORKS ═══════════════════════════════════════ -->
    <section class="how-section" id="about">
      <div class="section-wrap">
        <div class="section-header">
          <span class="section-badge">How It Works</span>
          <h2>Simple Steps to <span class="gradient-text">Make a Difference</span></h2>
          <p>Whether you have extra food to share or need a meal, we make the process seamless.</p>
        </div>

        <div class="steps-grid">
          <div v-for="(step, i) in steps" :key="i" class="step-card">
            <div class="step-number">{{ String(i + 1).padStart(2, '0') }}</div>
            <div class="step-icon">{{ step.icon }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
            <div class="step-connector" v-if="i < steps.length - 1">→</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ FEATURES ═══════════════════════════════════════════ -->
    <section class="features-section">
      <div class="section-wrap">
        <div class="section-header">
          <span class="section-badge">Why WasteFood?</span>
          <h2>Built for <span class="gradient-text">Real Impact</span></h2>
        </div>
        <div class="features-grid">
          <div v-for="(feat, i) in features" :key="i" class="feature-card">
            <div class="feature-icon-wrap">{{ feat.icon }}</div>
            <h3>{{ feat.title }}</h3>
            <p>{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ ABOUT MISSION ══════════════════════════════════════ -->
    <section class="mission-section">
      <div class="section-wrap">
        <div class="mission-inner">
          <div class="mission-text">
            <span class="section-badge">Our Mission</span>
            <h2>Who <span class="gradient-text">We Are</span></h2>
            <p>Founded in Bengaluru, WasteFood is a non-profit initiative leveraging technology to create a network of food donors and recipients.</p>
            <p>We believe that perfectly good food should feed people, not landfills. Our platform makes it easy for individuals, restaurants, and event organizers to donate surplus food safely and efficiently.</p>
            <RouterLink to="/register" class="btn-primary" style="margin-top:1.5rem; display:inline-flex;">
              Start Donating →
            </RouterLink>
          </div>
          <div class="mission-visual">
            <div class="mission-img-wrap">
              <img src="https://images.unsplash.com/photo-1593113598332-cd288d649433?w=600&q=80" alt="Community food sharing" />
              <div class="mission-badge-card">
                <span>🍽️</span>
                <div>
                  <strong>10,000+</strong>
                  <small>Meals Shared</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ CTA BANNER ═════════════════════════════════════════ -->
    <section class="cta-section" id="contact">
      <div class="section-wrap">
        <div class="cta-inner">
          <h2>Ready to Make a Difference?</h2>
          <p>Join thousands of donors and recipients across Bengaluru today.</p>
          <div class="cta-actions">
            <RouterLink to="/register" class="btn-primary">Sign Up Free</RouterLink>
            <div class="cta-contact">
              <p>📧 contact@wastefood.com</p>
              <p>📍 123 Tech Park, Bengaluru, Karnataka</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterLink } from 'vue-router';
import AnimatedCounter from '../components/AnimatedCounter.vue';

// Background slideshow
const backgroundImages = [
  'https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=1600&q=80',
  'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=1600&q=80',
  'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=1600&q=80',
];
const currentImageIndex = ref(0);
let slideInterval = null;

// Floating emojis data
const floatingEmojis = ref([
  { char: '🥗', x: 8, delay: 0, dur: 7, size: 2 },
  { char: '🍱', x: 20, delay: 1.5, dur: 9, size: 1.5 },
  { char: '🫶', x: 75, delay: 0.5, dur: 8, size: 1.8 },
  { char: '🥘', x: 88, delay: 2, dur: 6, size: 1.6 },
  { char: '🌽', x: 50, delay: 3, dur: 10, size: 1.4 },
  { char: '🍛', x: 35, delay: 4, dur: 7.5, size: 1.7 },
]);

const stats = [
  { icon: '🍽️', value: 10000, suffix: '+', label: 'Meals Shared' },
  { icon: '🤝', value: 500, suffix: '+', label: 'Active Donors' },
  { icon: '🌆', value: 50, suffix: '+', label: 'Communities' },
  { icon: '♻️', value: 2500, suffix: 'kg', label: 'Food Saved' },
];

const steps = [
  { icon: '📝', title: 'Register', desc: 'Create a free account in under 2 minutes. No credit card required.' },
  { icon: '🍱', title: 'List or Browse', desc: 'Post your surplus food or find available donations near you.' },
  { icon: '🤝', title: 'Connect', desc: 'Request food or approve requests from people in your community.' },
  { icon: '❤️', title: 'Impact', desc: 'Coordinate pickup and make a real difference together.' },
];

const features = [
  { icon: '🔒', title: 'Secure Auth', desc: 'Powered by Supabase with JWT authentication keeping your data safe.' },
  { icon: '⚡', title: 'Real-time Updates', desc: 'Instant notifications when someone requests your listed food.' },
  { icon: '📍', title: 'Location-Based', desc: 'Find food available near your specific pickup location.' },
  { icon: '📊', title: 'Track Donations', desc: 'Full dashboard to manage your donations and incoming requests.' },
  { icon: '✅', title: 'Approval Control', desc: 'Donors stay in control — you approve who receives your food.' },
  { icon: '🌱', title: 'Eco Impact', desc: 'Track how much CO₂ and waste you have helped prevent.' },
];

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
};

onMounted(() => {
  slideInterval = setInterval(() => {
    currentImageIndex.value = (currentImageIndex.value + 1) % backgroundImages.length;
  }, 4000);
});
onUnmounted(() => clearInterval(slideInterval));
</script>

<style scoped>
/* ─── Global ─── */
.home-page { background: #f8fafc; }

/* ─── Hero ─── */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  background: #0a0f1e;
}

/* Background slideshow */
.hero-bg-slide {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0.18;
  transition: background-image 1s ease;
}

/* Dark overlay */
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(16,185,129,0.15) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 30%, rgba(99,102,241,0.1) 0%, transparent 50%),
              linear-gradient(135deg, #0a0f1e 0%, #0f2027 50%, #1a3a2a 100%);
  z-index: 0;
}

/* Animated gradient orbs */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
  animation: float 8s ease-in-out infinite;
  z-index: 0;
}
.orb-1 { width: 500px; height: 500px; background: rgba(16,185,129,0.4); top: -100px; left: -100px; animation-delay: 0s; }
.orb-2 { width: 350px; height: 350px; background: rgba(99,102,241,0.3); bottom: -50px; right: -50px; animation-delay: 3s; }
.orb-3 { width: 250px; height: 250px; background: rgba(245,158,11,0.25); top: 50%; left: 60%; animation-delay: 5s; }

/* Floating emojis */
.floating-emojis { position: absolute; inset: 0; pointer-events: none; z-index: 1; }
.float-emoji {
  position: absolute;
  bottom: -50px;
  animation: floatUp linear infinite;
  opacity: 0.5;
}
@keyframes floatUp {
  0%   { bottom: -50px; opacity: 0; transform: translateX(0) rotate(0deg); }
  10%  { opacity: 0.5; }
  90%  { opacity: 0.3; }
  100% { bottom: 110vh; opacity: 0; transform: translateX(30px) rotate(20deg); }
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 860px;
  padding: 8rem 1.5rem 5rem;
}

.hero-badge {
  display: inline-block;
  padding: 0.45rem 1.2rem;
  background: rgba(16,185,129,0.15);
  border: 1px solid rgba(16,185,129,0.35);
  border-radius: 9999px;
  color: #34d399;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  margin-bottom: 1.5rem;
  animation: fadeInUp 0.6s ease forwards;
}

.hero-title {
  font-size: clamp(2.5rem, 7vw, 5rem);
  font-weight: 900;
  color: #f8fafc;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}
.hero-title .line { display: block; }
.hero-title .gradient-text {
  background: linear-gradient(135deg, #10b981, #34d399, #6ee7b7);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease infinite;
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.hero-subtitle {
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  color: rgba(248,250,252,0.75);
  line-height: 1.7;
  margin-bottom: 2.5rem;
}
.hero-subtitle strong { color: #34d399; }

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2.25rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  font-weight: 700;
  font-size: 1rem;
  border-radius: 9999px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 8px 30px rgba(16,185,129,0.35);
  border: none;
  cursor: pointer;
}
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(16,185,129,0.5); }

.btn-outline-white {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2.25rem;
  background: transparent;
  color: rgba(248,250,252,0.9);
  font-weight: 600;
  font-size: 1rem;
  border-radius: 9999px;
  text-decoration: none;
  border: 1.5px solid rgba(255,255,255,0.3);
  transition: all 0.3s ease;
  cursor: pointer;
}
.btn-outline-white:hover { border-color: rgba(255,255,255,0.7); background: rgba(255,255,255,0.08); transform: translateY(-3px); }

/* Scroll indicator */
.scroll-indicator {
  display: flex;
  justify-content: center;
}
.scroll-dot {
  width: 22px;
  height: 36px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 12px;
  position: relative;
}
.scroll-dot::before {
  content: '';
  position: absolute;
  top: 5px;
  left: 50%;
  width: 4px;
  height: 8px;
  background: #10b981;
  border-radius: 2px;
  transform: translateX(-50%);
  animation: scrollBounce 1.8s ease-in-out infinite;
}
@keyframes scrollBounce {
  0%, 100% { top: 5px; opacity: 1; }
  50% { top: 16px; opacity: 0.3; }
}

/* ─── Stats ─── */
.stats-section {
  padding: 4rem 1.5rem;
  background: #fff;
  position: relative;
  z-index: 1;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
}
.stat-card {
  text-align: center;
  padding: 2rem 1.5rem;
  border-radius: 16px;
  background: linear-gradient(145deg, #f0fdf4, #ecfdf5);
  border: 1px solid rgba(16,185,129,0.15);
  transition: all 0.35s ease;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
}
.stat-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(16,185,129,0.15); }
.stat-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.stat-number {
  font-size: 2.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #10b981, #059669);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.5rem;
}
.stat-label { color: #64748b; font-weight: 500; font-size: 0.9rem; }

/* ─── How It Works ─── */
.how-section {
  padding: 6rem 1.5rem;
  background: #f8fafc;
}
.section-header {
  text-align: center;
  margin-bottom: 3.5rem;
}
.section-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: rgba(16,185,129,0.1);
  color: #10b981;
  border: 1px solid rgba(16,185,129,0.25);
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 1rem;
}
.section-header h2 {
  font-size: clamp(1.8rem, 4vw, 2.75rem);
  color: #0f172a;
  margin-bottom: 0.75rem;
}
.section-header p { color: #64748b; font-size: 1.05rem; max-width: 520px; margin: 0 auto; }
.gradient-text {
  background: linear-gradient(135deg, #10b981, #059669);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  position: relative;
}
.step-card {
  text-align: center;
  padding: 2.5rem 1.5rem;
  background: #fff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  position: relative;
  transition: all 0.3s ease;
}
.step-card:hover { transform: translateY(-8px); box-shadow: 0 20px 48px rgba(0,0,0,0.1); border-color: rgba(16,185,129,0.3); }
.step-number {
  position: absolute;
  top: -14px;
  right: 20px;
  font-size: 3rem;
  font-weight: 900;
  color: rgba(16,185,129,0.12);
  line-height: 1;
}
.step-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.step-card h3 { font-size: 1.2rem; color: #0f172a; margin-bottom: 0.75rem; }
.step-card p { color: #64748b; font-size: 0.9rem; line-height: 1.6; }
.step-connector {
  position: absolute;
  right: -24px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.5rem;
  color: rgba(16,185,129,0.4);
  z-index: 1;
  display: none;
}

/* ─── Features ─── */
.features-section {
  padding: 6rem 1.5rem;
  background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 100%);
}
.features-section .section-header h2 { color: #f8fafc; }
.features-section .section-header p { color: rgba(248,250,252,0.6); }

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
.feature-card {
  padding: 2rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  transition: all 0.35s ease;
}
.feature-card:hover {
  background: rgba(16,185,129,0.08);
  border-color: rgba(16,185,129,0.3);
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.feature-icon-wrap { font-size: 2rem; margin-bottom: 1rem; }
.feature-card h3 { color: #f8fafc; font-size: 1.1rem; margin-bottom: 0.5rem; }
.feature-card p { color: rgba(248,250,252,0.6); font-size: 0.9rem; line-height: 1.6; }

/* ─── Mission ─── */
.mission-section { padding: 6rem 1.5rem; background: #fff; }
.mission-inner {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
  align-items: center;
}
.mission-text h2 { font-size: clamp(1.8rem, 3.5vw, 2.5rem); color: #0f172a; margin-bottom: 1.25rem; }
.mission-text p { color: #475569; line-height: 1.8; font-size: 1.05rem; margin-bottom: 1rem; }

.mission-img-wrap {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
}
.mission-img-wrap img { width: 100%; height: 380px; object-fit: cover; border-radius: 20px; }
.mission-badge-card {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.mission-badge-card div { display: flex; flex-direction: column; }
.mission-badge-card strong { font-size: 1.1rem; color: #0f172a; line-height: 1; }
.mission-badge-card small { color: #64748b; font-size: 0.8rem; }

/* ─── CTA Banner ─── */
.cta-section {
  background: linear-gradient(135deg, #10b981 0%, #059669 50%, #0d9488 100%);
  padding: 5rem 1.5rem;
}
.cta-inner { text-align: center; max-width: 700px; margin: 0 auto; }
.cta-inner h2 { font-size: clamp(1.8rem, 4vw, 2.75rem); color: #fff; margin-bottom: 0.75rem; }
.cta-inner > p { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-bottom: 2rem; }
.cta-actions { display: flex; flex-direction: column; align-items: center; gap: 1.5rem; }
.cta-actions .btn-primary {
  background: #fff;
  color: #059669;
  box-shadow: 0 8px 30px rgba(0,0,0,0.2);
  font-size: 1.05rem;
  padding: 1rem 2.5rem;
}
.cta-actions .btn-primary:hover { box-shadow: 0 16px 40px rgba(0,0,0,0.3); }
.cta-contact p { color: rgba(255,255,255,0.85); margin: 0.25rem 0; }

/* ─── Responsive ─── */
@media (min-width: 768px) {
  .mission-inner { grid-template-columns: 1fr 1fr; }
  .step-connector { display: block; }
  .cta-actions { flex-direction: row; justify-content: center; }
}

/* ─── Fade up animation ─── */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-up { opacity: 0; animation: fadeInUp 0.7s ease forwards; }
.delay-200 { animation-delay: 0.2s; }
.delay-400 { animation-delay: 0.4s; }
.delay-500 { animation-delay: 0.5s; }
.delay-700 { animation-delay: 0.7s; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@media (max-width: 768px) {
  .hero-content { padding: 6rem 1rem 3rem; }
  .hero-title { font-size: clamp(2rem, 10vw, 2.5rem); }
  .hero-subtitle { font-size: 1rem; margin-bottom: 2rem; }
  .hero-actions { margin-top: 1rem; }
  .stats-section { padding: 3rem 1rem; }
  .stats-grid { gap: 1rem; }
  .how-section { padding: 4rem 1rem; }
  .features-section { padding: 4rem 1rem; }
  .mission-section { padding: 4rem 1rem; }
  .mission-img-wrap img { height: 280px; }
  .mission-badge-card { font-size: 1.25rem; padding: 0.5rem 1rem; bottom: 10px; left: 10px; }
  .cta-section { padding: 3.5rem 1rem; }
}
</style>