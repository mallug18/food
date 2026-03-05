<template>
    <div class="settings-page">
        <div class="page-hero">
            <div class="section-wrap">
                <span class="hero-badge">⚙️ Settings</span>
                <h1>Profile <span class="grad-text">Settings</span></h1>
                <p>Update your personal information and preferences</p>
            </div>
        </div>

        <div class="page-content section-wrap">
            <div class="settings-layout">

                <!-- Sidebar -->
                <div class="settings-sidebar">
                    <button class="menu-item active">
                        <span class="icon">👤</span> Personal Info
                    </button>
                    <RouterLink to="/update-password" class="menu-item">
                        <span class="icon">🔑</span> Security
                    </RouterLink>
                </div>

                <!-- Main Form -->
                <div class="settings-main">
                    <div class="settings-card">

                        <div v-if="loading" class="loading-overlay">
                            <span class="spinner"></span> Loading profile...
                        </div>

                        <form @submit.prevent="saveProfile" class="profile-form">

                            <!-- Avatar Upload -->
                            <div class="avatar-section">
                                <div class="avatar-wrapper">
                                    <img v-if="profilePreview || form.avatar_url"
                                        :src="profilePreview || form.avatar_url" class="avatar-img" />
                                    <div v-else class="avatar-placeholder">{{ getInitial(form.username) }}</div>

                                    <button type="button" class="avatar-edit-btn" @click="$refs.fileInput.click()">
                                        <span>📷</span> Edit
                                    </button>
                                    <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*"
                                        style="display: none;" />
                                </div>
                                <div class="avatar-text">
                                    <h3>Profile Picture</h3>
                                    <p>PNG, JPG up to 5MB. Recommended size is 256x256px.</p>
                                </div>
                            </div>

                            <hr class="divider" />

                            <!-- Form Fields -->
                            <div class="form-grid">
                                <div class="field-wrap">
                                    <label>Full Name</label>
                                    <div class="input-group">
                                        <span class="input-icon">👤</span>
                                        <input v-model="form.username" type="text" placeholder="Your name" required />
                                    </div>
                                </div>

                                <div class="field-wrap">
                                    <label>Email Address</label>
                                    <div class="input-group">
                                        <span class="input-icon">📧</span>
                                        <input :value="email" type="email" disabled class="disabled-input" />
                                    </div>
                                    <small class="help-text">Email cannot be changed directly.</small>
                                </div>

                                <div class="field-wrap">
                                    <label>Phone Number</label>
                                    <div class="input-group">
                                        <span class="input-icon">📞</span>
                                        <input v-model="form.phone" type="tel" placeholder="Your mobile number" />
                                    </div>
                                </div>

                                <div class="field-wrap">
                                    <label>Location</label>
                                    <div class="input-group">
                                        <span class="input-icon">📍</span>
                                        <input v-model="form.location" type="text"
                                            placeholder="e.g. Bangalore, India" />
                                    </div>
                                </div>
                            </div>

                            <!-- Messages & Submit -->
                            <div class="form-footer">
                                <Transition name="fade">
                                    <div v-if="message" class="status-msg" :class="isError ? 'error' : 'success'">
                                        {{ isError ? '⚠️' : '✅' }} {{ message }}
                                    </div>
                                </Transition>

                                <button type="submit" class="save-btn" :disabled="saving">
                                    <span v-if="saving" class="spin-ring"></span>
                                    <template v-else>Save Changes</template>
                                </button>
                            </div>

                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '../supabase';
import apiClient from '@/api';

const loading = ref(true);
const saving = ref(false);
const message = ref('');
const isError = ref(false);

const email = ref('');
const form = ref({
    username: '',
    phone: '',
    location: '',
    avatar_url: ''
});

const fileInput = ref(null);
const profilePreview = ref(null);
const profileBase64 = ref(null);

function getInitial(name) {
    return name ? name.charAt(0).toUpperCase() : 'U';
}

const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        profilePreview.value = e.target.result;
        profileBase64.value = e.target.result;
    };
    reader.readAsDataURL(file);
};

const fetchProfile = async () => {
    try {
        const { data: { session } } = await supabase.auth.getSession();
        if (!session) return;

        email.value = session.user.email;

        const response = await apiClient.get('/api/profile', {
            headers: { Authorization: `Bearer ${session.access_token}` },
        });

        if (response.data) {
            form.value.username = response.data.username || '';
            form.value.phone = response.data.phone || '';
            form.value.location = response.data.location || '';
            form.value.avatar_url = response.data.avatar_url || '';
        }
    } catch (error) {
        console.error("Failed to load profile:", error);
        showMessage("Failed to load profile data.", true);
    } finally {
        loading.value = false;
    }
};

const showMessage = (msg, error = false) => {
    message.value = msg;
    isError.value = error;
    setTimeout(() => { message.value = ''; }, 4000);
};

const saveProfile = async () => {
    saving.value = true;
    message.value = '';

    try {
        const { data: { session } } = await supabase.auth.getSession();

        const payload = {
            username: form.value.username,
            phone: form.value.phone,
            location: form.value.location,
        };

        if (profileBase64.value) {
            payload.profile_picture_base64 = profileBase64.value;
        }

        const response = await apiClient.post('/api/profile', payload, {
            headers: { Authorization: `Bearer ${session.access_token}` },
        });

        showMessage("Profile updated successfully!");

        // Update local state if image changed
        if (response.data.avatar_url) {
            form.value.avatar_url = response.data.avatar_url;
            profileBase64.value = null; // reset

            // Update supabase auth metadata
            await supabase.auth.updateUser({
                data: { avatar_url: response.data.avatar_url }
            });
        }

    } catch (error) {
        showMessage(error.response?.data?.error || error.message, true);
    } finally {
        saving.value = false;
    }
};

onMounted(() => {
    fetchProfile();
});
</script>

<style scoped>
.settings-page {
    background: #f8fafc;
    min-height: 100vh;
    padding-top: 72px;
}

.page-hero {
    background: linear-gradient(135deg, #0a0f1e 0%, #1a2a4a 100%);
    padding: 3rem 1.5rem;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 1rem;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 9999px;
    color: #34d399;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.page-hero h1 {
    color: #f8fafc;
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    margin-bottom: 0.5rem;
}

.page-hero p {
    color: rgba(248, 250, 252, 0.6);
    font-size: 1rem;
    margin: 0;
}

.grad-text {
    background: linear-gradient(135deg, #10b981, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section-wrap {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

.page-content {
    padding: 3rem 1.5rem;
}

.settings-layout {
    display: flex;
    gap: 2.5rem;
    align-items: flex-start;
}

/* Sidebar */
.settings-sidebar {
    width: 240px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.85rem 1rem;
    background: transparent;
    border: none;
    border-radius: 10px;
    color: #475569;
    font-size: 0.95rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    text-align: left;
    text-decoration: none;
    transition: all 0.2s;
}

.menu-item:hover {
    background: #f1f5f9;
    color: #0f172a;
}

.menu-item.active {
    background: #fff;
    color: #10b981;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    font-weight: 600;
}

.icon {
    font-size: 1.1rem;
}

/* Main Area */
.settings-main {
    flex: 1;
}

.settings-card {
    background: #fff;
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
}

.loading-overlay {
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(4px);
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    font-weight: 500;
    color: #64748b;
}

.spinner {
    width: 24px;
    height: 24px;
    border: 3px solid #e2e8f0;
    border-top-color: #10b981;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Avatar section */
.avatar-section {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.avatar-wrapper {
    position: relative;
}

.avatar-img {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #e2e8f0;
}

.avatar-placeholder {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: bold;
    border: 3px solid #e2e8f0;
}

.avatar-edit-btn {
    position: absolute;
    bottom: 0;
    right: -5px;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.avatar-edit-btn:hover {
    border-color: #10b981;
    color: #10b981;
}

.avatar-text h3 {
    margin: 0 0 0.25rem 0;
    font-size: 1.1rem;
    color: #0f172a;
}

.avatar-text p {
    margin: 0;
    color: #64748b;
    font-size: 0.85rem;
}

.divider {
    height: 1px;
    background: #f1f5f9;
    border: none;
    margin: 2rem 0;
}

/* Form Fields */
.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.field-wrap label {
    display: block;
    font-weight: 600;
    font-size: 0.9rem;
    color: #334155;
    margin-bottom: 0.5rem;
}

.input-group {
    position: relative;
    display: flex;
    align-items: center;
}

.input-icon {
    position: absolute;
    left: 1rem;
    font-size: 1rem;
    z-index: 1;
}

.input-group input {
    width: 100%;
    padding: 0.85rem 1rem 0.85rem 2.8rem;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    font-size: 0.95rem;
    color: #0f172a;
    transition: all 0.2s;
    background: #fff;
    outline: none;
    font-family: 'Inter', sans-serif;
}

.input-group input:focus {
    border-color: #10b981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

.disabled-input {
    background: #f8fafc !important;
    color: #94a3b8 !important;
    cursor: not-allowed;
}

.help-text {
    display: block;
    margin-top: 0.4rem;
    font-size: 0.8rem;
    color: #94a3b8;
}

.form-footer {
    margin-top: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 1rem;
}

.status-msg {
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 500;
}

.status-msg.success {
    background: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
}

.status-msg.error {
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.save-btn {
    padding: 0.85rem 2rem;
    background: linear-gradient(135deg, #10b981, #059669);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    min-width: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.save-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.save-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.spin-ring {
    width: 20px;
    height: 20px;
    border: 2.5px solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@media (max-width: 768px) {
    .settings-layout {
        flex-direction: column;
    }

    .settings-sidebar {
        width: 100%;
        flex-direction: row;
        overflow-x: auto;
        padding-bottom: 0.5rem;
    }

    .menu-item {
        white-space: nowrap;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

    .form-footer {
        flex-direction: column-reverse;
        align-items: stretch;
    }

    .save-btn {
        width: 100%;
    }
}
</style>
