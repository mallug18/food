<template>
  <div class="page-container">
    <h1>My Donations</h1>
    <p>Here you can see the status of all the food items you have listed for donation.</p>

    <div v-if="loading">Loading your donations...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="!loading && donations.length === 0" class="no-donations">
      You have not donated any items yet. Go to the dashboard to share food!
    </div>
    
    <div class="donations-list">
      <div v-for="item in donations" :key="item.id" class="donation-card" :class="item.status">
        <div class="card-header">
          <h3>{{ item.name }}</h3>
          <span class="status-badge">{{ item.status }}</span>
        </div>
        <p><strong>Quantity:</strong> {{ item.quantity }}</p>
        <p><strong>Location:</strong> {{ item.location }}</p>

        <div v-if="item.requests && item.requests.length > 0" class="requests-section">
          <h4>Incoming Request:</h4>
          <div v-for="request in item.requests" :key="request.id" class="request-details">
            
            <div v-if="request.status === 'pending'">
              <p>Requested by: <strong>{{ request.profiles.username || 'A user' }}</strong></p>
              <div class="action-buttons">
                <button @click="handleApproval(request.id)" class="approve-button">Approve Request</button>
              </div>
            </div>

            <div v-if="request.status === 'approved'" class="approved-info">
              <p><strong>Request Approved!</strong></p>
              <p>You can now contact the receiver to arrange pickup:</p>
              <ul>
                <li><strong>Receiver:</strong> {{ request.profiles.username || 'N/A' }}</li>
                <li><strong>Contact:</strong> {{ request.profiles.phone || 'No phone number provided' }}</li>
              </ul>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '../supabase'; // We still need this for authentication
import apiClient from '@/api'; // <-- 1. IMPORT THE CENTRAL API CLIENT

const donations = ref([]);
const loading = ref(true);
const error = ref('');

async function fetchMyDonations() {
  loading.value = true;
  error.value = '';
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error("You must be logged in.");

    // 2. USE THE API CLIENT INSTEAD OF FETCH (GET REQUEST)
    const response = await apiClient.get('/api/my-donations', {
      headers: { 'Authorization': `Bearer ${session.access_token}` },
    });
    
    // With axios (used by apiClient), the JSON data is in `response.data`
    donations.value = response.data;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

async function handleApproval(requestId) {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error("Authentication error.");

    // 3. USE THE API CLIENT FOR THE POST REQUEST
    await apiClient.post(`/api/requests/${requestId}/approve`, {}, { // POST data is the second argument
      headers: {
        'Authorization': `Bearer ${session.access_token}`,
      },
    });
    
    alert('Request approved!');
    fetchMyDonations(); // Refresh the list of donations
  } catch (err) {
    // Axios provides more detailed error messages
    alert(err.response?.data?.error || err.message);
  }
}

onMounted(() => {
  fetchMyDonations();
});
</script>

<style scoped>
.page-container { max-width: 900px; margin: 2rem auto; }
.donations-list { margin-top: 2rem; display: grid; gap: 1.5rem; }
.donation-card {
  border: 1px solid #eee; padding: 1.5rem; border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border-left: 5px solid #ccc;
}
.donation-card.available { border-left-color: #5cb85c; }
.donation-card.requested { border-left-color: #f0ad4e; }
.donation-card.claimed { border-left-color: #d9534f; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.status-badge {
  padding: 5px 10px; border-radius: 15px; color: white;
  font-size: 0.8rem; text-transform: capitalize;
}
.donation-card.available .status-badge { background-color: #5cb85c; }
.donation-card.requested .status-badge { background-color: #f0ad4e; }
.donation-card.claimed .status-badge { background-color: #d9534f; }
.requests-section { border-top: 1px solid #eee; margin-top: 1rem; padding-top: 1rem; }
.request-details { background-color: #f9f9f9; padding: 1rem; border-radius: 5px; }
.action-buttons { margin-top: 10px; }
.approve-button {
  background-color: #42b983; color: white; border: none;
  padding: 8px 15px; border-radius: 5px; cursor: pointer;
}
.approved-info { background-color: #e8f5e9; padding: 1rem; border-radius: 5px; }
.approved-info ul { list-style: none; padding-left: 0; }
.error-message, .no-donations { text-align: center; color: #777; padding: 2rem; }
</style>