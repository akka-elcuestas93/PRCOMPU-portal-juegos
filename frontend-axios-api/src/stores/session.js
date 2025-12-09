// src/stores/session.js
import { reactive } from "vue";
import { me } from "@/api/auth";

export const session = reactive({ user: null, ready: false });

export async function loadSession() {
  try {
    const { user } = await me();
    session.user = user;
  } finally {
    session.ready = true;
  }
}
