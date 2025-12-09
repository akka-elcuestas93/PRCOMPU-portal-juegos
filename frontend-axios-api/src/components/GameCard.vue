<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
  game: { type: Object, required: true },
  isAdmin: { type: Boolean, default: false },
  onEdit: { type: Function, default: null },
  onDelete: { type: Function, default: null },
  // nuevo: bloquear la tarjeta (p.ej., si no hay sesión y no está en el top-4)
  locked: { type: Boolean, default: false },
  lockTo: { type: String, default: "/login" },
});

const router = useRouter();
const isInternal = computed(() => typeof props.game.url === "string" && props.game.url.startsWith("/"));

function open() {
  if (props.locked) {
    router.push(props.lockTo);
    return;
  }
  if (!props.game.url) return;
  if (isInternal.value) router.push(props.game.url);
  else window.open(props.game.url, "_blank");
}
</script>

<template>
  <article class="card">
    <div class="thumb" @click="open">
      <img v-if="game.image_url" :src="game.image_url" alt="">
      <div v-else class="noimg">Sin imagen</div>

      <!-- Overlay de bloqueo -->
      <div v-if="locked" class="lock" title="Inicia sesión para jugar">🔒</div>
    </div>

    <div class="body">
      <h3 class="title" :title="game.title">{{ game.title }}</h3>
      <p class="meta">
        <span>{{ game.genre || "Indie" }}</span>
        <span v-if="game.rating != null">• ⭐ {{ game.rating }}</span>
      </p>

      <div class="actions">
        <button class="pill" @click="open">
          {{ locked ? "Iniciar sesión" : (game.url ? "Jugar" : "Sin enlace") }}
        </button>

        <div class="right" v-if="isAdmin && onEdit && onDelete">
          <button class="icon" @click="onEdit(game)" title="Editar">✏️</button>
          <button class="icon danger" @click="onDelete(game.id)" title="Borrar">🗑️</button>
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.card {
  background: #0f172a; border: 1px solid #1f2937; border-radius: 14px; overflow: hidden;
  display: flex; flex-direction: column; box-shadow: 0 6px 24px rgba(0,0,0,.25);
}
.thumb { position: relative; height: 160px; background:#111827; display:flex; align-items:center; justify-content:center; cursor: pointer; }
.thumb img { width:100%; height:100%; object-fit: cover; }
.noimg { color:#9ca3af; font-size: 14px; }
.lock {
  position: absolute; top: 10px; right: 10px; font-size: 18px;
  background: rgba(2,6,23,.7); border: 1px solid #334155; padding: 6px 8px; border-radius: 10px;
}
.body { padding: 12px 14px; color: #e5e7eb; }
.title { margin: 0 0 6px; font-size: 18px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.meta { margin: 0 0 10px; font-size: 13px; color: #9ca3af; }
.actions { display:flex; align-items:center; justify-content: space-between; }
.pill {
  border: 1px solid #334155; background: #1f2937; color:#e5e7eb; padding: 6px 12px; border-radius: 999px;
}
.pill:hover { background: #374151; }
.right { display:flex; gap:8px; }
.icon {
  border: 1px solid #334155; background: #0b1220; color:#e5e7eb; padding: 6px 8px; border-radius: 8px;
}
.icon:hover { background: #1f2937; }
.icon.danger:hover { background: #3b0d12; border-color:#7f1d1d; }
</style>
