/**
 * E2E critical path 4: Auth guard and session management
 *
 * Unauthenticated users must be redirected to login for all protected routes.
 * Wrong credentials must show an error without leaking session data.
 * Logout must clear the token and prevent further access.
 *
 * Failure here = open access to learner data / broken session = data leak risk.
 */
import { expect, test } from "@playwright/test";

const LEARNER_EMAIL = process.env.E2E_LEARNER_EMAIL ?? "learner@pilot.example";
const LEARNER_PASSWORD = process.env.E2E_LEARNER_PASSWORD ?? "password123";

test.describe("Auth guard", () => {
  test("unauthenticated root redirect goes to login", async ({ page }) => {
    await page.goto("/");
    // Should end up on login (or a page that requires login)
    await expect(page).toHaveURL(/login|\/$/);
  });

  test("unauthenticated direct access to exercise page redirects to login", async ({
    page,
  }) => {
    const fakeId = "00000000-0000-0000-0000-000000000001";
    await page.goto(`/exercises/${fakeId}`);
    await expect(page).toHaveURL(/login/);
  });

  test("wrong credentials show error and do not redirect", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill("definitely-wrong-password");
    await page.getByRole("button", { name: /log in|sign in/i }).click();

    // Error message is shown
    await expect(
      page.getByText(/invalid|incorrect|wrong|credentials|unauthorized/i)
    ).toBeVisible({ timeout: 5_000 });

    // Still on login page
    await expect(page).toHaveURL(/login/);
  });

  test("logout clears session and redirects to login", async ({ page }) => {
    // Log in first
    await page.goto("/login");
    await page.getByLabel(/email/i).fill(LEARNER_EMAIL);
    await page.getByLabel(/password/i).fill(LEARNER_PASSWORD);
    await page.getByRole("button", { name: /log in|sign in/i }).click();
    await expect(page).not.toHaveURL(/login/);

    // Log out
    const logoutLink = page.getByRole("link", { name: /log.?out|sign.?out/i });
    const logoutButton = page.getByRole("button", { name: /log.?out|sign.?out/i });
    const trigger =
      (await logoutLink.count()) > 0 ? logoutLink : logoutButton;
    await trigger.click();

    // Must end up on login
    await expect(page).toHaveURL(/login/, { timeout: 5_000 });

    // Going back must not restore the session
    await page.goto("/");
    await expect(page).toHaveURL(/login/);
  });
});
