<script setup>
import { ref, onMounted } from "vue";
import { listGames } from "@/api/games";
import { session } from "@/stores/session";
import GameCard from "@/components/GameCard.vue";

const items = ref([]);
const loading = ref(false);
const error = ref("");

async function fetchFew() {
  loading.value = true; error.value = "";
  try {
    const { items: data } = await listGames({ limit: 12, offset: 0 });
    // No inyectamos nada local. Si hay tictactoe en BD, saldrá; si no, no.
    items.value = data;
  } catch (e) {
    error.value = e?.response?.data?.error || e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(fetchFew);
</script>

<template>
  <section class="wrap">
    <div class="hero">
      <h1>🎮 Bienvenido al Portal de Juegos</h1>
      <p>Explora, juega y descubre nuevos desafíos.</p>
      <div class="cta" v-if="!session.user">
        <router-link class="btn" to="/login">Iniciar sesión</router-link>
        <router-link class="btn ghost" to="/register">Registrarse</router-link>
      </div>
    </div>

    <h2 class="h2">Juegos destacados</h2>

    <div v-if="error" class="msg err">{{ error }}</div>
    <div v-if="loading" class="msg">Cargando juegos…</div>

    <div v-if="!loading" class="grid">
      <!-- Si NO hay sesión, sólo los 4 primeros son jugables; el resto se bloquea -->
      <GameCard
        v-for="(g, idx) in items"
        :key="g.id"
        :game="g"
        :locked="!session.user && idx >= 4"
        lock-to="/login"
      />
    </div>
  </section>
</template>

<style scoped>
.wrap { max-width: 1100px; margin: 0 auto; padding: 22px 18px; color:#e5e7eb; }
.hero { background: radial-gradient(1200px 400px at 10% -10%, #1f2937, transparent),
                   linear-gradient(180deg,#0b1020,#0a0f1c);
        border:1px solid #1f2937; border-radius:18px; padding:28px; margin-bottom:22px; }
.hero h1 { margin:0 0 6px; font-size: 34px; }
.hero p { margin:0 0 14px; color:#cbd5e1; }
.cta { display:flex; gap:10px; }
.btn { border:1px solid #334155; background:#1f2937; color:#e5e7eb; padding:10px 14px; border-radius: 12px; text-decoration:none; }
.btn:hover { background:#374151; }
.btn.ghost { background:transparent; }
.h2 { margin: 14px 0; font-size: 22px; }
.grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:16px; }
.msg { color:#9ca3af; margin: 8px 0 16px; }
.msg.err { color:#fca5a5; }
</style>
