<template>
  <div class="requests-page">
    <div class="page-hero">
      <div class="section-wrap">
        <span class="hero-badge">📬 Requests</span>
        <h1>Manage <span class="grad-text">Incoming Requests</span></h1>
        <p>Review and approve requests for your food listings</p>
      </div>
    </div>

    <div class="page-content section-wrap">
      <div v-if="loading" class="loading-wrap">
        <div v-for="i in 3" :key="i" class="request-skeleton">
          <div class="sk sk-header"></div>
          <div class="sk sk-line"></div>
        </div>
      </div>

      <div v-if="error" class="page-error">⚠️ {{ error }}</div>

      <div v-if="!loading && requests.length === 0 && !error" class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>No pending requests</h3>
        <p>You don't have any pending requests to review right now.</p>
        <RouterLink to="/dashboard" class="cta-btn">Share More Food</RouterLink>
      </div>

      <div v-if="!loading && requests.length > 0" class="requests-grid">
        <div v-for="req in sortedRequests" :key="req.id" class="request-card" :class="req.status">
          <div class="req-header">
            <span class="food-emoji">{{ getFoodEmoji(req.food_items?.name) }}</span>
            <div class="req-food-info">
              <h3>{{ req.food_items?.name || 'Unknown Item' }}</h3>
              <span>{{ req.food_items?.quantity || 'Unknown Quantity' }}</span>
            </div>
            <div class="status-badge" :class="req.status">{{ req.status }}</div>
          </div>

          <div class="requester-details">
            <div class="requester-avatar">
              <img v-if="req.profiles?.avatar_url" :src="req.profiles.avatar_url" />
              <span v-else>{{ getInitial(req.profiles?.username) }}</span>
            </div>
            <div class="requester-info">
              <strong>{{ req.profiles?.username || 'A user' }}</strong>
              <small>wants to pick this up</small>
            </div>
            <div class="requester-phone">
              <span class="phone-icon">📞</span>
              <span>{{ req.profiles?.phone || 'No phone provided' }}</span>
            </div>
          </div>

          <div class="req-actions">
            <button 
              v-if="req.status === 'pending'" 
              class="approve-btn" 
              @click="handleApproval(req.id)"
              :disabled="approving === req.id"
            >
              <span v-if="approving === req.id" class="spin-ring"></span>
              <template v-else>✅ Approve Request</template>
            </button>
            <div v-else-if="req.status === 'approved'" class="approved-msg">
              <span class="check-icon">✓</span> Request Approved! Contact the receiver.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { supabase } from '../supabase';
import apiClient from '@/api';

const requests = ref([]);
const loading = ref(true);
const error = ref('');
const approving = ref(null);

const sortedRequests = computed(() => {
  return [...requests.value].sort((a, b) => {
    // Pending first
    if (a.status === 'pending' && b.status !== 'pending') return -1;
    if (a.status !== 'pending' && b.status === 'pending') return 1;
    return new Date(b.created_at) - new Date(a.created_at);
  });
});

const foodEmojiMap = { rice:'🍚', curry:'🍛', bread:'🍞', fruit:'🍎', veg:'🥗', dal:'🫘', biryani:'🍛', chicken:'🍗', sweet:'🍮', milk:'🥛', pizza:'🍕', pasta:'🍝' };
function getFoodEmoji(name) {
  const n = (name || '').toLowerCase();
  for (const [k, v] of Object.entries(foodEmojiMap)) { if (n.includes(k)) return v; }
  return '🍱';
}

function getInitial(name) { return (name || 'U').charAt(0).toUpperCase(); }

async function fetchRequests() {
  loading.value = true;
  error.value = '';
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error('You must be logged in.');
    const response = await apiClient.get('/api/incoming-requests', {
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    // Only show pending requests initially. If approved, it will stay in the list until refresh to see contact info.
    requests.value = response.data.filter(r => r.status === 'pending');
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

async function handleApproval(requestId) {
  approving.value = requestId;
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error('Authentication error.');
    await apiClient.post(`/api/requests/${requestId}/approve`, {}, {
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    
    // Optimistic update
    const reqIndex = requests.value.findIndex(r => r.id === requestId);
    if (reqIndex !== -1) {
      requests.value[reqIndex].status = 'approved';
    }

    // Fire event to update the navbar dot indicator globally
    window.dispatchEvent(new Event('request-approved'));

  } catch (err) {
    alert(err.response?.data?.error || err.message);
  } finally {
    approving.value = null;
  }
}

onMounted(() => fetchRequests());
</script>

<style scoped>
.requests-page { background: #f8fafc; min-height: 100vh; padding-top: 72px; }

.page-hero {
  background: linear-gradient(135deg, #0a0f1e 0%, #1a2a4a 100%);
  padding: 3rem 1.5rem;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.35rem 1rem; background: rgba(16,185,129,0.15);
  border: 1px solid rgba(16,185,129,0.3); border-radius: 9999px;
  color: #34d399; font-size: 0.8rem; font-weight: 600;
  letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 1rem;
}
.page-hero h1 { color: #f8fafc; font-size: clamp(1.8rem, 4vw, 2.5rem); margin-bottom: 0.5rem; }
.page-hero p { color: rgba(248,250,252,0.6); font-size: 1rem; }
.grad-text {
  background: linear-gradient(135deg, #10b981, #34d399);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.section-wrap { max-width: 900px; margin: 0 auto; padding: 0 1.5rem; }
.page-content { padding: 2.5rem 1.5rem; }

/* Error and Empty States */
.page-error { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; }
.empty-state { text-align: center; padding: 5rem 1.5rem; }
.empty-icon { font-size: 4rem; margin-bottom: 1rem; }
.empty-state h3 { color: #0f172a; font-size: 1.4rem; margin-bottom: 0.5rem; }
.empty-state p { color: #64748b; max-width: 380px; margin: 0 auto 2rem; line-height: 1.7; }
.cta-btn {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.85rem 2rem; background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border-radius: 9999px; text-decoration: none; font-weight: 600;
  transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(16,185,129,0.3);
}
.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(16,185,129,0.4); }

/* Loading */
.loading-wrap { display: flex; flex-direction: column; gap: 1rem; }
.request-skeleton { background: #fff; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.04); animation: shimmer 1.5s ease-in-out infinite; }
@keyframes shimmer { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
.sk { background: #e8e8ea; border-radius: 6px; margin-bottom: 0.75rem; }
.sk-header { height: 24px; width: 40%; }
.sk-line { height: 16px; width: 70%; }

/* Requests Grid */
.requests-grid { display: flex; flex-direction: column; gap: 1.25rem; }

.request-card {
  background: #fff; border-radius: 16px; padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  border-left: 5px solid #cbd5e1;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.request-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); }
.request-card.pending { border-left-color: #f59e0b; }
.request-card.approved { border-left-color: #10b981; background: #fafdfb; }

.req-header { display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1.2rem; border-bottom: 1px solid #f1f5f9; }
.food-emoji { font-size: 2.5rem; }
.req-food-info { flex: 1; min-width: 0; }
.req-food-info h3 { margin: 0 0 0.25rem 0; font-size: 1.2rem; color: #0f172a; word-wrap: break-word; overflow-wrap: break-word; word-break: break-word; }
.req-food-info span { color: #64748b; font-size: 0.9rem; word-wrap: break-word; overflow-wrap: break-word; word-break: break-word; }

.status-badge {
  padding: 0.35rem 1rem; border-radius: 9999px;
  font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
}
.status-badge.pending { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
.status-badge.approved { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }

.requester-details {
  display: flex; align-items: center; flex-wrap: wrap; gap: 1.25rem; margin-bottom: 1.5rem;
}
.requester-avatar {
  width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold; overflow: hidden;
}
.requester-avatar img { width: 100%; height: 100%; object-fit: cover; }
.requester-info { flex: 1; min-width: 0; }
.requester-info strong { display: block; font-size: 1.05rem; color: #1e293b; margin-bottom: 0.1rem; word-wrap: break-word; overflow-wrap: break-word; word-break: break-word; }
.requester-info small { color: #64748b; font-size: 0.85rem; }

.requester-phone {
  display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1rem;
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
  color: #0f172a; font-weight: 600; font-size: 0.95rem;
}
.phone-icon { font-size: 1.1rem; }

.req-actions { display: flex; justify-content: flex-end; }
.approve-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border: none; border-radius: 12px; font-size: 0.95rem;
  font-weight: 700; font-family: 'Inter', sans-serif; cursor: pointer;
  transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(16,185,129,0.3); min-width: 160px;
}
.approve-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(16,185,129,0.4); }
.approve-btn:disabled { opacity: 0.7; cursor: not-allowed; }

.spin-ring {
  width: 18px; height: 18px; border: 2.5px solid rgba(255,255,255,0.3);
  border-top-color: #fff; border-radius: 50%;
  animation: spin 0.7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

.approved-msg {
  display: flex; align-items: center; gap: 0.5rem;
  color: #047857; font-weight: 600; background: #ecfdf5;
  padding: 0.75rem 1.25rem; border-radius: 10px; border: 1px solid #a7f3d0;
}
.check-icon { background: #10b981; color: white; width: 20px; height: 20px; display: inline-flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 0.7rem; }

@media (max-width: 640px) {
  .req-header { flex-direction: column; align-items: flex-start; width: 100%; box-sizing: border-box; }
  .req-food-info { width: 100%; box-sizing: border-box; }
  .status-badge { margin-top: 0.5rem; }
  .requester-details { flex-direction: column; align-items: flex-start; gap: 1rem; width: 100%; box-sizing: border-box; }
  .requester-info { width: 100%; box-sizing: border-box; }
  .requester-phone { width: 100%; justify-content: center; box-sizing: border-box; }
  .approve-btn { width: 100%; box-sizing: border-box; }
}
</style>
