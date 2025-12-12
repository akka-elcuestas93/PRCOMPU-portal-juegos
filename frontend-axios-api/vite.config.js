import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig(async ({ command }) => {
  const plugins = [vue()];

  // ✅ Solo en local (vite serve)
  if (command === "serve") {
    const { default: VueDevTools } = await import("vite-plugin-vue-devtools");
    plugins.push(VueDevTools());
  }

  return { plugins };
});
