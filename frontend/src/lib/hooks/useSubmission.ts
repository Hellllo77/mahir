"use client";

import { useEffect, useRef, useState } from "react";
import { getSubmission } from "../api-client";
import type { SubmissionDetail } from "../api-types";

const TERMINAL = new Set(["evaluated", "failed"]);
const POLL_MS = 3000;

export function useSubmission(submissionId: string | null) {
  const [data, setData] = useState<SubmissionDetail | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!submissionId) return;
    let cancelled = false;

    async function poll() {
      try {
        const result = await getSubmission(submissionId!);
        if (cancelled) return;
        setData(result);
        if (!TERMINAL.has(result.status)) {
          timerRef.current = setTimeout(poll, POLL_MS);
        }
      } catch (err) {
        if (!cancelled) setError(err as Error);
      }
    }

    poll();

    return () => {
      cancelled = true;
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [submissionId]);

  return { data, error };
}
