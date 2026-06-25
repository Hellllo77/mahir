"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getRole } from "@/lib/api-client";

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("mahir_token");
    if (token) {
      const role = getRole();
      const isStaff = role === "org_admin" || role === "super_admin" || role === "facilitator";
      router.replace(isStaff ? "/facilitator/cohorts" : "/dashboard");
    } else {
      router.replace("/login");
    }
  }, [router]);

  return null;
}
