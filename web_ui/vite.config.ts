import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ command, mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    // 基础路径配置
    base: command === 'serve' ? '/' : '/',
    // 开发服务器配置
    server: {
      proxy: {
        '/wx': {
          target: env.VITE_API_BASE_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
    // 构建配置
    build: {
      outDir: '../static',
      emptyOutDir: true,
      assetsDir: 'assets'
    }
  }
})