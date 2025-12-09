<script setup>
import { ref } from "vue";
import { login } from "@/api/auth";
import { session } from "@/stores/session";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");
const router = useRouter();

async function submit() {
  if (loading.value) return;
  error.value = "";

  if (!username.value.trim() || !password.value) {
    error.value = "Introduce usuario y contraseña.";
    return;
  }

  loading.value = true;
  try {
    const { user } = await login(username.value.trim(), password.value);
    session.user = user;
    router.push("/games");
  } catch (e) {
    error.value = e?.response?.data?.error || "Credenciales inválidas.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section class="page">
    <div class="card">
      <h1>Iniciar sesión</h1>
      <p class="subtitle">Accede a tu biblioteca de juegos</p>

      <p v-if="error" class="alert">{{ error }}</p>

      <div class="form">
        <label>
          <span>Usuario</span>
          <input
            v-model="username"
            placeholder="Tu usuario"
            @keyup.enter="submit"
            autocomplete="username"
          />
        </label>

        <label>
          <span>Contraseña</span>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            @keyup.enter="submit"
            autocomplete="current-password"
          />
        </label>

        <button :disabled="loading" @click="submit">
          {{ loading ? "Entrando…" : "Entrar" }}
        </button>
      </div>

      <p class="footnote">
        ¿No tienes cuenta?
        <router-link to="/register">Regístrate</router-link>
      </p>
    </div>
  </section>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background:
    radial-gradient(900px 300px at 10% -10%, #1f2937 0, transparent 70%),
    linear-gradient(180deg, #0b1020, #0a0f1c);
  color: #e5e7eb;
}
.card {
  width: 100%;
  max-width: 440px;
  background: #0f172a;
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 26px 22px;
  box-shadow: 0 14px 38px rgba(0,0,0,.35);
}
h1 { margin: 0 0 6px; font-size: 28px; }
.subtitle { margin: 0 0 16px; color: #94a3b8; }
.form { display: grid; gap: 12px; }
label { display: grid; gap: 6px; font-size: 14px; }
input {
  border: 1px solid #334155;
  background: #0b1220;
  color: #e5e7eb;
  border-radius: 10px;
  padding: 10px 12px;
}
input:focus { outline: none; border-color: #60a5fa; box-shadow: 0 0 0 3px rgba(96,165,250,.15); }
button {
  margin-top: 6px;
  border: 1px solid #334155;
  background: #1f2937;
  color: #e5e7eb;
  padding: 10px 12px;
  border-radius: 12px;
  font-weight: 600;
}
button:hover { background: #374151; }
button:disabled { opacity: .7; cursor: default; }
.alert {
  background: #3b0d12;
  border: 1px solid #7f1d1d;
  color: #fecaca;
  padding: 10px 12px;
  border-radius: 10px;
  margin: 6px 0 10px;
  font-size: 14px;
}
.footnote {
  margin-top: 12px;
  color: #9ca3af;
  font-size: 14px;
  text-align: center;
}
.footnote a { color: #93c5fd; }
</style>
