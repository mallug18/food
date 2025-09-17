import { ref } from 'vue';
import { supabase } from '../supabase';

const userSession = ref(null);

export function useAuth() {
  
  supabase.auth.onAuthStateChange((event, session) => {
    userSession.value = session;
  });
  
  const signUp = async (email, password, username) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          username: username, // Pass the username as metadata
        },
      },
    });
    if (error) throw error;
    return data;
  };

  const signIn = async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return data;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  };

  return {
    userSession,
    signUp,
    signIn,
    signOut,
  };
}