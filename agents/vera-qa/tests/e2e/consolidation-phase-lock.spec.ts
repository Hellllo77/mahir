/**
 * E2E critical path 2: Consolidation phase-lock
 *
 * A learner in the 'exploring' phase must NOT be able to access consolidation content.
 * This is the pedagogical invariant at the heart of Productive Failure (ADR-004).
 * Failure here = learners skip the struggle phase and the training loses its value.
 */
import { expect, test } from "@playwright/test";

const LEARNER_EMAIL = process.env.E2E_LEARNER_EMAIL ?? "learner@pilot.example";
const LEARNER_PASSWORD = process.env.E2E_LEARNER_PASSWORD ?? "password123";

test.describe("Consolidation phase-lock", () => {
  test("consolidation tab/link is not accessible while in exploring phase", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill(LEARNER_PASSWORD);
    await page.getByRole("button", { name: /log in|sign in/i }).click();

    // Open first exercise
    const firstExercise = page.getByRole("link", { name: /exercise|challenge/i }).first();
    await firstExercise.waitFor();
    await firstExercise.click();

    // If there's a "Consolidation" link/tab, clicking it must show a locked message
    const consolidationLink = page.getByRole("link", { name: /consolidation/i });
    const consolidationTab = page.getByRole("tab", { name: /consolidation/i });

    const target = (await consolidationLink.count()) > 0 ? consolidationLink : consolidationTab;

    if (await target.count() > 0) {
      await target.click();
      // Must show locked UI — not the reference solution
      await expect(page.getByText(/locked|complete.*exploration|not.*yet/i)).toBeVisible();
      await expect(page.getByText(/reference solution/i)).not.toBeVisible();
    } else {
      // Consolidation not surfaced at all when locked — also acceptable
      await expect(page.getByText(/reference solution/i)).not.toBeVisible();
    }
  });

  test("direct navigation to consolidation URL returns 409 or redirect", async ({
    page,
    request,
  }) => {
    // Get a valid exercise ID from the modules list via API
    const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/v1";

    // Log in to get a token
    const loginResp = await request.post(`${API_BASE}/auth/login`, {
      data: { email: LEARNER_EMAIL, password: LEARNER_PASSWORD },
    });
    expect(loginResp.ok()).toBeTruthy();
    const { access_token } = await loginResp.json();

    // Get the learner's profile to find enrolment and cohort
    const meResp = await request.get(`${API_BASE}/me`, {
      headers: { Authorization: `Bearer ${access_token}` },
    });
    expect(meResp.ok()).toBeTruthy();
    const me = await meResp.json();

    if (!me.enrolments?.length) {
      test.skip(true, "No enrolments — seed data required");
      return;
    }

    const cohortId = me.enrolments[0].cohort_id;
    const modulesResp = await request.get(`${API_BASE}/cohorts/${cohortId}/modules`, {
      headers: { Authorization: `Bearer ${access_token}` },
    });
    expect(modulesResp.ok()).toBeTruthy();
    const modules = await modulesResp.json();

    const firstExercise = modules[0]?.exercises?.[0];
    if (!firstExercise) {
      test.skip(true, "No exercises — seed data required");
      return;
    }

    // Direct API call to consolidation must return 409 while in exploring
    const consolidationResp = await request.get(
      `${API_BASE}/exercises/${firstExercise.id}/consolidation`,
      { headers: { Authorization: `Bearer ${access_token}` } }
    );
    expect(consolidationResp.status()).toBe(409);
    const body = await consolidationResp.json();
    expect(body.type ?? body.detail?.type).toBe("phase_locked");
  });
});
