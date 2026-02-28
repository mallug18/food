<template>
  <div class="donations-page">
    <!-- Page Hero -->
    <div class="page-hero">
      <div class="section-wrap">
        <span class="hero-badge">📋 My Activity</span>
        <h1>My <span class="grad-text">Donations</span></h1>
        <p>Track all your food listings, incoming requests, and approvals</p>
      </div>
    </div>

    <div class="page-content section-wrap">
      <!-- Loading -->
      <div v-if="loading" class="loading-wrap">
        <div v-for="i in 3" :key="i" class="donation-skeleton">
          <div class="sk sk-header"></div>
          <div class="sk sk-line"></div>
          <div class="sk sk-line sk-short"></div>
        </div>
      </div>

      <!-- Error -->
      <div v-if="error" class="page-error">⚠️ {{ error }}</div>

      <!-- Empty -->
      <div v-if="!loading && donations.length === 0 && !error" class="empty-state">
        <div class="empty-icon">📦</div>
        <h3>No donations yet</h3>
        <p>You haven't shared any food items yet. Head to the dashboard to list your first donation!</p>
        <RouterLink to="/dashboard" class="cta-btn">🍱 Go to Dashboard</RouterLink>
      </div>

      <!-- Donations Timeline -->
      <div v-if="!loading && donations.length > 0" class="timeline">
        <div
          v-for="(item, idx) in donations"
          :key="item.id"
          class="timeline-item"
          :style="{ animationDelay: (idx * 0.1) + 's' }"
        >
          <!-- Timeline dot -->
          <div class="timeline-dot" :class="item.status">
            <span>{{ statusEmoji(item.status) }}</span>
          </div>

          <!-- Card -->
          <div class="donation-card" :class="item.status">
            <div class="card-header">
              <div class="card-title-group">
                <span class="food-emoji-big">{{ getFoodEmoji(item.name) }}</span>
                <div>
                  <h3>{{ item.name }}</h3>
                  <div class="card-meta">
                    <span>⚖️ {{ item.quantity }}</span>
                    <span>📍 {{ item.location }}</span>
                  </div>
                </div>
              </div>
              <div class="status-badge" :class="item.status">
                {{ statusLabel(item.status) }}
              </div>
            </div>

            <!-- Request section -->
            <div v-if="item.requests && item.requests.length > 0" class="requests-section">
              <h4>📬 Incoming Requests</h4>
              <div v-for="req in item.requests" :key="req.id" class="request-row">

                <div v-if="req.status === 'pending'" class="request-pending">
                  <div class="requester-info">
                    <div class="requester-avatar">{{ getInitial(req.profiles?.username) }}</div>
                    <div>
                      <strong>{{ req.profiles?.username || 'A user' }}</strong>
                      <small>wants this food</small>
                    </div>
                  </div>
                  <button class="approve-btn" @click="handleApproval(req.id)">
                    ✅ Approve
                  </button>
                </div>

                <div v-if="req.status === 'approved'" class="request-approved">
                  <div class="approved-banner">
                    <span>🎉</span>
                    <div>
                      <strong>Request Approved!</strong>
                      <p>Coordinate pickup with the receiver:</p>
                    </div>
                  </div>
                  <div class="contact-details">
                    <div class="contact-item">
                      <span class="contact-icon">👤</span>
                      <span>{{ req.profiles?.username || 'N/A' }}</span>
                    </div>
                    <div class="contact-item">
                      <span class="contact-icon">📞</span>
                      <span>{{ req.profiles?.phone || 'No phone provided' }}</span>
                    </div>
                  </div>
                </div>

              </div>
            </div>

            <div v-else class="no-requests">
              <span>⏳</span> Waiting for someone to request this food
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { supabase } from '../supabase';
import apiClient from '@/api';

const donations = ref([]);
const loading = ref(true);
const error = ref('');

const foodEmojiMap = { rice:'🍚', curry:'🍛', bread:'🍞', fruit:'🍎', veg:'🥗', dal:'🫘', biryani:'🍛', chicken:'🍗', sweet:'🍮', milk:'🥛', pizza:'🍕', pasta:'🍝' };
function getFoodEmoji(name) {
  const n = (name || '').toLowerCase();
  for (const [k, v] of Object.entries(foodEmojiMap)) { if (n.includes(k)) return v; }
  return '🍱';
}
function getInitial(name) { return (name || 'U').charAt(0).toUpperCase(); }
function statusEmoji(s) { return { available:'✅', requested:'⏳', claimed:'🎉' }[s] || '📦'; }
function statusLabel(s) { return { available:'Available', requested:'Requested', claimed:'Claimed' }[s] || s; }

async function fetchMyDonations() {
  loading.value = true; error.value = '';
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error('You must be logged in.');
    const response = await apiClient.get('/api/my-donations', {
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
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
    if (!session) throw new Error('Authentication error.');
    await apiClient.post(`/api/requests/${requestId}/approve`, {}, {
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    fetchMyDonations();
  } catch (err) {
    alert(err.response?.data?.error || err.message);
  }
}

onMounted(() => fetchMyDonations());
</script>

<style scoped>
.donations-page { background: #f8fafc; min-height: 100vh; padding-top: 72px; }

/* Hero */
.page-hero {
  background: linear-gradient(135deg, #0a0f1e 0%, #1a2a4a 100%);
  padding: 3rem 1.5rem;
}
.page-hero .hero-badge {
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

/* Loading skeleton */
.loading-wrap { display: flex; flex-direction: column; gap: 1rem; }
.donation-skeleton { background: #fff; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.04); animation: shimmer 1.5s ease-in-out infinite; }
@keyframes shimmer { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
.sk { background: #e8e8ea; border-radius: 6px; margin-bottom: 0.75rem; }
.sk-header { height: 24px; width: 50%; }
.sk-line { height: 16px; width: 80%; }
.sk-short { width: 40%; }

/* Error */
.page-error { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; }

/* Empty */
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

/* Timeline */
.timeline { display: flex; flex-direction: column; gap: 1.5rem; position: relative; }
.timeline::before {
  content: ''; position: absolute; left: 20px; top: 30px; bottom: 30px;
  width: 2px; background: linear-gradient(to bottom, #10b981, rgba(16,185,129,0.1));
  border-radius: 2px;
}
.timeline-item {
  display: flex; gap: 1.25rem; align-items: flex-start;
  animation: slideIn 0.5s ease both;
}
@keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }

.timeline-dot {
  width: 42px; height: 42px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; z-index: 1; border: 3px solid #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  animation: dotPulse 2s ease-in-out infinite;
}
.timeline-dot.available { background: #ecfdf5; }
.timeline-dot.requested { background: #fff7ed; animation: dotPulse 1.5s ease-in-out infinite; }
.timeline-dot.claimed { background: #eff6ff; }
@keyframes dotPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.08); } }

/* Donation card */
.donation-card {
  flex: 1; background: #fff; border-radius: 16px; padding: 1.5rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.06);
  border-left: 4px solid #cbd5e1;
  transition: all 0.3s ease;
}
.donation-card:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.1); transform: translateY(-2px); }
.donation-card.available { border-left-color: #10b981; }
.donation-card.requested { border-left-color: #f59e0b; }
.donation-card.claimed { border-left-color: #6366f1; }

.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.75rem; }
.card-title-group { display: flex; align-items: flex-start; gap: 0.75rem; }
.food-emoji-big { font-size: 2rem; flex-shrink: 0; }
.card-title-group h3 { color: #0f172a; font-size: 1.1rem; margin: 0 0 0.3rem; }
.card-meta { display: flex; gap: 1rem; flex-wrap: wrap; }
.card-meta span { color: #64748b; font-size: 0.85rem; }

.status-badge {
  padding: 0.3rem 0.9rem; border-radius: 9999px;
  font-size: 0.78rem; font-weight: 700; text-transform: capitalize; flex-shrink: 0;
}
.status-badge.available { background: #ecfdf5; color: #065f46; }
.status-badge.requested { background: #fff7ed; color: #92400e; }
.status-badge.claimed { background: #eff6ff; color: #3730a3; }

/* Requests */
.requests-section { border-top: 1px solid #f1f5f9; margin-top: 1rem; padding-top: 1rem; }
.requests-section h4 { color: #374151; font-size: 0.9rem; margin-bottom: 0.75rem; }
.request-row { display: flex; flex-direction: column; gap: 0.5rem; }

.request-pending { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1rem; background: #fff7ed; border-radius: 12px; border: 1px solid #fed7aa; flex-wrap: wrap; }
.requester-info { display: flex; align-items: center; gap: 0.75rem; }
.requester-avatar {
  width: 36px; height: 36px; background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  color: #fff; font-weight: 800; font-size: 0.9rem; flex-shrink: 0;
}
.requester-info strong { display: block; color: #0f172a; font-size: 0.95rem; }
.requester-info small { color: #6b7280; font-size: 0.8rem; }

.approve-btn {
  padding: 0.55rem 1.25rem; background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border: none; border-radius: 9999px; font-size: 0.85rem; font-weight: 700;
  cursor: pointer; transition: all 0.3s ease; font-family: 'Inter', sans-serif;
  box-shadow: 0 4px 12px rgba(16,185,129,0.3);
}
.approve-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(16,185,129,0.4); }

.request-approved { padding: 1rem; background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(16,185,129,0.04)); border-radius: 12px; border: 1px solid rgba(16,185,129,0.2); }
.approved-banner { display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.75rem; font-size: 1.5rem; }
.approved-banner div strong { color: #065f46; display: block; }
.approved-banner div p { color: #047857; font-size: 0.85rem; margin: 0; }
.contact-details { display: flex; flex-direction: column; gap: 0.5rem; }
.contact-item { display: flex; align-items: center; gap: 0.75rem; }
.contact-icon { font-size: 1rem; }
.contact-item span:last-child { color: #0f172a; font-weight: 500; font-size: 0.9rem; }

.no-requests { color: #94a3b8; font-size: 0.85rem; padding: 0.5rem 0; display: flex; align-items: center; gap: 0.5rem; }

@media (max-width: 768px) {
  .hero-bar-inner { padding: 6rem 1rem 2rem; }
  .hero-titles h1 { font-size: 2rem; }
  .content-wrapper { padding: 2rem 1rem; }
  .timeline::before { left: 1.25rem; }
  .timeline-item { gap: 1rem; }
  .timeline-dot { width: 40px; height: 40px; flex-shrink: 0; margin-left: -5px; }
  .timeline-content { width: calc(100% - 50px); }
  .donation-card-header { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
  .donation-stats { flex-wrap: wrap; }
}
</style>