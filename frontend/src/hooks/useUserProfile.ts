import { useState, useEffect } from 'react';
import type { UserProfile } from '../types/user';
import { getUserProfile } from '../services/userService';

const defaultProfile: UserProfile = {
  user_id: 'usr_98741',
  full_name: 'Alex Morgan',
  email: 'alex.morgan@ai-learning.io',
  learning_goal: 'Data Science & AI Engineering',
  preferred_learning_style: 'visual',
  skill_level: 'intermediate',
  weekly_goal_hours: 5,
  completed_hours: 4.2,
  streak_days: 12,
  skills: [
    { skill_id: 'sk_py', skill_name: 'Python', mastery_score: 0.85, last_evaluated: '2026-09-24', category: 'Programming' },
    { skill_id: 'sk_ds', skill_name: 'Data Structs', mastery_score: 0.75, last_evaluated: '2026-09-22', category: 'CS Core' },
    { skill_id: 'sk_ml', skill_name: 'Machine Learning', mastery_score: 0.60, last_evaluated: '2026-09-20', category: 'AI' },
    { skill_id: 'sk_gnn', skill_name: 'RecSys Architecture', mastery_score: 0.70, last_evaluated: '2026-09-25', category: 'AI' },
  ],
};

export const useUserProfile = (userId: string = 'usr_98741') => {
  const [profile, setProfile] = useState<UserProfile>(defaultProfile);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    const loadProfile = async () => {
      try {
        setLoading(true);
        const data = await getUserProfile(userId);
        if (isMounted && data) {
          setProfile(data);
        }
      } catch (err) {
        // Fallback to default mock profile
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadProfile();
    return () => {
      isMounted = false;
    };
  }, [userId]);

  return { profile, loading };
};
