<template>
  <div class="about-page">
    <!-- Hero -->
    <section class="about-hero">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="about-hero-content section-wrap">
        <span class="section-badge">🌿 Our Story</span>
        <h1>Fighting <span class="grad-text">Food Waste</span>,<br/>One Meal at a Time</h1>
        <p>WasteFood is a Bengaluru-born non-profit leveraging technology to bridge the gap between surplus food and hunger.</p>
      </div>
    </section>

    <!-- Mission Cards -->
    <section class="mission-section">
      <div class="section-wrap">
        <div class="section-head">
          <span class="section-badge">What We Believe</span>
          <h2>Our <span class="grad-text">Core Values</span></h2>
        </div>
        <div class="values-grid">
          <div v-for="(v, i) in values" :key="i" class="value-card" :style="{ animationDelay: (i*0.1)+'s' }">
            <div class="value-icon">{{ v.icon }}</div>
            <h3>{{ v.title }}</h3>
            <p>{{ v.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="impact-section">
      <div class="section-wrap">
        <div class="section-head">
          <span class="section-badge light">📊 Our Impact</span>
          <h2 style="color:#f8fafc;">Numbers That <span class="grad-text">Matter</span></h2>
        </div>
        <div class="impact-grid">
          <div v-for="(s, i) in impacts" :key="i" class="impact-card">
            <span class="impact-icon">{{ s.icon }}</span>
            <strong class="impact-num">{{ s.value }}</strong>
            <span>{{ s.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Timeline -->
    <section class="timeline-section">
      <div class="section-wrap">
        <div class="section-head">
          <span class="section-badge">🏁 Our Journey</span>
          <h2>Milestones <span class="grad-text">So Far</span></h2>
        </div>
        <div class="journey-timeline">
          <div v-for="(m, i) in milestones" :key="i" class="milestone" :class="{ right: i % 2 !== 0 }" :style="{ animationDelay: (i*0.15)+'s' }">
            <div class="milestone-dot">{{ m.year }}</div>
            <div class="milestone-card">
              <h4>{{ m.title }}</h4>
              <p>{{ m.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="about-cta">
      <div class="section-wrap">
        <h2>Ready to Be Part of the Story?</h2>
        <p>Join thousands who are already making a difference.</p>
        <RouterLink to="/register" class="cta-btn">Get Started Free →</RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';

const values = [
  { icon: '🤝', title: 'Community First', desc: 'We believe local communities hold the power to eliminate hunger one meal at a time.' },
  { icon: '🌱', title: 'Sustainability', desc: 'Every kilogram of food saved reduces our collective carbon footprint and environmental impact.' },
  { icon: '🔒', title: 'Safety & Trust', desc: 'Secure verified connections between donors and recipients with full accountability.' },
  { icon: '⚡', title: 'Simplicity', desc: 'Technology should make helping easier, not harder. Our platform is simple by design.' },
  { icon: '📊', title: 'Transparency', desc: 'We share our impact data openly so our community can see the real difference.' },
  { icon: '🌍', title: 'Scale', desc: 'Starting in Bengaluru, we plan to expand across every city in India.' },
];

const impacts = [
  { icon: '🍽️', value: '10,000+', label: 'Meals Shared' },
  { icon: '👥', value: '500+', label: 'Active Donors' },
  { icon: '🌆', value: '50+', label: 'Communities' },
  { icon: '♻️', value: '2,500kg', label: 'Food Saved' },
];

const milestones = [
  { year: '2023', title: 'WasteFood Founded', desc: 'Started as a student project in Bengaluru to tackle food waste during college events.' },
  { year: '2024', title: 'First 100 Donations', desc: 'Reached our first 100 successful food donations within 3 months of launch.' },
  { year: '2024', title: 'Backend Launch', desc: 'Launched our secure Flask + Supabase backend enabling real-time tracking.' },
  { year: '2025', title: '10,000 Meals', desc: 'Crossed the milestone of 10,000 meals shared across Karnataka.' },
];
</script>

<style scoped>
.about-page { padding-top: 72px; background: #f8fafc; }

/* Hero */
.about-hero {
  position: relative; overflow: hidden;
  background: linear-gradient(135deg, #0a0f1e 0%, #0f2027 50%, #1a3a2a 100%);
  padding: 5rem 1.5rem 4rem;
  text-align: center;
}
.orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.2; }
.orb-1 { width: 500px; height: 500px; background: #10b981; top: -150px; left: -150px; animation: float 10s ease-in-out infinite; }
.orb-2 { width: 350px; height: 350px; background: #6366f1; bottom: -100px; right: -80px; animation: float 8s ease-in-out infinite reverse; }

.about-hero-content { position: relative; z-index: 1; }
.section-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.35rem 1rem; background: rgba(16,185,129,0.15);
  border: 1px solid rgba(16,185,129,0.3); border-radius: 9999px;
  color: #34d399; font-size: 0.8rem; font-weight: 600;
  letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 1.25rem;
}
.section-badge.light { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2); color: rgba(248,250,252,0.8); }
.about-hero h1 { color: #f8fafc; font-size: clamp(2rem, 5vw, 3.5rem); margin-bottom: 1rem; line-height: 1.15; }
.about-hero p { color: rgba(248,250,252,0.7); font-size: 1.1rem; max-width: 580px; margin: 0 auto; line-height: 1.7; }

.grad-text {
  background: linear-gradient(135deg, #10b981, #34d399);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.section-wrap { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem; }
.section-head { text-align: center; margin-bottom: 3rem; }
.section-head h2 { font-size: clamp(1.6rem, 3.5vw, 2.5rem); color: #0f172a; }

/* Values */
.mission-section { padding: 5rem 1.5rem; }
.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}
.value-card {
  background: #fff; border-radius: 16px; padding: 2rem;
  border: 1px solid #e8e8ea;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  transition: all 0.3s ease;
  animation: fadeUp 0.6s ease both;
}
.value-card:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(0,0,0,0.1); border-color: rgba(16,185,129,0.3); }
.value-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.value-card h3 { color: #0f172a; font-size: 1.1rem; margin-bottom: 0.5rem; }
.value-card p { color: #64748b; font-size: 0.9rem; line-height: 1.6; }

/* Impact */
.impact-section {
  padding: 5rem 1.5rem;
  background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 100%);
}
.impact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
}
.impact-card {
  display: flex; flex-direction: column; align-items: center;
  gap: 0.5rem; text-align: center;
  padding: 2rem 1rem;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  transition: all 0.3s ease;
}
.impact-card:hover { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.3); transform: translateY(-4px); }
.impact-icon { font-size: 2rem; }
.impact-num { font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.impact-card span:last-child { color: rgba(248,250,252,0.6); font-size: 0.85rem; }

/* Timeline / Journey */
.timeline-section { padding: 5rem 1.5rem; background: #f8fafc; }
.journey-timeline { display: flex; flex-direction: column; gap: 1.5rem; max-width: 700px; margin: 0 auto; }
.milestone { display: flex; gap: 1.25rem; align-items: flex-start; animation: fadeUp 0.6s ease both; }
.milestone-dot {
  min-width: 64px; height: 40px; background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 9999px; display: flex; align-items: center; justify-content: center;
  color: #fff; font-weight: 800; font-size: 0.85rem; flex-shrink: 0;
  box-shadow: 0 4px 16px rgba(16,185,129,0.3);
}
.milestone-card { background: #fff; border-radius: 14px; padding: 1.25rem 1.5rem; flex: 1; box-shadow: 0 2px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; }
.milestone-card h4 { color: #0f172a; margin-bottom: 0.35rem; }
.milestone-card p { color: #64748b; font-size: 0.9rem; line-height: 1.6; margin: 0; }

/* CTA */
.about-cta {
  padding: 5rem 1.5rem;
  background: linear-gradient(135deg, #10b981, #059669);
  text-align: center;
}
.about-cta h2 { color: #fff; font-size: clamp(1.6rem, 3.5vw, 2.5rem); margin-bottom: 0.75rem; }
.about-cta p { color: rgba(255,255,255,0.85); font-size: 1.05rem; margin-bottom: 2rem; }
.cta-btn {
  display: inline-flex; gap: 0.5rem;
  padding: 1rem 2.5rem; background: #fff; color: #059669;
  border-radius: 9999px; text-decoration: none; font-weight: 700;
  font-size: 1.05rem; transition: all 0.3s ease;
  box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}
.cta-btn:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(0,0,0,0.3); }

@keyframes fadeUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }

@media (max-width: 768px) {
  .about-hero { padding: 4rem 1rem 3rem; }
  .about-hero h1 { font-size: 2.25rem; }
  .mission-section { padding: 3.5rem 1rem; }
  .impact-section { padding: 3.5rem 1rem; }
  .timeline-section { padding: 3.5rem 1rem; }
  .about-cta { padding: 4rem 1rem; }
  .impact-grid { grid-template-columns: 1fr 1fr; }
  .milestone { flex-direction: column; gap: 0.75rem; }
  .milestone-dot { height: 32px; min-width: 56px; font-size: 0.8rem; }
}
</style>