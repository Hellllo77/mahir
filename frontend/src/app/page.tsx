import { redirect } from "next/navigation";

/**
 * Root entry point — redirects to login.
 * After successful auth, the login page resolves the learner's active enrolment
 * and redirects to /cohorts/:cohortId, or /dashboard if no active enrolment.
 */
export default function RootPage() {
  redirect("/login");
}

