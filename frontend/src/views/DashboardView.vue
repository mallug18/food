<template>
  <div class="dashboard-page">
    <!-- Page header -->
    <div class="dash-hero">
      <div class="dash-hero-inner section-wrap">
        <div class="dash-greeting">
          <span class="greeting-icon">👋</span>
          <div>
            <h1>Your Dashboard</h1>
            <p>Manage food donations and requests from one place</p>
          </div>
        </div>
        <div class="dash-quick-tabs">
          <button
            :class="['tab-pill', { active: activeTab === 'share' }]"
            @click="activeTab = 'share'"
          >
            <span>🍱</span> Share Food
          </button>
          <button
            :class="['tab-pill', { active: activeTab === 'receive' }]"
            @click="activeTab = 'receive'; fetchAvailableFood()"
          >
            <span>🤝</span> Find Food
            <span v-if="availableFood.length > 0" class="tab-count">{{ availableFood.length }}</span>
          </button>
        </div>
      </div>
    </div>

    <div class="dash-content section-wrap">

      <!-- ── SHARE TAB ─────────────────────────────── -->
      <Transition name="tab-fade" mode="out-in">
        <div v-if="activeTab === 'share'" key="share" class="tab-panel">
          <div class="panel-split">
            <!-- Form -->
            <div class="share-form-card">
              <div class="card-top">
                <span class="card-icon">📦</span>
                <div>
                  <h2>List a Donation</h2>
                  <p>Fill in the details below to share your surplus food</p>
                </div>
              </div>

              <form @submit.prevent="handleShareFood" class="share-form">
                <div class="form-field">
                  <label>Food Name</label>
                  <div class="field-input">
                    <span>🍛</span>
                    <input v-model="form.name" type="text" placeholder="e.g., Rice and Curry, Bread Loaves" required />
                  </div>
                </div>
                <div class="form-field">
                  <label>Quantity</label>
                  <div class="field-input">
                    <span>⚖️</span>
                    <input v-model="form.quantity" type="text" placeholder="e.g., Serves 5 people, 2kg" required />
                  </div>
                </div>
                <div class="form-field">
                  <label>Pickup Location</label>
                  <div class="field-input">
                    <span>📍</span>
                    <input v-model="form.location" type="text" placeholder="e.g., Indiranagar, Bengaluru" required />
                  </div>
                </div>

                <Transition name="msg-fade">
                  <div v-if="formMessage" class="form-msg" :class="isSuccess ? 'success' : 'error'">
                    {{ isSuccess ? '✅' : '⚠️' }} {{ formMessage }}
                  </div>
                </Transition>

                <button type="submit" class="submit-btn" :disabled="isSubmitting">
                  <span v-if="isSubmitting" class="spin-ring"></span>
                  <template v-else><span>🚀</span> Share Food Now</template>
                </button>
              </form>
            </div>

            <!-- Tips -->
            <div class="tips-card">
              <h3>💡 Tips for Good Donations</h3>
              <ul>
                <li>✅ Ensure food is fresh and safe to eat</li>
                <li>✅ Provide an accurate quantity estimate</li>
                <li>✅ Choose a public, accessible pickup location</li>
                <li>✅ Respond promptly to pickup requests</li>
                <li>✅ Package food hygienically when possible</li>
              </ul>
              <div class="impact-preview">
                <span class="impact-emoji">🌱</span>
                <p>Each donation prevents waste and helps a neighbour!</p>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- ── RECEIVE TAB ────────────────────────────── -->
      <Transition name="tab-fade" mode="out-in">
        <div v-if="activeTab === 'receive'" key="receive" class="tab-panel">
          <div class="receive-header">
            <h2>Available Food Near You</h2>
            <button class="refresh-btn" @click="fetchAvailableFood" :disabled="loading">
              <span :class="{ spinning: loading }">↻</span> Refresh
            </button>
          </div>

          <!-- Loading skeleton -->
          <div v-if="loading" class="food-grid">
            <div v-for="i in 6" :key="i" class="food-card skeleton">
              <div class="sk-line sk-title"></div>
              <div class="sk-line sk-short"></div>
              <div class="sk-line sk-short"></div>
              <div class="sk-line sk-btn"></div>
            </div>
          </div>

          <div v-if="apiError" class="api-error">⚠️ {{ apiError }}</div>

          <div v-if="!loading && availableFood.length === 0 && !apiError" class="empty-state">
            <div class="empty-icon">🍽️</div>
            <h3>No food available right now</h3>
            <p>Be the first to share! Switch to the Share tab to list a donation.</p>
            <button class="tab-pill active" @click="activeTab = 'share'">
              🍱 Share Food
            </button>
          </div>

          <div v-if="!loading && availableFood.length > 0" class="food-grid">
            <div
              v-for="(item, idx) in availableFood"
              :key="item.id"
              class="food-card"
              :style="{ animationDelay: (idx * 0.07) + 's' }"
            >
              <div class="food-card-top">
                <div class="food-emoji">{{ getRandomFoodEmoji(item.name) }}</div>
                <span class="food-status" :class="item.status">{{ item.status }}</span>
              </div>
              <h3>{{ item.name }}</h3>
              <div class="food-meta">
                <span>⚖️ {{ item.quantity }}</span>
                <span>📍 {{ item.location }}</span>
              </div>
              <p class="food-date">🕒 {{ formatDate(item.created_at) }}</p>
              <button
                class="request-btn"
                @click="handleRequestFood(item)"
                :disabled="isMyOwnItem(item.donor_id) || item.status === 'requested'"
                :class="{ mine: isMyOwnItem(item.donor_id), requested: item.status === 'requested' }"
              >
                {{ getButtonText(item) }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '../supabase';
import apiClient from '@/api';

const activeTab = ref('receive');
const isSubmitting = ref(false);
const formMessage = ref('');
const isSuccess = ref(false);
const userSession = ref(null);
const availableFood = ref([]);
const loading = ref(true);
const apiError = ref('');

const form = ref({ name: '', quantity: '', location: '' });

const foodEmojis = { rice: '🍚', curry: '🍛', bread: '🍞', fruit: '🍎', veg: '🥗', dal: '🫘', biryani: '🍛', chicken: '🍗', sweet: '🍮', milk: '🥛' };
function getRandomFoodEmoji(name) {
  const n = name.toLowerCase();
  for (const [k, v] of Object.entries(foodEmojis)) {
    if (n.includes(k)) return v;
  }
  return '🍱';
}
function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

async function fetchAvailableFood() {
  loading.value = true;
  apiError.value = '';
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error('You must be logged in to view food items.');
    const response = await apiClient.get('/api/food-items', {
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    availableFood.value = response.data;
  } catch (error) {
    apiError.value = error.response?.data?.error || error.message;
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
    if (!session) throw new Error('You must be logged in to share food.');
    await apiClient.post('/api/food-items', form.value, {
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    isSuccess.value = true;
    formMessage.value = 'Thank you! Your donation has been listed successfully.';
    form.value = { name: '', quantity: '', location: '' };
    setTimeout(() => { activeTab.value = 'receive'; fetchAvailableFood(); }, 1800);
  } catch (error) {
    isSuccess.value = false;
    formMessage.value = error.response?.data?.error || error.message;
  } finally {
    isSubmitting.value = false;
  }
}

async function handleRequestFood(item) {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error('You must be logged in to make a request.');
    await apiClient.post('/api/requests', { food_item_id: item.id, donor_id: item.donor_id }, {
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    fetchAvailableFood();
  } catch (error) {
    alert(error.response?.data?.error || error.message);
  }
}

function isMyOwnItem(donorId) {
  return userSession.value && userSession.value.user.id === donorId;
}
function getButtonText(item) {
  if (isMyOwnItem(item.donor_id)) return '👤 Your Item';
  if (item.status === 'requested') return '⏳ Already Requested';
  return '🤝 Request This Food';
}

onMounted(async () => {
  const { data } = await supabase.auth.getSession();
  userSession.value = data.session;
  fetchAvailableFood();
});
</script>

<style scoped>
.dashboard-page { background: #f8fafc; min-height: 100vh; padding-top: 72px; }

/* Hero bar */
.dash-hero {
  background: linear-gradient(135deg, #0a0f1e 0%, #1a3a2a 100%);
  padding: 2.5rem 1.5rem;
}
.dash-hero-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}
.dash-greeting { display: flex; align-items: center; gap: 1rem; }
.greeting-icon { font-size: 2.5rem; animation: wave 2s ease-in-out infinite; }
@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(15deg); }
  75% { transform: rotate(-10deg); }
}
.dash-greeting h1 { color: #f8fafc; font-size: 1.75rem; margin: 0 0 0.2rem; }
.dash-greeting p { color: rgba(248,250,252,0.6); margin: 0; font-size: 0.95rem; }

.dash-quick-tabs { display: flex; gap: 0.75rem; }

.tab-pill {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 9999px;
  color: rgba(248,250,252,0.75);
  font-size: 0.9rem; font-weight: 500;
  cursor: pointer; transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}
.tab-pill:hover { background: rgba(255,255,255,0.12); color: #fff; }
.tab-pill.active { background: linear-gradient(135deg, #10b981, #059669); border-color: transparent; color: #fff; box-shadow: 0 4px 16px rgba(16,185,129,0.3); }

.tab-count {
  background: rgba(255,255,255,0.25);
  padding: 1px 7px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
}

/* Content */
.section-wrap { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }
.dash-content { padding: 2.5rem 1.5rem; }

/* Transitions */
.tab-fade-enter-active, .tab-fade-leave-active { transition: all 0.3s ease; }
.tab-fade-enter-from { opacity: 0; transform: translateY(12px); }
.tab-fade-leave-to { opacity: 0; transform: translateY(-8px); }

.msg-fade-enter-active, .msg-fade-leave-active { transition: all 0.3s ease; }
.msg-fade-enter-from, .msg-fade-leave-to { opacity: 0; transform: translateY(-8px); }

/* Share tab */
.panel-split {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
@media (min-width: 768px) { .panel-split { grid-template-columns: 1.5fr 1fr; } }

.share-form-card {
  background: #fff;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  border: 1px solid #f0f0f0;
}
.card-top { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 2rem; }
.card-icon { font-size: 2.5rem; }
.card-top h2 { color: #0f172a; margin: 0 0 0.25rem; font-size: 1.4rem; }
.card-top p { color: #64748b; font-size: 0.9rem; margin: 0; }

.share-form { display: flex; flex-direction: column; gap: 1rem; }
.form-field label { display: block; font-weight: 600; font-size: 0.9rem; color: #374151; margin-bottom: 0.5rem; }
.field-input { display: flex; align-items: center; border: 1.5px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #f8fafc; transition: all 0.3s ease; }
.field-input:focus-within { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.12); }
.field-input span { padding: 0 0.85rem; font-size: 1.1rem; background: transparent; }
.field-input input {
  flex: 1; padding: 0.85rem 0.85rem 0.85rem 0;
  border: none; background: transparent; outline: none;
  font-size: 0.95rem; font-family: 'Inter', sans-serif; color: #0f172a;
}
.field-input input::placeholder { color: #94a3b8; }

.form-msg { padding: 0.75rem 1rem; border-radius: 10px; font-size: 0.9rem; }
.form-msg.success { background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; }
.form-msg.error { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; }

.submit-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  padding: 1rem; background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border: none; border-radius: 12px; font-size: 1rem;
  font-weight: 700; font-family: 'Inter', sans-serif;
  cursor: pointer; transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(16,185,129,0.3);
  min-height: 52px;
}
.submit-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(16,185,129,0.4); }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }

.spin-ring {
  width: 20px; height: 20px; border: 2.5px solid rgba(255,255,255,0.3);
  border-top-color: #fff; border-radius: 50%;
  animation: spin 0.7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

.tips-card {
  background: linear-gradient(145deg, #f0fdf4, #ecfdf5);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 20px;
  padding: 2rem;
}
.tips-card h3 { color: #0f172a; font-size: 1.1rem; margin-bottom: 1.25rem; }
.tips-card ul { list-style: none; display: flex; flex-direction: column; gap: 0.7rem; }
.tips-card li { color: #374151; font-size: 0.9rem; }
.impact-preview { display: flex; align-items: center; gap: 0.75rem; margin-top: 1.5rem; padding: 1rem; background: rgba(16,185,129,0.1); border-radius: 12px; }
.impact-emoji { font-size: 1.75rem; }
.impact-preview p { color: #065f46; font-size: 0.9rem; line-height: 1.5; margin: 0; }

/* Receive tab */
.receive-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.receive-header h2 { color: #0f172a; }
.refresh-btn {
  display: flex; align-items: center; gap: 0.4rem;
  padding: 0.5rem 1rem; border-radius: 9999px;
  border: 1.5px solid #10b981; background: transparent;
  color: #10b981; font-weight: 600; font-size: 0.85rem;
  cursor: pointer; transition: all 0.3s ease; font-family: 'Inter', sans-serif;
}
.refresh-btn:hover { background: #10b981; color: #fff; }
.spinning { display: inline-block; animation: spin 0.8s linear infinite; }

/* Food grid */
.food-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}
.food-card {
  background: #fff; border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #f0f0f0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  display: flex; flex-direction: column; gap: 0.5rem;
  transition: all 0.3s ease;
  animation: cardIn 0.5s ease both;
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.food-card:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(0,0,0,0.1); border-color: rgba(16,185,129,0.2); }
.food-card-top { display: flex; justify-content: space-between; align-items: flex-start; }
.food-emoji { font-size: 2rem; }
.food-status {
  padding: 3px 12px; border-radius: 9999px; font-size: 0.78rem;
  font-weight: 700; text-transform: capitalize;
}
.food-status.available { background: #ecfdf5; color: #065f46; }
.food-status.requested { background: #fff7ed; color: #9a3412; }
.food-status.claimed { background: #fef2f2; color: #991b1b; }
.food-card h3 { color: #0f172a; font-size: 1.05rem; margin: 0; }
.food-meta { display: flex; flex-direction: column; gap: 0.25rem; }
.food-meta span { color: #64748b; font-size: 0.85rem; }
.food-date { color: #94a3b8; font-size: 0.8rem; margin-top: auto; }

.request-btn {
  width: 100%; padding: 0.75rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border: none; border-radius: 10px;
  font-size: 0.9rem; font-weight: 600; font-family: 'Inter', sans-serif;
  cursor: pointer; transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(16,185,129,0.25);
}
.request-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(16,185,129,0.4); }
.request-btn:disabled { background: linear-gradient(135deg, #94a3b8, #64748b); box-shadow: none; cursor: not-allowed; transform: none; }

/* Skeleton */
.skeleton { animation: shimmer 1.5s infinite; pointer-events: none; }
@keyframes shimmer { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
.sk-line { background: #e2e8f0; border-radius: 6px; margin-bottom: 0.75rem; }
.sk-title { height: 22px; width: 70%; }
.sk-short { height: 16px; width: 50%; }
.sk-btn { height: 42px; width: 100%; margin-top: auto; border-radius: 10px; }

/* Empty state */
.empty-state { text-align: center; padding: 4rem 1.5rem; }
.empty-icon { font-size: 4rem; margin-bottom: 1rem; }
.empty-state h3 { color: #0f172a; font-size: 1.4rem; margin-bottom: 0.5rem; }
.empty-state p { color: #64748b; margin-bottom: 2rem; }

.api-error { background: #fef2f2; border: 1px solid #fecaca; padding: 1rem 1.5rem; border-radius: 12px; color: #dc2626; margin-bottom: 1.5rem; }
@media (max-width: 768px) {
  .hero-bar-inner { padding: 6rem 1rem 2rem; flex-direction: column; gap: 1.5rem; }
  .hero-titles h1 { font-size: 2rem; }
  .tab-buttons { align-self: stretch; display: flex; background: rgba(0,0,0,0.2); }
  .tab-btn { flex: 1; justify-content: center; padding: 0.6rem; font-size: 0.85rem; }
  .content-wrapper { padding: 2rem 1rem; }
  .dashboard-grid { grid-template-columns: 1fr; gap: 2rem; }
  .food-grid { grid-template-columns: 1fr; }
}
</style>