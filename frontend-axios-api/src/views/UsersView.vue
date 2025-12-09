<script setup>
import { ref, onMounted } from "vue";
import { http } from "@/services/http";

const users = ref([]);
const newUser = ref({
  firstName: "",
  lastName: "",
  age: "",
  email: "",
});

const loading = ref(false);
const error = ref("");

// Obtener lista de usuarios desde DummyJSON
async function fetchUsers() {
  loading.value = true;
  error.value = "";
  try {
    const { data } = await http.get("/users?limit=10");
    users.value = data.users;
  } catch (e) {
    error.value = e?.response?.data?.error || e.message;
  } finally {
    loading.value = false;
  }
}

// Crear un usuario nuevo en DummyJSON (no persistente, pero sirve como prueba)
async function addUser() {
  if (!newUser.value.firstName || !newUser.value.lastName) {
    alert("Por favor, completa nombre y apellidos");
    return;
  }
  loading.value = true;
  try {
    const { data } = await http.post("/users/add", newUser.value);
    users.value.unshift(data); // Añadir al principio de la lista
    newUser.value = { firstName: "", lastName: "", age: "", email: "" };
  } catch (e) {
    error.value = e?.response?.data?.error || e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(fetchUsers);
</script>

<template>
  <section class="p-6 max-w-5xl mx-auto text-white">
    <h1 class="text-3xl font-bold mb-4">👥 Usuarios (DummyJSON API)</h1>

    <p v-if="error" class="text-red-400 mb-4">{{ error }}</p>

    <!-- Formulario -->
    <div class="border border-gray-700 rounded p-4 mb-6 bg-[#181818]">
      <h2 class="font-semibold mb-3 text-lg">Añadir usuario de prueba</h2>
      <div class="grid grid-cols-2 gap-3">
        <input
          v-model="newUser.firstName"
          placeholder="Nombre"
          class="border border-gray-600 bg-[#222] rounded px-2 py-1"
        />
        <input
          v-model="newUser.lastName"
          placeholder="Apellidos"
          class="border border-gray-600 bg-[#222] rounded px-2 py-1"
        />
        <input
          v-model="newUser.age"
          type="number"
          placeholder="Edad"
          class="border border-gray-600 bg-[#222] rounded px-2 py-1"
        />
        <input
          v-model="newUser.email"
          type="email"
          placeholder="Correo electrónico"
          class="border border-gray-600 bg-[#222] rounded px-2 py-1"
        />
      </div>
      <button
        class="mt-4 border border-gray-600 rounded px-3 py-2 bg-[#333] hover:bg-[#444]"
        @click="addUser"
        :disabled="loading"
      >
        {{ loading ? "Añadiendo..." : "Añadir usuario" }}
      </button>
    </div>

    <!-- Tabla -->
    <div v-if="loading" class="text-gray-400">Cargando usuarios...</div>

    <table
      v-if="!loading && users.length"
      class="w-full border border-gray-700 text-sm text-left bg-[#1A1A1A]"
    >
      <thead class="bg-[#222] text-gray-300">
        <tr>
          <th class="border border-gray-700 p-2">ID</th>
          <th class="border border-gray-700 p-2">Nombre</th>
          <th class="border border-gray-700 p-2">Edad</th>
          <th class="border border-gray-700 p-2">Email</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id" class="hover:bg-[#2A2A2A]">
          <td class="border border-gray-700 p-2">{{ u.id }}</td>
          <td class="border border-gray-700 p-2">{{ u.firstName }} {{ u.lastName }}</td>
          <td class="border border-gray-700 p-2">{{ u.age }}</td>
          <td class="border border-gray-700 p-2">{{ u.email }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="!loading && !users.length" class="text-gray-400">
      No se encontraron usuarios.
    </p>
  </section>
</template>
