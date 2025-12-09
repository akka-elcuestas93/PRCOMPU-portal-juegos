import http from "@/services/httpBackend";

export async function listGames({ q = "", limit = 50, offset = 0 } = {}) {
  return (await http.get("/games", { params: { q, limit, offset } })).data;
}
export async function createGame(payload) { return (await http.post("/games", payload)).data; }
export async function updateGame(id, payload) { return (await http.patch(`/games/${id}`, payload)).data; }
export async function deleteGame(id) { return (await http.delete(`/games/${id}`)).data; }
