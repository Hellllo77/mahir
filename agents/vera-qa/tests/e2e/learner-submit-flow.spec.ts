/**
 * E2E critical path 1: Learner login → module list → exercise view → submit agent
 *
 * Covers the primary revenue path for the Mahir Co-Worker pilot.
 * Failure here = learner cannot complete any exercise.
 */
import { expect, test } from "@playwright/test";

const LEARNER_EMAIL = process.env.E2E_LEARNER_EMAIL ?? "learner@pilot.example";
const LEARNER_PASSWORD = process.env.E2E_LEARNER_PASSWORD ?? "password123";

test.describe("Learner submit flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
  });

  test("learner can log in and see module list", async ({ page }) => {
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill(LEARNER_PASSWORD);
    await page.getByRole("button", { name: /log in|sign in/i }).click();

    // Redirected away from login
    await expect(page).not.toHaveURL(/\/login/);

    // Module navigation is visible
    await expect(page.getByRole("navigation")).toBeVisible();
  });

  test("learner can open an exercise and see the problem prompt", async ({ page }) => {
    // Login
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill(LEARNER_PASSWORD);
    await page.getByRole("button", { name: /log in|sign in/i }).click();

    // Navigate to first available exercise
    const firstExercise = page.getByRole("link", { name: /exercise|challenge/i }).first();
    await firstExercise.waitFor({ state: "visible" });
    await firstExercise.click();

    // Exercise prompt is rendered
    await expect(page.getByText(/build/i)).toBeVisible();

    // Consolidation content must NOT be visible (PF gate)
    await expect(page.getByText(/reference solution/i)).not.toBeVisible();
  });

  test("learner can submit an agent build and see queued status", async ({ page }) => {
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill(LEARNER_PASSWORD);
    await page.getByRole("button", { name: /log in|sign in/i }).click();

    const firstExercise = page.getByRole("link", { name: /exercise|challenge/i }).first();
    await firstExercise.waitFor();
    await firstExercise.click();

    // Fill in the agent builder textarea/editor
    const editor = page.getByRole("textbox").first();
    await editor.fill(
      JSON.stringify({
        schema_version: "1.0",
        model: "claude-haiku-4-5",
        tools: [{ name: "classify", description: "Classify text sentiment" }],
      })
    );

    // Submit
    const submitButton = page.getByRole("button", { name: /submit/i });
    await submitButton.click();

    // Status indicator shows queued or evaluating
    await expect(
      page.getByText(/queued|evaluating|submitted/i)
    ).toBeVisible({ timeout: 10_000 });
  });
});
