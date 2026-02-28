<template>
  <footer class="site-footer">
    <!-- Wave SVG -->
    <div class="footer-wave">
      <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
        <path d="M0,40 C240,80 480,0 720,40 C960,80 1200,0 1440,40 L1440,80 L0,80 Z" fill="#0a0f1e"/>
      </svg>
    </div>

    <div class="footer-inner">
      <div class="footer-grid">
        <!-- Brand -->
        <div class="footer-brand">
          <div class="footer-logo"><img src="/favicon.png" alt="Logo" style="width: 24px; height: 24px; margin-right: 8px; vertical-align: middle;" />Waste<span>Food</span></div>
          <p>Connecting communities, reducing waste, fighting hunger — one meal at a time.</p>
          <div class="social-links">
            <a href="#" aria-label="Twitter" class="social-btn">𝕏</a>
            <a href="#" aria-label="Instagram" class="social-btn">📸</a>
            <a href="#" aria-label="LinkedIn" class="social-btn">💼</a>
          </div>
        </div>

        <!-- Links -->
        <div class="footer-col">
          <h4>Platform</h4>
          <ul>
            <li><RouterLink to="/">Home</RouterLink></li>
            <li><RouterLink to="/login">Login</RouterLink></li>
            <li><RouterLink to="/register">Register</RouterLink></li>
            <li><RouterLink to="/dashboard">Dashboard</RouterLink></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Learn More</h4>
          <ul>
            <li><a href="/#about">About Us</a></li>
            <li><a href="/#contact">Contact</a></li>
            <li><a href="#">Privacy Policy</a></li>
          </ul>
        </div>

        <!-- Stats -->
        <div class="footer-col footer-impact">
          <h4>Our Impact</h4>
          <div class="impact-stat">
            <span class="impact-num">10K+</span>
            <span>Meals Shared</span>
          </div>
          <div class="impact-stat">
            <span class="impact-num">500+</span>
            <span>Active Donors</span>
          </div>
          <div class="impact-stat">
            <span class="impact-num">50+</span>
            <span>Communities</span>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© 2025 WasteFood Initiative. Built with ❤️ to fight hunger in India.</p>
        <p class="footer-tagline">Every meal shared is a life impacted.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.site-footer {
  position: relative;
  background: #0a0f1e;
  color: rgba(248, 250, 252, 0.7);
  margin-top: auto;
}

.footer-wave {
  position: relative;
  height: 80px;
  overflow: hidden;
  background: #f8fafc; /* matches background before footer */
}
.footer-wave svg {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100%;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 1.5rem 2rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 2.5rem;
  padding-bottom: 2.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}

.footer-brand .footer-logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: #f8fafc;
  margin-bottom: 0.75rem;
}
.footer-brand .footer-logo span {
  background: linear-gradient(135deg, #10b981, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.footer-brand p {
  font-size: 0.9rem;
  line-height: 1.7;
  margin-bottom: 1.25rem;
  max-width: 260px;
}

.social-links { display: flex; gap: 0.75rem; }
.social-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  text-decoration: none;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
}
.social-btn:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.4);
  transform: translateY(-3px);
}

.footer-col h4 {
  color: #f8fafc;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 1rem;
}
.footer-col ul { list-style: none; }
.footer-col ul li { margin-bottom: 0.6rem; }
.footer-col ul li a {
  color: rgba(248, 250, 252, 0.55);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}
.footer-col ul li a:hover {
  color: #10b981;
  transform: translateX(4px);
}

.footer-impact .impact-stat {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}
.impact-num {
  font-size: 1.3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #10b981, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  min-width: 55px;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding-top: 1.5rem;
  font-size: 0.85rem;
}
.footer-tagline {
  color: rgba(16, 185, 129, 0.7);
  font-style: italic;
}

@media (max-width: 900px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .footer-brand { grid-column: 1 / -1; }
}
@media (max-width: 600px) {
  .footer-grid { grid-template-columns: 1fr; }
  .footer-bottom { flex-direction: column; text-align: center; }
}
</style>