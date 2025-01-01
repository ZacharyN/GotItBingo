// vite.config.js
export default {
  build: {
    // Build files to Django's static directory
    outDir: '../backend/static/dist',
    assetsDir: '',
    manifest: true,
    rollupOptions: {
      input: 'src/main.js',
    },
  },
  server: {
    // Configure dev server to proxy API requests to Django
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
}