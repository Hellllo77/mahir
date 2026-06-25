"use client";

import { useEffect } from "react";
import { clearToken, clearRole } from "@/lib/api-client";

export default function LogoutPage() {
  useEffect(() => {
    clearToken();
    clearRole();
    window.location.replace("/login");
  }, []);
  return null;
}
