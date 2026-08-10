import { useState, useEffect } from 'react';

export function useAuth() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch data
  }, []);

  return { data, loading };
}
