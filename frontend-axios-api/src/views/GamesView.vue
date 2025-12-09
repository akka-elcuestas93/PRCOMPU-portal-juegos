<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import { listGames, createGame, updateGame, deleteGame } from "@/api/games";
import { session } from "@/stores/session";
import GameCard from "@/components/GameCard.vue";

const q = ref("");
const loading = ref(false);
const error = ref("");
const rows = ref([]);
const total = ref(0);
const isAdmin = computed(() => session.user?.role === "admin");

async function fetchData() {
  loading.value = true; error.value = "";
  try {
    const { items, total: t } = await listGames({ q: q.value, limit: 200, offset: 0 });
    rows.value = items;
    total.value = t;
  } catch (e) {
    error.value = e?.response?.data?.error || e.message;
  } finally { loading.value = false; }
}

onMounted(fetchData);

// --- Form admin ---
const editing = ref(false);
const form = reactive({ id:null, title:"", genre:"", url:"", image_url:"", description:"", rating:null });

function resetForm(){
  editing.value = false;
  Object.assign(form, { id:null, title:"", genre:"", url:"", image_url:"", description:"", rating:null });
}

function editRow(g){
  if (!isAdmin.value) return;
  editing.value = true; Object.assign(form, { ...g });
}

async function save(){
  if (!isAdmin.value) return;
  loading.value = true; error.value = "";
  try {
    if (editing.value && form.id) await updateGame(form.id, { ...form });
    else await createGame({ ...form });
    resetForm(); await fetchData();
  } catch (e) {
    error.value = e?.response?.data?.error || e.message;
  } finally { loading.value = false; }
}

async function removeRow(id){
  if (!isAdmin.value) return;
  if (!confirm("¿Eliminar el juego?")) return;
  loading.value = true; error.value = "";
  try { await deleteGame(id); await fetchData(); }
  catch(e){ error.value = e?.response?.data?.error || e.message; }
  finally { loading.value = false; }
}
</script>

<template>
  <section class="wrap">
    <div class="top">
      <h1>🎮 Lista de Juegos</h1>
      <div class="right">
        <input class="search" v-model="q" placeholder="Buscar por título…" @keyup.enter="fetchData" />
        <button class="btn" @click="fetchData">Buscar</button>
      </div>
    </div>

    <p v-if="!isAdmin" class="hint">Modo lectura. Inicia sesión como admin para gestionar juegos.</p>
    <p v-if="error" class="msg err">{{ error }}</p>
    <p v-if="loading" class="msg">Cargando…</p>

    <div class="grid">
      <GameCard
        v-for="g in rows"
        :key="g.id"
        :game="g"
        :isAdmin="isAdmin"
        :onEdit="editRow"
        :onDelete="removeRow"
      />
    </div>

    <div v-if="isAdmin" class="panel">
      <h2>{{ editing ? "Editar juego" : "Nuevo juego" }}</h2>
      <div class="formgrid">
        <label> Título <input v-model="form.title" /> </label>
        <label> Género <input v-model="form.genre" /> </label>
        <label> Rating <input v-model.number="form.rating" type="number" step="0.1" /> </label>
        <label> URL <input v-model="form.url" placeholder="https://… o /ruta-interna" /> </label>
        <label class="full"> Imagen (URL) <input v-model="form.image_url" placeholder="https://… o /archivo.jpg" /> </label>
        <label class="full"> Descripción <textarea v-model="form.description" rows="3"></textarea> </label>
      </div>
      <div class="actions">
        <button class="btn" @click="save">{{ editing ? "Guardar cambios" : "Crear" }}</button>
        <button class="btn ghost" @click="resetForm">Limpiar</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.wrap { max-width: 1100px; margin: 0 auto; padding: 22px 18px; color:#e5e7eb; }
.top { display:flex; align-items:center; gap: 16px; }
.top h1 { font-size: 24px; margin: 0; }
.right { margin-left: auto; display:flex; gap:8px; }
.search { width: 260px; padding: 9px 12px; border-radius: 10px; border:1px solid #334155; background:#0b1220; color:#e5e7eb; }
.btn { border:1px solid #334155; background:#1f2937; color:#e5e7eb; padding:8px 12px; border-radius:10px; }
.btn:hover { background:#374151; }
.btn.ghost { background:transparent; }
.hint { color:#94a3b8; margin: 8px 0 10px; }
.msg { color:#9ca3af; margin: 8px 0 16px; }
.msg.err { color:#fca5a5; }
.grid { margin-top: 10px; display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:16px; }

.panel { margin-top: 22px; border:1px solid #1f2937; background:#0b1020; border-radius: 14px; padding: 16px; }
.panel h2 { margin: 0 0 10px; }
.formgrid { display:grid; grid-template-columns: 1fr 1fr; gap:12px; }
.formgrid label { display:flex; flex-direction:column; gap:6px; font-size: 14px; }
.formgrid input, .formgrid textarea {
  border:1px solid #334155; background:#0b1220; color:#e5e7eb; border-radius:10px; padding:8px 10px;
}
.full { grid-column: 1 / -1; }
.actions { margin-top: 12px; display:flex; gap:10px; }
</style>
