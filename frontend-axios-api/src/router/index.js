import { createRouter, createWebHistory } from "vue-router";
import { session, loadSession } from "@/stores/session";

// --- Definición de rutas ---
const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/Home.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/Register.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/games",
    name: "games",
    component: () => import("@/views/GamesView.vue"),
    meta: { requiresAuth: true }, // requiere sesión iniciada
  },
  {
    path: "/tictactoe",
    name: "tictactoe",
    component: () => import("@/components/TicTacToe.vue"),
    meta: { requiresAuth: true },
  },
  // Ruta comodín por si el usuario escribe algo inexistente
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

// --- Creación del router ---
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// --- Middleware de sesión y acceso ---
let sessionLoaded = false;

router.beforeEach(async (to, from, next) => {
  // cargar sesión solo una vez
  if (!sessionLoaded) {
    await loadSession();
    sessionLoaded = true;
  }

  const user = session.user;

  // Si la ruta requiere login y no hay usuario → redirigir a login
  if (to.meta.requiresAuth && !user) {
    return next({ name: "login" });
  }

  // Si la ruta es solo para invitados y ya hay usuario → redirigir a home
  if (to.meta.guestOnly && user) {
    return next({ name: "home" });
  }

  next();
});

export default router;
