import { useState, useEffect } from 'react';

export function useMetrics() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch data
  }, []);

  return { data, loading };
}
