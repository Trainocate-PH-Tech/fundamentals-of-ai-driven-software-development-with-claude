# AGENTS.md

## Purpose

This repository is a React admin panel template. When extending it, follow the existing users feature and service modules instead of introducing a new frontend architecture.

This guide is for AI agents and contributors so new screens keep the same routing, component structure, API interaction pattern, and visual style.

## Stack Summary

- React function components
- `react-router-dom` with hash-based routing
- Custom `esbuild` build script in `build.js`
- Bootstrap and project SCSS for layout and styling
- FontAwesome for icons
- Axios for backend API calls
- JWT authentication stored in `localStorage`

## Core Architectural Pattern

This app uses page components backed by thin service modules.

- Page components own screen state, loading state, navigation, and rendering.
- Backend calls belong in `src/js/services/*Service.js`.
- API headers and token access belong in shared helpers, not inline in screens.
- Shared UI wrappers and primitives belong in `src/js/commons/`.
- Generic helpers belong in `src/js/helpers/`.

Do not add a global state library, API client framework, TypeScript conversion, or a new build tool unless the task explicitly asks for that change.

## Project Conventions

### Components

- Use function components and React hooks.
- Keep authenticated feature screens under `src/js/<feature>/` when the feature has multiple screens.
- Keep one-off top-level pages under `src/js/`.
- Export components with the current default export style.
- Use `PageHeader` and `AdminContent` for standard admin pages.
- Use `Loader` for loading states when it fits the existing page shape.

Example shape:

```js
const WidgetsIndex = () => {
  return (
    <div className="d-flex flex-column gap-4">
      <PageHeader eyebrow="Administration" title="Widgets" />
      <AdminContent title="Widget Directory">
        ...
      </AdminContent>
    </div>
  );
};

export default WidgetsIndex;
```

### Routing

- Routes live in `src/js/App.js`.
- Public routes render from `PublicApp`.
- Authenticated routes render from `AuthenticatedApp` inside the sidebar layout.
- The app uses hash routing; use normal route paths such as `/users` and let `HashRouter` handle the hash.
- Add sidebar navigation in `src/js/Sidebar.js` when a feature should be discoverable from the main nav.

### Styling

- Prefer Bootstrap utilities, cards, tables, badges, form classes, and spacing first.
- Add SCSS only when Bootstrap utilities are not enough.
- Put shared style imports in `src/styles/index.scss`.
- Keep the interface simple and dense like an admin tool.
- Buttons should include a relevant FontAwesome icon when a matching icon exists.
- Use badges for statuses, preferably through `statusToLabel(status)` when the existing status palette fits.

## API Service Pattern

All backend interaction should go through a service module.

### Rules

- Create one service file per backend resource or domain area, for example `src/js/services/WidgetService.js`.
- Import `axios` directly in the service module.
- Import `buildHeaders` or `buildFileUploadHeaders` from `src/js/helpers/AppHelper.js`.
- Return the raw axios promise from service functions.
- Let the calling component decide how to set state, show validation errors, redirect, or display alerts.
- Do not manually read `localStorage` or build `Authorization` headers in page components.
- Do not duplicate token/session logic outside `AuthService.js` and `AppHelper.js`.
- Keep service function names action-oriented: `fetchWidgets`, `fetchWidget`, `createWidget`, `updateWidget`, `deleteWidget`.

### Standard JSON Requests

Follow the existing `UserService.js` pattern:

```js
import axios from "axios";
import { buildHeaders } from "../helpers/AppHelper";

export const fetchWidgets = (args = {}) => {
  return axios.get(`${API_BASE_URL}/widgets`, {
    params: args,
    headers: buildHeaders()
  });
};

export const fetchWidget = (id) => {
  return axios.get(`${API_BASE_URL}/widgets/${id}`, {
    headers: buildHeaders()
  });
};

export const createWidget = (args) => {
  return axios.post(`${API_BASE_URL}/widgets`, args, {
    headers: buildHeaders()
  });
};

export const updateWidget = (id, args) => {
  return axios.put(`${API_BASE_URL}/widgets/${id}`, args, {
    headers: buildHeaders()
  });
};

export const deleteWidget = (id) => {
  return axios.delete(`${API_BASE_URL}/widgets/${id}`, {
    headers: buildHeaders()
  });
};
```

For a system health check endpoint, keep the API call in a service module as well:

```js
import axios from "axios";
import { buildHeaders } from "../helpers/AppHelper";

export const fetchSystemHealthCheck = () => {
  return axios.get(`${API_BASE_URL}/system/health_check`, {
    headers: buildHeaders()
  });
};
```

### File Upload Requests

Use `buildFileUploadHeaders()` for multipart requests:

```js
import axios from "axios";
import { buildFileUploadHeaders } from "../helpers/AppHelper";

export const uploadWidgetImage = (id, formData) => {
  return axios.post(`${API_BASE_URL}/widgets/${id}/image`, formData, {
    headers: buildFileUploadHeaders()
  });
};
```

## API Response Handling

Keep API response handling in page components consistent with the users screens.

- For index endpoints, expect the Rails API pagination shape:
  - `records`
  - `current_page`
  - `total_pages`
  - `next_page`
  - `prev_page`
- For validation failures, expect HTTP `422` and an object whose keys are field names and values are arrays of messages.
- Use `getInputClassName(errors, field)` and `renderInputErrors(errors, field)` for form validation UI.
- For authorization failures that should end the session, call `destroySession()` and navigate to `/login`.
- Prefer a `pageError` or `errorMessage` string for non-validation failures.

Example form error handling:

```js
request
  .then((response) => {
    setErrors({});
    navigate(`/widgets/${response.data.id}`);
  })
  .catch((error) => {
    if (error.response?.status === 403) {
      destroySession();
      navigate("/login");
      return;
    }

    if (error.response?.status === 422) {
      setErrors(error.response.data);
      setPageError("");
      return;
    }

    setPageError(error.response?.data?.message || "Unable to save widget.");
  });
```

## Feature Checklist

When adding a backend-backed feature:

1. Add or update a service module under `src/js/services/`.
2. Add screen components under `src/js/<feature>/` when multiple screens are needed.
3. Use local `useState` for form values, errors, loading flags, page errors, pagination, and records.
4. Use existing commons and helpers before adding new abstractions.
5. Register routes in `src/js/App.js`.
6. Add navigation in `src/js/Sidebar.js` if the feature belongs in the sidebar.
7. Add feature SCSS only if Bootstrap utilities are insufficient.
8. Run `npm run build` before finishing when environment variables are available.

## Build And Environment

The build is custom and depends on build-time environment variables.

Expected variables include:

- `API_BASE_URL`
- `TOKEN_BEARER`
- `CURRENT_USER`
- `API_VERSION`

If `API_VERSION` is missing, `npm run build` fails before app code runs. When build verification is blocked by missing environment, report that clearly instead of changing app code to bypass it.

## Existing Quirks

- `HashRouter` is intentional.
- The custom build pipeline is intentional.
- The mock server and login form may not be perfectly aligned; do not silently repair unrelated mock behavior while building a feature.
- Keep changes scoped to the requested feature or fix.
