/**
 * E2E critical path 5: Submission status polling / evaluation result display
 *
 * After submitting an agent build, the learner must see the evaluation result
 * once it completes. This covers the async evaluation loop: submit → queued →
 * evaluated → result displayed with PF signal feedback.
 *
 * Failure here = learners submit work but never see feedback, breaking the
 * Productive Failure learning loop (lost training value + support escalations).
 *
 * NOTE: This test requires a fast evaluation path (mock evaluator or seeded result).
 * In CI, use E2E_MOCK_EVAL=true to short-circuit the judge and return a canned result.
 */
import { expect, test } from "@playwright/test";

const LEARNER_EMAIL = process.env.E2E_LEARNER_EMAIL ?? "learner@pilot.example";
const LEARNER_PASSWORD = process.env.E2E_LEARNER_PASSWORD ?? "password123";
const MOCK_EVAL = process.env.E2E_MOCK_EVAL === "true";

test.describe("Submission status polling", () => {
  test.skip(!MOCK_EVAL, "Requires E2E_MOCK_EVAL=true for fast evaluation turnaround");

  test("submission result is displayed after evaluation completes", async ({
    page,
  }) => {
    await page.goto("/login");
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill(LEARNER_PASSWORD);
    await page.getByRole("button", { name: /log in|sign in/i }).click();

    // Open first exercise
    const firstExercise = page
      .getByRole("link", { name: /exercise|challenge/i })
      .first();
    await firstExercise.waitFor();
    await firstExercise.click();

    // Fill in the agent builder
    const editor = page.getByRole("textbox").first();
    await editor.fill(
      JSON.stringify({
        schema_version: "1.0",
        model: "claude-haiku-4-5",
        tools: [{ name: "classify", description: "Classify sentiment" }],
      })
    );

    await page.getByRole("button", { name: /submit/i }).click();

    // Wait for result to appear (up to 20s — mock evaluator is fast)
    await expect(
      page.getByText(/score|feedback|productive|low.effort|off.task/i)
    ).toBeVisible({ timeout: 20_000 });

    // Score is visible (numeric or progress bar)
    await expect(page.getByText(/\d+%|\d+\.\d+/)).toBeVisible();
  });

  test("PF progress indicator updates after genuine attempt", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill(LEARNER_PASSWORD);
    await page.getByRole("button", { name: /log in|sign in/i }).click();

    const firstExercise = page
      .getByRole("link", { name: /exercise|challenge/i })
      .first();
    await firstExercise.waitFor();
    await firstExercise.click();

    // Submit productive attempt
    const editor = page.getByRole("textbox").first();
    await editor.fill(
      JSON.stringify({
        schema_version: "1.0",
        model: "claude-haiku-4-5",
        tools: [{ name: "classify", description: "Classify text" }],
        description: "First genuine attempt",
      })
    );
    await page.getByRole("button", { name: /submit/i }).click();

    // PF gate progress indicator shows attempt count increased
    await expect(
      page.getByText(/1\s*(of|\/)\s*\d+\s*(attempt|genuine)/i)
    ).toBeVisible({ timeout: 20_000 });
  });
});
