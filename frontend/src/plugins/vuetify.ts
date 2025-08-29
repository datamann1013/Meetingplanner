import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import type { ThemeDefinition } from 'vuetify'

const LightThemeC: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#FBF5DB', 
    surface: '#C8DAA6',    
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
  }
}

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
    defaultTheme: 'LightThemeC',
    themes: {
      LightThemeC,
    },
  },
})

export type Vuetify = ReturnType<typeof createVuetify>