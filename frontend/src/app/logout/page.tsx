"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { clearToken, clearRole } from "@/lib/api-client";

export default function LogoutPage() {
  const router = useRouter();
  useEffect(() => {
    clearToken();
    clearRole();
    router.replace("/login");
  }, [router]);
  return null;
}
