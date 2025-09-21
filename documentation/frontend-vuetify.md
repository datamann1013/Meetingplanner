
# Meetingplanner Frontend (Vue 3 + Vuetify + Vite)

## Technology Stack
- **Vue 3.5** with `<script setup>` SFCs
- **TypeScript** throughout
- **Vite 7** for build/dev
- **Vuetify 3.9.5** (Material Design)
- **Pinia** for state management
- **Vue Router 4** for routing
- **Axios** for API calls

## Project Structure

- **Main entry:** `frontend/src/main.ts`
- **App shell:** `frontend/src/App.vue` (uses `<v-app>`, `<v-app-bar>`, `<router-view>`)
- **Routing:** `frontend/src/router/index.ts` (guards for auth, board role, guest)
- **State:** `frontend/src/stores/auth.ts` (Pinia, JWT, user roles)
- **API:** `frontend/src/services/strapi.ts` (Axios, JWT, auto-logout on 401)
- **Global styles:** `frontend/src/styles/styles.css` (all colors, spacing, etc. as CSS variables)
- **Vuetify config:** `frontend/src/plugins/vuetify.ts` (themes, defaults, icons)
- **Composables:** `frontend/src/composables/` (all business logic, e.g. `EventTable`, `EventCard`, `LoginForm`)
- **Components:**
  - `components/shared/` (UI: `EventCard`, `TableEntry`, `Dropdown`, etc.)
  - `components/admin/` (admin dashboard, event management)
  - `components/admin/eventview/` (event CRUD, modals, email, etc.)
- **Views:**
  - `views/index/HomeView.vue` (event list, uses `EventCard`)
  - `views/shared/LoginView.vue` (login form, uses `LoginForm` composable)
  - `views/admin/AdminView.vue` (admin dashboard, tabs, event management)

## Vuetify & Theming
- **Themes:**
  - `LightThemeC` (default): custom palette, background/surface, tokens for overlays/infoBar/deadline
  - `DarkThemeC`: matching tokens for dark mode
- **Switching:** Use `THEME_LIGHT`/`THEME_DARK` constants or set `defaultTheme` in `vuetify.ts`
- **Icons:** Material Design Icons (mdi)
- **Component defaults:**
  - `VBtn`, `VCard`, `VTextField`, `VSelect`, `VAutocomplete` (density, variant, rounded)
- **Location:** `frontend/src/plugins/vuetify.ts`

## Stylesheet
- **All static styles** in `frontend/src/styles/styles.css`
- **CSS variables** for all colors, spacing, sizing, border-radius (see `:root`)
- **Component-specific sections**: EventCard, TableEntry, DashboardLayout, EventActionsBox, EventTable, LoginView
- **No local `<style>` blocks** in Vue files except for dynamic inline styles (e.g. background images)
- **Consistent use of variables** for all color, padding, margin, border-radius
- **Structure:**
  1. Root Variables
  2. Shared Components
  3. Specific Components (EventCard, TableEntry, etc.)
  4. Views (LoginView, etc.)

## Composables
- **All business logic** is in composables in `frontend/src/composables/`
- **Examples:**
  - `EventTable`: fetches and maps event data for tables
  - `EventCard`: computes cover image style, date formatting
  - `LoginForm`: handles login, state, navigation
  - `TableEntry`: generic table logic
- **Pattern:** Components import composables, only minimal wiring in `<script setup>`
- **API mapping** (e.g. event fields) is handled in composables

## Components
- **Shared:**
  - `EventCard.vue`: Card for event display (used in HomeView, etc.)
  - `TableEntry.vue`: Generic table, slot-based columns
  - `Dropdown.vue`, `DateTimePicker.vue`, `FileUploadBox.vue`, etc.
- **Admin:**
  - `DashboardLayout.vue`, `DualInteractiveBoxes.vue`, `SidebarItem.vue`
  - `eventview/`: `EventTable.vue`, `EditEventModal.vue`, `EmailSenderBox.vue`, etc.

## Views
- **HomeView.vue:** Event list, uses `EventCard`, shows loading/errors
- **LoginView.vue:** Login form, uses `LoginForm` composable
- **AdminView.vue:** Sidebar, tabs, event management, dashboard widgets

## Routing & Auth
- **Routes:** `/` (Home), `/login`, `/admin` (board only)
- **Guards:**
  - `requiresAuth`, `requiresBoard`, `requiresGuest` (see `router/index.ts`)
- **Auth:**
  - Pinia store, JWT in localStorage, auto-check on navigation
  - Board role: `user.role.name === 'Board'`

## API
- **Strapi backend** via Axios wrapper (`services/strapi.ts`)
- **JWT** sent on all requests, auto-logout on 401
- **Event data**: `/events?populate=*` (see `EventTable` composable)

---
**For peers:**
- All business/data logic is in composables, not components
- All static styles are in the global stylesheet, not in components
- All theming and Vuetify config is in `plugins/vuetify.ts`
- Use the folder structure above to quickly locate logic, UI, or config
