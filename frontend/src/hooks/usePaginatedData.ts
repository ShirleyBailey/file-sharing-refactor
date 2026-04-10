"use client";

import { useCallback, useEffect, useState } from "react";
import type { PagedResponse } from "@/lib/api";

type FetchFn<T> = (page: number, pageSize: number) => Promise<PagedResponse<T>>;

export function usePaginatedData<T>(fetchFn: FetchFn<T>, pageSize = 20) {
  const [data, setData] = useState<PagedResponse<T> | null>(null);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(
    async (p: number) => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await fetchFn(p, pageSize);
        setData(result);
        setPage(p);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Произошла ошибка");
      } finally {
        setIsLoading(false);
      }
    },
    [fetchFn, pageSize],
  );

  useEffect(() => {
    void load(1);
  }, [load]);

  return { data, page, isLoading, error, load };
}
