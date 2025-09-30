<template>
  <div class="home-page">
    <section id="home" class="hero-section" :style="heroStyle">
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { RouterLink } from 'vue-router';

// --- START: New code for slideshow ---

// 1. Define your list of images
// Replace these placeholders with your actual image URLs
const backgroundImages = ref([
  'https://images7.alphacoders.com/110/1103153.jpg',
  'https://images.squarespace-cdn.com/content/v1/669a8576009c437dabc4d36c/e1d15f4f-7a66-416b-8c83-68174a947d14/scraping-food-into-bin.jpeg',
  'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiKfcDfTZJVfY2vZ7hdh0E9Uu07e4GxuDLkyXEmzgKNpIxuh84OhR47DHGETCh0jKOIIzWUCMZy3V3q8-UxwZZZ4iLixTHyiyJAYeypznXB7AX21EUEY-sQtpTvns1TpxwkQq1gzy3BWUfL/s0/stop-food-waste-day-rich-poor-hungry.jpg'
]);

const currentImageIndex = ref(0);
let intervalId = null;

// 2. Create a computed property for the dynamic style
const heroStyle = computed(() => ({
  backgroundImage: `
    linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
    url('${backgroundImages.value[currentImageIndex.value]}')
  `
}));

// 3. Use lifecycle hooks to start and stop the slideshow
onMounted(() => {
  // Start the slideshow every 2 seconds (2000 milliseconds)
  intervalId = setInterval(() => {
    currentImageIndex.value = (currentImageIndex.value + 1) % backgroundImages.value.length;
  }, 2000);
});

onUnmounted(() => {
  // Important: Clear the interval when the component is no longer on the page
  clearInterval(intervalId);
});

// --- END: New code for slideshow ---

</script>

<style scoped>
.hero-section {
  text-align: center; padding: 4rem 1rem;
  /* The 'background' property is now handled by the :style binding in the template.
    We add a transition for a smooth fade effect between images.
  */
  transition: background-image 2s ease-in-out;
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