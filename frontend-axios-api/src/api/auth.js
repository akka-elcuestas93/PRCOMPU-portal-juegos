import http from "@/services/httpBackend";

export const me = async () => (await http.get("/me")).data;
export const login = async (username, password) =>
  (await http.post("/auth/login", { username, password })).data;
export const logout = async () => (await http.post("/auth/logout")).data;
export const register = async (username, password) =>
  (await http.post("/auth/register", { username, password })).data;
