import { useState, useEffect } from 'react';

const STORAGE_KEY = 'userProfile';

/**
 * Hook para manejar el perfil de usuario en LocalStorage
 */
export function useUserProfile() {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadProfile();
    }, []);

    const loadProfile = () => {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                setProfile(JSON.parse(stored));
            }
        } catch (error) {
            console.error('Error loading profile:', error);
        } finally {
            setLoading(false);
        }
    };

    const saveProfile = (newProfile) => {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(newProfile));
            setProfile(newProfile);
            return true;
        } catch (error) {
            console.error('Error saving profile:', error);
            return false;
        }
    };

    const updateProfile = (updates) => {
        const updated = { ...profile, ...updates };
        return saveProfile(updated);
    };

    const clearProfile = () => {
        localStorage.removeItem(STORAGE_KEY);
        setProfile(null);
    };

    return {
        profile,
        loading,
        saveProfile,
        updateProfile,
        clearProfile,
        hasProfile: !!profile
    };
}
