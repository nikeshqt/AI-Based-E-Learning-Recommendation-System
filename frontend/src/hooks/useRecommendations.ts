import { useState, useEffect } from 'react';
import type { RecommendationItem } from '../types/recommendation';
import { fetchPersonalizedRecommendations } from '../services/recommendationService';

export const useRecommendations = (userId: string = 'usr_98741') => {
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    const loadRecs = async () => {
      try {
        setLoading(true);
        const data = await fetchPersonalizedRecommendations(userId);
        if (isMounted) {
          setRecommendations(data.recommendations);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setError('Using offline recommendation fallback state.');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadRecs();
    return () => {
      isMounted = false;
    };
  }, [userId]);

  return { recommendations, loading, error };
};
