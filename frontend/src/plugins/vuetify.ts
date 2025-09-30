import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import type { ThemeDefinition } from 'vuetify'

const LightThemeC: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#FBF5DB', 
    surface: '#f5f5f5',    // Changed to match input field color (--color-table-header-bg)
    primary: '#76944C',    
    'primary-darken-1': '#60793E', 
    secondary: '#FFD21D',  
    'secondary-darken-1': '#D9B310', 
    error: '#B00020',
    info: '#2196F3',
    success: '#4CAF50', 
    warning: '#FB8C00',
   
    'on-surface': '#2E2E2E',
    overlay: 'rgba(200,218,166,0.95)',
    infoBar: 'rgba(200,218,166,0.85)',
    deadline: '#FFD21D',

  }
}

const DarkThemeC: ThemeDefinition = {
  dark: true,
  colors: {
    background: '#0F120D',
    surface: '#1E2616',
    primary: '#A7C957',
    'primary-darken-1': '#8FB247',
    secondary: '#FFD21D',
    'secondary-darken-1': '#D9B310',
    error: '#CF6679',
    info: '#64B5F6',
    success: '#66BB6A',
    warning: '#FFB74D',

    'on-surface': '#ECEFE8',
    overlay: 'rgba(31, 41, 22, 0.92)',
    infoBar: 'rgba(31, 41, 22, 0.88)',
    deadline: '#FFD21D',
    date: '#2E3B21',
    sidebar: '#60793E',
  }
}

export const THEME_LIGHT = 'LightThemeC' as const
export const THEME_DARK = 'DarkThemeC' as const

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    // Use light theme by default; switch to THEME_DARK to enable dark mode
    defaultTheme: THEME_LIGHT,
    themes: {
      LightThemeC,
      DarkThemeC,
    },
  },
  // App-wide sensible defaults (can be overridden per component)
  defaults: {
    VBtn: { variant: 'text', density: 'comfortable' },
    VCard: { rounded: 'lg' },
    VTextField: { density: 'comfortable', variant: 'outlined' },
    VSelect: { density: 'comfortable', variant: 'outlined' },
    VAutocomplete: { density: 'comfortable', variant: 'outlined' },
  },
})

export type Vuetify = ReturnType<typeof createVuetify>