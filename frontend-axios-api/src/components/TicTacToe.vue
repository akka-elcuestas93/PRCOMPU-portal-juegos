<script setup>
import { ref, computed } from 'vue'

// Estado del tablero y turno
const board = ref(Array(9).fill(null)) // 9 casillas
const xIsNext = ref(true)               // turno actual: X empieza
const winningLine = ref([])             // índices de la línea ganadora

// Marcador
const xWins = ref(0)
const oWins = ref(0)
const draws = ref(0)

const lines = [
  [0,1,2],[3,4,5],[6,7,8], // filas
  [0,3,6],[1,4,7],[2,5,8], // columnas
  [0,4,8],[2,4,6]          // diagonales
]

const currentPlayer = computed(() => (xIsNext.value ? 'X' : 'O'))

const winner = computed(() => {
  for (const [a,b,c] of lines) {
    const v = board.value
    if (v[a] && v[a] === v[b] && v[a] === v[c]) {
      winningLine.value = [a,b,c]
      return v[a]
    }
  }
  winningLine.value = []
  return null
})

const isDraw = computed(() => !winner.value && board.value.every(Boolean))

function play(i) {
  if (board.value[i] || winner.value) return
  board.value[i] = currentPlayer.value
  xIsNext.value = !xIsNext.value

  // Actualiza marcador en el momento en que termina la partida
  if (winner.value) {
    if (winner.value === 'X') xWins.value++
    else oWins.value++
    return
  }
  if (isDraw.value) {
    draws.value++
  }
}

function resetBoard() {
  board.value = Array(9).fill(null)
  xIsNext.value = true
  winningLine.value = []
}

function resetAll() {
  xWins.value = 0
  oWins.value = 0
  draws.value = 0
  resetBoard()
}
</script>

<template>
  <section class="game">
    <div class="header">
      <h2>Tres en raya</h2>
      <div class="score">
        <span class="badge x">X: {{ xWins }}</span>
        <span class="badge o">O: {{ oWins }}</span>
        <span class="badge d">Empates: {{ draws }}</span>
      </div>
    </div>

    <div class="status" role="status" aria-live="polite">
      <template v-if="winner">🎉 Ganó <strong>{{ winner }}</strong></template>
      <template v-else-if="isDraw">🤝 Empate</template>
      <template v-else>Turno de <strong>{{ currentPlayer }}</strong></template>
    </div>

    <div class="board" role="grid" aria-label="Tablero tres en raya">
      <button
        v-for="(cell, i) in board"
        :key="i"
        class="cell"
        :class="{ win: winningLine.includes(i) }"
        role="gridcell"
        :aria-label="cell ? 'Casilla ' + i + ', ' + cell : 'Casilla ' + i + ', vacía'"
        @click="play(i)"
      >
        <span v-if="cell" class="mark" :class="cell">{{ cell }}</span>
      </button>
    </div>

    <div class="actions">
      <button class="reset" @click="resetBoard">Nueva partida</button>
      <button class="reset alt" @click="resetAll" title="Reinicia marcador y tablero">Reiniciar marcador</button>
    </div>
  </section>
</template>

<style scoped>
.game { display: grid; gap: 1rem; }
.header { display: grid; gap: .25rem; justify-items: center; }
.score { display: flex; gap: .5rem; flex-wrap: wrap; justify-content: center; }
.badge { padding: .25rem .6rem; border-radius: .6rem; font-weight: 700; border: 1px solid #e5e7eb; background: #fff; }
.badge.x { color: var(--orange); }
.badge.o { color: var(--blue); }
.badge.d { color: #6b7280; }

.status { text-align: center; font-size: 1.1rem; }

/* Tablero 3x3 grande, responsive */
.board {
  display: grid;
  grid-template-columns: repeat(3, min(24vmin, 120px));
  grid-auto-rows: min(24vmin, 120px);
  gap: .6rem;
  justify-content: center;
}

.cell {
  display: grid;
  place-items: center;
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial;
  font-weight: 700;
  font-size: clamp(2.2rem, 7vmin, 3.2rem);
  background: #fff;
  color: #111; /* color base por si falta clase */
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  box-shadow: 0 6px 20px rgba(0,0,0,.06);
  cursor: pointer;
  user-select: none;
  transition: transform .06s ease, box-shadow .2s ease, background-color .2s ease, border-color .2s ease;
}
.cell:hover { transform: translateY(-1px); box-shadow: 0 10px 24px rgba(0,0,0,.08); }
.cell:active { transform: translateY(0); }

/* Marca X/O */
.mark { line-height: 1; }
.mark.X { color: #f97316; }
.mark.O { color: #2563eb; }

/* Marca la línea ganadora en verde claro */
.cell.win { background: #dcfce7; border-color: #86efac; box-shadow: 0 0 0 3px rgba(134,239,172,.35) inset; }

.actions { display: flex; gap: .6rem; justify-content: center; }
.reset {
  padding: .7rem 1rem;
  border-radius: .8rem;
  border: 1px solid #e5e7eb;
  background: #111827; color: #fff;
  font-weight: 600; cursor: pointer;
}
.reset.alt { background: #fff; color: #111; }
.reset:hover { filter: brightness(1.05); }
</style>
