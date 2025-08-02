/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

<<<<<<< Updated upstream
=======
// Composables
import { createApp } from 'vue'

>>>>>>> Stashed changes
// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

<<<<<<< Updated upstream
// Composables
import { createApp } from 'vue'

=======
>>>>>>> Stashed changes
// Styles
import 'unfonts.css'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
