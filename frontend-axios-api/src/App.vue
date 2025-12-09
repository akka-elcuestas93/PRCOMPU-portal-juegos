<template>
  <div id="app" class="min-h-screen flex flex-col bg-[#1A1A1A] text-white">
    <!-- Barra de navegación global -->
    <NavBar />

    <!-- Contenido dinámico -->
    <main class="flex-1">
      <router-view v-if="ready" />
      <div v-else class="flex justify-center items-center h-64">
        <p class="text-gray-400">Cargando sesión...</p>
      </div>
    </main>

    <!-- Pie de página simple -->
    <footer class="border-t border-gray-700 py-4 text-center text-sm text-gray-400">
      <p>© 2025 Portal de Juegos — Desarrollado por Daniel Cuesta López y Alejandro Sánchez Febrero</p>
    </footer>
  </div>
</template>

<script setup>
import { session } from "@/stores/session";
import NavBar from "@/components/NavBar.vue";
import { computed } from "vue";

// estado para esperar a que se cargue la sesión (desde router)
const ready = computed(() => session.ready);
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: "Inter", "Segoe UI", Roboto, sans-serif;
}
a {
  color: #66b3ff;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
button {
  cursor: pointer;
}
</style>
