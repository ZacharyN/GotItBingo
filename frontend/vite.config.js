import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // Forward API requests to Django
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      // Forward media/static requests to Django
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    // Output to Django's static directory
    outDir: '../static/dist',
    assetsDir: '',
    manifest: true,
    rollupOptions: {
      input: 'src/main.js'
    }
  }
})