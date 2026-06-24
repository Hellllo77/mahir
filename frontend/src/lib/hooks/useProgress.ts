"use client";

import { useEffect, useState } from "react";
import { getExerciseProgress } from "../api-client";
import type { ExerciseProgress } from "../api-types";

export function useExerciseProgress(exerciseId: string) {
  const [data, setData] = useState<ExerciseProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getExerciseProgress(exerciseId)
      .then((p) => { if (!cancelled) setData(p); })
      .catch((e) => { if (!cancelled) setError(e); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [exerciseId]);

  const refresh = () => {
    getExerciseProgress(exerciseId)
      .then(setData)
      .catch(setError);
  };

  return { data, loading, error, refresh };
}
