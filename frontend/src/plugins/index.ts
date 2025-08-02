/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

<<<<<<< Updated upstream
// Plugins
import vuetify from './vuetify'
import router from '../router'

// Types
import type { App } from 'vue'
=======
// Types
import type { App } from 'vue'
import router from '../router'

// Plugins
import vuetify from './vuetify'
>>>>>>> Stashed changes

export function registerPlugins (app: App) {
  app
    .use(vuetify)
    .use(router)
}
