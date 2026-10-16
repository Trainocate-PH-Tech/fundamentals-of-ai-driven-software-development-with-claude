import { test, expect } from "@playwright/test";
test("category and issue lifecycle persists through real API and reload", async ({
  page,
}) => {
  const suffix = Date.now(),
    category = `Browser category ${suffix}`,
    title = `Browser issue ${suffix}`;
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/#/login");
  await page.getByLabel("Email").fill("admin@example.com");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: /sign in|login/i }).click();
  await page.getByRole("link", { name: "Categories", exact: true }).click();
  await page.getByLabel("Name").fill(category);
  await page.getByRole("button", { name: "Create category" }).click();
  await expect(
    page.getByRole("cell", { name: category, exact: true }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Issues", exact: true }).click();
  await page.getByRole("link", { name: "New issue" }).click();
  await expect(
    page.getByRole("heading", { name: "New issue", exact: true }),
  ).toBeVisible();
  await page.getByLabel("Title *", { exact: true }).fill(title);
  await page.getByLabel("Category").selectOption({ label: category });
  await page.getByLabel("Assignee").selectOption({ index: 1 });
  await page.getByRole("button", { name: "Save issue" }).click();
  await expect(page.getByRole("heading", { name: title })).toBeVisible();
  await page.getByRole("link", { name: "Edit issue" }).click();
  await page.getByLabel("Status").selectOption("in_progress");
  await page.getByLabel("Priority").selectOption("high");
  await page.getByRole("button", { name: "Save issue" }).click();
  await expect(page.getByText("in progress", { exact: true })).toBeVisible();
  await page.reload();
  await expect(page.getByText("high", { exact: true })).toBeVisible();
  await page.getByRole("link", { name: "Categories", exact: true }).click();
  await page
    .getByRole("row")
    .filter({ has: page.getByRole("cell", { name: category, exact: true }) })
    .getByRole("button", { name: "Delete" })
    .click();
  await page.getByRole("button", { name: "Confirm delete" }).click();
  await expect(page.getByRole("alert")).toContainText(/issue|use/i);
  await page.getByRole("link", { name: "Issues", exact: true }).click();
  await page.getByLabel("Search title").fill(title);
  await page.getByLabel("Status").selectOption("in_progress");
  await page.getByLabel("Priority").selectOption("high");
  await page.getByRole("button", { name: "Apply filters" }).click();
  await page.getByRole("link", { name: title, exact: true }).click();
  await page.getByRole("link", { name: "Edit issue" }).click();
  await page.getByLabel("Category").selectOption({ label: "Bug" });
  await page.getByLabel("Assignee").selectOption("");
  await page.getByRole("button", { name: "Save issue" }).click();
  await expect(
    page.getByRole("heading", { name: title, exact: true }),
  ).toBeVisible();
  await page.reload();
  await expect(page.getByText("Unassigned", { exact: true })).toBeVisible();
  await expect(page.getByText("Bug", { exact: true })).toBeVisible();
  await page.getByRole("link", { name: "Back to issues" }).click();
  const row = page
    .getByRole("row")
    .filter({ has: page.getByRole("link", { name: title, exact: true }) });
  await row.getByRole("button", { name: "Delete" }).click();
  await page.getByRole("button", { name: "Cancel", exact: true }).click();
  await expect(row).toBeVisible();
  await row.getByRole("button", { name: "Delete" }).click();
  await page.getByRole("button", { name: "Confirm delete" }).click();
  await expect(
    page.getByRole("link", { name: title, exact: true }),
  ).toHaveCount(0);
  await page.getByRole("link", { name: "Categories", exact: true }).click();
  await page
    .getByRole("row")
    .filter({ has: page.getByRole("cell", { name: category, exact: true }) })
    .getByRole("button", { name: "Delete" })
    .click();
  await page.getByRole("button", { name: "Confirm delete" }).click();
  await expect(
    page.getByRole("cell", { name: category, exact: true }),
  ).toHaveCount(0);
  expect(errors).toEqual([]);
});

test("empty filters, reset and network error feedback", async ({ page }) => {
  await page.goto("/#/login");
  await page.getByLabel("Email").fill("admin@example.com");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: /sign in|login/i }).click();
  await page.getByRole("link", { name: "Issues", exact: true }).click();
  await page.getByLabel("Search title").fill("no-such-issue-" + Date.now());
  await page.getByRole("button", { name: "Apply filters" }).click();
  await expect(
    page.getByText("No issues match the selected filters."),
  ).toBeVisible();
  await page.getByRole("button", { name: "Reset filters" }).click();
  await expect(page.getByLabel("Search title")).toHaveValue("");
  await page.route("**/issues?*", (route) => route.abort());
  await page.getByRole("button", { name: "Apply filters" }).click();
  await expect(page.getByRole("alert")).toContainText(
    "Unable to reach the API",
  );
});
