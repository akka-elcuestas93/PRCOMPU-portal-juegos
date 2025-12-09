<script setup>
import { ref } from "vue";
import { register, login } from "@/api/auth";
import { session } from "@/stores/session";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const password2 = ref("");
const loading = ref(false);
const error = ref("");
const ok = ref(false);
const router = useRouter();

async function submit() {
  if (loading.value) return;
  error.value = "";
  ok.value = false;

  if (!username.value.trim() || !password.value || !password2.value) {
    error.value = "Rellena todos los campos.";
    return;
  }
  if (password.value !== password2.value) {
    error.value = "Las contraseñas no coinciden.";
    return;
  }
  if (password.value.length < 4) {
    error.value = "La contraseña debe tener al menos 4 caracteres.";
    return;
  }

  loading.value = true;
  try {
    await register(username.value.trim(), password.value);
    // login automático
    const { user } = await login(username.value.trim(), password.value);
    session.user = user;
    ok.value = true;
    router.push("/games");
  } catch (e) {
    error.value = e?.response?.data?.error || "No se pudo registrar.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section class="page">
    <div class="card">
      <h1>Crear cuenta</h1>
      <p class="subtitle">Únete al portal y comienza a jugar</p>

      <p v-if="error" class="alert">{{ error }}</p>
      <p v-if="ok" class="ok">Registro completado 🎉</p>

      <div class="form">
        <label>
          <span>Usuario</span>
          <input
            v-model="username"
            placeholder="Elige un usuario"
            autocomplete="username"
          />
        </label>

        <label>
          <span>Contraseña</span>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            autocomplete="new-password"
          />
        </label>

        <label>
          <span>Repite la contraseña</span>
          <input
            v-model="password2"
            type="password"
            placeholder="••••••••"
            autocomplete="new-password"
          />
        </label>

        <button :disabled="loading" @click="submit">
          {{ loading ? "Registrando…" : "Registrarse" }}
        </button>
      </div>

      <p class="footnote">
        ¿Ya tienes cuenta?
        <router-link to="/login">Inicia sesión</router-link>
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
  max-width: 480px;
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
.ok {
  background: #0a3320;
  border: 1px solid #14532d;
  color: #bbf7d0;
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
