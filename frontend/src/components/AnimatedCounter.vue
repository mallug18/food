<template>
  <span class="animated-counter">{{ displayValue.toLocaleString() }}{{ suffix }}</span>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  target: { type: Number, default: 0 },
  duration: { type: Number, default: 2000 },
  suffix: { type: String, default: '' },
});

const displayValue = ref(0);
let observer = null;
let rafId = null;
let containerEl = null;

function animateCount(el) {
  const start = performance.now();
  const startVal = 0;
  const endVal = props.target;

  const step = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / props.duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    displayValue.value = Math.round(startVal + (endVal - startVal) * eased);
    if (progress < 1) {
      rafId = requestAnimationFrame(step);
    }
  };
  rafId = requestAnimationFrame(step);
}

onMounted(() => {
  // Find the parent element for IntersectionObserver
  const el = document.querySelector('.counter-trigger') || document.body;
  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        animateCount();
        observer.disconnect();
      }
    },
    { threshold: 0.5 }
  );
  // Observe the component's own root element
  const root = document.querySelector('.animated-counter');
  if (root) observer.observe(root.parentElement || root);
});

onUnmounted(() => {
  if (observer) observer.disconnect();
  if (rafId) cancelAnimationFrame(rafId);
});
</script>

<style scoped>
.animated-counter {
  font-variant-numeric: tabular-nums;
}
</style>
