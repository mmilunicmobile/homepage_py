import { defineConfig } from 'vite';
import solidPlugin from 'vite-plugin-solid';
// import devtools from 'solid-devtools/vite';

const components = ['src/pages/refactoringPython.jsx', 'src/pages/pagetwo.jsx'] //import.meta.glob('./src/web-components/*.jsx');

const export_paths = {}

for (const [number, path] of components.entries()) {
  export_paths["page" + number] = path
}

export default defineConfig({
  plugins: [
    /* 
    Uncomment the following line to enable solid-devtools.
    For more info see https://github.com/thetarnav/solid-devtools/tree/main/packages/extension#readme
    */
    // devtools(),
    solidPlugin({ ssr: true }),
  ],
  server: {
    port: 3000,
  },
  build: {
    target: 'esnext',
    manifest: true,
    rollupOptions: {
      // input: {
      //   refactoringPython: 'src/refactoringPython.jsx',
      //   // sussy: resolve(__dirname, 'src/pagetwo.jsx'),
      // }
      input: export_paths
    }
  }
});
