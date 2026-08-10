import { useState, useEffect } from 'react';

export function useTasks() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch data
  }, []);

  return { data, loading };
}
