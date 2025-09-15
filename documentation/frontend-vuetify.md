## Vuetify setup (frontend)

- Vuetify v3.9.5 with Vue 3.5, Vite 7
- Core styles imported once via `vuetify/styles` and MDI icons via `@mdi/font`
- Icon set: Material Design Icons (font)
- Themes:
  - LightThemeC (default): background/surface and custom tokens used by CSS: `on-surface`, `overlay`, `infoBar`, `deadline`, `date`
  - DarkThemeC: matching tokens for dark mode; switchable via `defaultTheme` or programmatically
- Exposed constants: `THEME_LIGHT`, `THEME_DARK` for toggling
- Defaults set for common components: `VBtn`, `VCard`, `VTextField`, `VSelect`, `VAutocomplete`

Notes and next steps:

- System theme: consider dynamic theme based on `prefers-color-scheme` and a user toggle in the UI
- Icons: if switching to SVG icons for performance, wire with `vuetify/iconsets/svg` or custom SVGs
- Locale: add Vuetify locale when i18n is introduced (e.g., Norwegian Bokmål)
- Treeshaking: current setup registers all `components` and `directives`. For smaller bundles, introduce `vite-plugin-vuetify` with auto-import/SSR support and remove the broad registration
- Lab components: if needed, enable via `vite-plugin-vuetify` options

File location: `frontend/src/plugins/vuetify.ts`

## Stylesheet Refactor

- All static styles for the frontend are now centralized in `frontend/src/styles/styles.css`.
- All colors, spacing, sizing, and border-radius values use CSS custom properties (variables) defined in the `:root` block for easy theming and maintainability.
- Component-specific styles (EventCard, TableEntry, DashboardLayout, EventActionsBox, EventTable, LoginView) are grouped and documented in the stylesheet for clarity.
- No local `<style>` blocks remain in Vue components except for dynamic inline styles (e.g., background images) and Vuetify theme props.
- All hardcoded values for color, padding, margin, and border-radius have been replaced with variables for consistency.
- The stylesheet is structured for easy navigation and future extension.

See `frontend/src/styles/styles.css` for the full structure and variable list.
