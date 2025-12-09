<script setup>
import { session } from "@/stores/session";
import { logout } from "@/api/auth";
import { useRouter } from "vue-router";
const router = useRouter();

async function doLogout() {
  try {
    await logout();
    session.user = null;
    router.push("/");
  } catch (e) {
    console.error(e);
  }
}
</script>

<template>
  <header class="nav">
    <div class="nav__inner">
      <router-link to="/" class="brand">🎮 Portal de Juegos</router-link>
      <nav class="links">
        <router-link to="/games">Juegos</router-link>
      </nav>
      <div class="auth">
        <template v-if="session.user">
          <span class="hello">
            Hola, <b>{{ session.user.username }}</b>
            <span v-if="session.user.role === 'admin'" class="badge">admin</span>
          </span>
          <button class="btn" @click="doLogout">Cerrar sesión</button>
        </template>
        <template v-else>
          <router-link class="btn ghost" to="/login">Iniciar sesión</router-link>
          <router-link class="btn" to="/register">Registrarse</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
.nav {
  background: linear-gradient(90deg, #0f172a, #111827);
  border-bottom: 1px solid #1f2937;
}
.nav__inner {
  max-width: 1100px; margin: 0 auto; padding: 14px 18px;
  display: flex; align-items: center; gap: 18px; color: #e5e7eb;
}
.brand { font-weight: 800; color: #fff; text-decoration: none; letter-spacing: .3px; }
.links { display: flex; gap: 14px; margin-left: 6px; }
.links a { color: #cbd5e1; text-decoration: none; }
.links a.router-link-active { color: #60a5fa; text-decoration: underline; }
.auth { margin-left: auto; display: flex; align-items: center; gap: 10px; }
.hello { font-size: 14px; color: #cbd5e1; }
.badge { margin-left: 6px; font-size: 11px; padding: 2px 6px; border-radius: 999px;
  color: #111827; background: #fde047; font-weight: 700; }
.btn {
  appearance: none; border: 1px solid #334155; color: #e5e7eb;
  background: #1f2937; padding: 8px 12px; border-radius: 10px;
}
.btn:hover { background: #374151; }
.btn.ghost { background: transparent; }
</style>
