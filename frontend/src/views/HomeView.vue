<template>
  <div class="home-page">
    <section id="home" class="hero-section">
      <div class="hero-content">
        <h1>Reduce Waste, Share Abundance</h1>
        <p>Connect with your community to share surplus food and fight hunger. Your small contribution can make a big difference.</p>
        <RouterLink to="/register" class="cta-button">Join Our Mission</RouterLink>
      </div>
    </section>

    <section id="about" class="content-section">
      <div class="section-container">
        <h2>About Our Mission</h2>
        <div class="flex-content">
          <div class="text-content">
            <h3>Who We Are</h3>
            <p>Founded in Bengaluru, WasteFood is a non-profit initiative leveraging technology to create a network of food donors and recipients. We believe that perfectly good food should feed people, not landfills.</p>
            <p>Our platform makes it easy for individuals, restaurants, and event organizers to donate surplus food safely and efficiently.</p>
          </div>
          <img src="https://placehold.co/600x400/EFEFEF/333?text=Community" alt="Community gathering" />
        </div>
      </div>
    </section>

    <section id="contact" class="content-section-dark">
       <div class="section-container">
        <h2>Get In Touch</h2>
        <p>Have questions or want to partner with us? We’d love to hear from you.</p>
        <div class="contact-info">
          <p><strong>Email:</strong> contact@wastefood.com</p>
          <p><strong>Address:</strong> 123 Tech Park, Bengaluru, Karnataka, India</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.hero-section {
  text-align: center; padding: 4rem 1rem;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://placehold.co/1920x1080/444/FFF?text=Food+Donation');
  background-size: cover; background-position: center; color: white;
}
.hero-content h1 { font-size: 2.5rem; margin-bottom: 1rem; }
.cta-button {
  display: inline-block; padding: 14px 28px; background-color: #42b983;
  color: white; text-decoration: none; border-radius: 5px; font-weight: bold;
  margin-top: 1.5rem; transition: background-color 0.3s;
}
.cta-button:hover { background-color: #36a473; }
.content-section { padding: 3rem 1rem; }
.content-section-dark { background-color: #f9f9f9; padding: 3rem 1rem; border-top: 1px solid #eee; border-bottom: 1px solid #eee;}
.section-container { max-width: 1100px; margin: 0 auto; }
.section-container h2 { text-align: center; font-size: 2rem; margin-bottom: 2rem; }
.flex-content { display: flex; gap: 2rem; align-items: center; flex-direction: column; } /* Default to column for mobile */
.flex-content img { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
.contact-info { text-align: center; margin-top: 1rem; font-size: 1.1rem; }

/* --- DESKTOP STYLES --- */
@media (min-width: 769px) {
  .hero-section { padding: 6rem 2rem; }
  .hero-content h1 { font-size: 3.5rem; }
  .content-section, .content-section-dark { padding: 4rem 2rem; }
  .section-container h2 { font-size: 2.5rem; }
  .flex-content { flex-direction: row; } /* Side-by-side on desktop */
  .flex-content img { max-width: 50%; }
}
</style>