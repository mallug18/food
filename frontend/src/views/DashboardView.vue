<template>
  <div class="dashboard-container">
    <h1>Your Dashboard</h1>
    
    <div class="tabs">
      <button :class="{ active: activeTab === 'share' }" @click="activeTab = 'share'">Share Food</button>
      <button :class="{ active: activeTab === 'receive' }" @click="activeTab = 'receive'">Available Food</button>
    </div>

    <div v-if="activeTab === 'share'" class="tab-content">
      <h2>List a New Food Donation</h2>
      <div class="share-form">
        <input v-model="form.name" type="text" placeholder="Food Name (e.g., Rice and Curry)" />
        <input v-model="form.quantity" type="text" placeholder="Quantity (e.g., Serves 5 people)" />
        <input v-model="form.location" type="text" placeholder="Pickup Location (e.g., Indiranagar, Bengaluru)" />
        <button @click="handleShareFood" :disabled="isSubmitting">
          {{ isSubmitting ? 'Submitting...' : 'Share Food Now' }}
        </button>
        <p v-if="formMessage" :class="{ 'success-message': isSuccess, 'error-message': !isSuccess }">{{ formMessage }}</p>
      </div>
    </div>

    <div v-if="activeTab === 'receive'" class="tab-content">
      <h2>Find Available Food Near You</h2>
      <div v-if="loading" class="loading">Loading available donations...</div>
      <div v-if="!loading && availableFood.length === 0" class="no-food">No food items are currently available. Check back soon!</div>
      <div v-if="apiError" class="error-message">{{ apiError }}</div>
      <div class="food-grid">
        <div v-for="item in availableFood" :key="item.id" class="food-card">
          <h3>{{ item.name }}</h3>
          <p><strong>Quantity:</strong> {{ item.quantity }}</p>
          <p><strong>Location:</strong> {{ item.location }}</p>
          <p class="posted-at">Posted on: {{ new Date(item.created_at).toLocaleDateString() }}</p>
          
          <button 
            @click="handleRequestFood(item)" 
            :disabled="isMyOwnItem(item.donor_id) || item.status === 'requested'"
            class="request-button">
            {{ getButtonText(item) }}
          </button>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '../supabase';

const activeTab = ref('receive'); // Default to showing available food
const isSubmitting = ref(false);
const formMessage = ref('');
const isSuccess = ref(false);
const userSession = ref(null); // To store the logged-in user's session

const form = ref({
  name: '',
  quantity: '',
  location: '',
});

const availableFood = ref([]);
const loading = ref(true);
const apiError = ref('');

// --- DATA FETCHING AND SUBMITTING LOGIC ---

async function fetchAvailableFood() {
  loading.value = true;
  apiError.value = '';
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error("You must be logged in to view food items.");

    const response = await fetch('http://localhost:5000/api/food-items', {
      headers: { 'Authorization': `Bearer ${session.access_token}` },
    });
    if (!response.ok) throw new Error("Failed to fetch food items.");

    availableFood.value = await response.json();
  } catch (error) {
    apiError.value = error.message;
  } finally {
    loading.value = false;
  }
}

async function handleShareFood() {
  isSubmitting.value = true;
  formMessage.value = '';
  isSuccess.value = false;
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error("You must be logged in to share food.");
    
    const response = await fetch('http://localhost:5000/api/food-items', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.access_token}`,
      },
      body: JSON.stringify(form.value),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to submit donation.");
    }
    
    isSuccess.value = true;
    formMessage.value = "Thank you! Your donation has been listed successfully.";
    form.value = { name: '', quantity: '', location: '' }; // Reset form
    activeTab.value = 'receive'; // Switch to available food tab to see the new item
    fetchAvailableFood(); // Refresh the list of available food
  } catch (error) {
    isSuccess.value = false;
    formMessage.value = error.message;
  } finally {
    isSubmitting.value = false;
  }
}

// --- NEW LOGIC FOR HANDLING FOOD REQUESTS ---

async function handleRequestFood(item) {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error("You must be logged in to make a request.");

    const response = await fetch('http://localhost:5000/api/requests', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.access_token}`,
      },
      body: JSON.stringify({
        food_item_id: item.id,
        donor_id: item.donor_id
      }),
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to submit request.");
    }
    
    alert('Request sent successfully!');
    // Refresh the list to update the item's status
    fetchAvailableFood();

  } catch (error) {
    alert(error.message);
  }
}

function isMyOwnItem(donorId) {
  return userSession.value && userSession.value.user.id === donorId;
}

function getButtonText(item) {
  if (isMyOwnItem(item.donor_id)) return "This is Your Item";
  if (item.status === 'requested') return "Requested";
  return "Request This Food";
}

// --- LIFECYCLE HOOK ---

onMounted(async () => {
  // Get the user session once when the component loads
  const { data } = await supabase.auth.getSession();
  userSession.value = data.session;
  // Fetch the initial list of food
  fetchAvailableFood();
});
</script>

<style scoped>
.dashboard-container { max-width: 900px; margin: 2rem auto; padding: 2rem; }
.tabs { display: flex; gap: 1rem; border-bottom: 1px solid #ddd; margin-bottom: 2rem; }
.tabs button {
  padding: 10px 20px; border: none; background: none; cursor: pointer;
  font-size: 1.1rem; border-bottom: 3px solid transparent;
}
.tabs button.active { border-bottom-color: #42b983; font-weight: bold; }

.share-form { max-width: 500px; margin: 1rem auto; }
.share-form input {
  display: block; width: 100%; padding: 12px; margin-bottom: 1rem;
  box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;
}
.share-form button {
  width: 100%; padding: 12px; background-color: #42b983; color: white;
  border: none; border-radius: 4px; cursor: pointer; font-size: 1rem;
}
.share-form button:disabled { background-color: #aaa; }

.food-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem; }
.food-card {
  border: 1px solid #eee; padding: 1.5rem; border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex; flex-direction: column;
}
.food-card h3 { margin-top: 0; }
.posted-at { font-size: 0.8rem; color: #888; margin-top: 1rem; }

.request-button {
  width: 100%; padding: 10px; background-color: #5cb85c; color: white;
  border: none; border-radius: 4px; cursor: pointer; margin-top: auto; /* Pushes button to the bottom */
  font-weight: bold;
}
.request-button:disabled { background-color: #aaa; cursor: not-allowed; }

.loading, .no-food { text-align: center; padding: 2rem; color: #777; }
.success-message { color: green; text-align: center; margin-top: 1rem; }
.error-message { color: red; text-align: center; margin-top: 1rem; }
</style>