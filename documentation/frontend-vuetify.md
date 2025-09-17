## Vuetify setup (frontend)

- Vuetify v3.9.5 with Vue 3.5, Vite 7
- Core styles imported once via `vuetify/styles` and MDI icons via `@mdi/font`
- Icon set: Material Design Icons (font)
- Themes:
  - LightThemeC (default): background/surface and custom tokens used by CSS: `on-surface`, `overlay`, `infoBar`, `deadline`, `date`
  - DarkThemeC: matching tokens for dark mode; switchable via `defaultTheme` or programmatically
- Exposed constants: `THEME_LIGHT`, `THEME_DARK` for toggling
- Defaults set for common components: `VBtn`, `VCard`, `VTextField`, `VSelect`, `VAutocomplete`

File location: `frontend/src/plugins/vuetify.ts`

## Stylesheet Refactor

- All static styles for the frontend are now centralized in `frontend/src/styles/styles.css`.
- All colors, spacing, sizing, and border-radius values use CSS custom properties (variables) defined in the `:root` block for easy theming and maintainability.
- Component-specific styles (EventCard, TableEntry, DashboardLayout, EventActionsBox, EventTable, LoginView) are grouped and documented in the stylesheet for clarity.
- No local `<style>` blocks remain in Vue components except for dynamic inline styles (e.g., background images) and Vuetify theme props.
- All hardcoded values for color, padding, margin, and border-radius have been replaced with variables for consistency.
- The stylesheet is structured for easy navigation and future extension.

See `frontend/src/styles/styles.css` for the full structure and variable list.

## Composables & Script Refactor

- All major frontend logic has been modularized into composables in `frontend/src/composables/`.
- Vue components now import and use composables for all business logic, state, and actions. Only minimal wiring code remains in the components.
- Example composables: `EventTable`, `EventCard`, `TableEntry`, `LoginForm`, `EventActions`.
- All event, card, table, and login logic is handled in composables, making the codebase more maintainable and testable.
- Imports in Vue files now reference composables directly, with no duplicated logic or local script blocks.
- API data mapping (e.g., for event cards) is handled in composables to ensure correct fields and structure for UI components.
- This approach ensures a clear separation of concerns: UI in components, logic in composables, styles in the global stylesheet.

See the `frontend/src/composables/` folder for details and usage examples.
