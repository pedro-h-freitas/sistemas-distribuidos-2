import { 
  apiDelete,
  apiGet,
  apiPatch,
  apiPost,
  apiPut
} from "../lib/api";

export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const USERS_URL = `${API_URL}/users`;


export function listUsers() {
  return apiGet(USERS_URL);
}


export function getUser(userId) {
  return apiGet(`${USERS_URL}/${userId}`);
}


export function createUser(body) {
  return apiPost(`${USERS_URL}`, body);
}


export function updateUserRoles(userId, body) {
  return apiPut(`${USERS_URL}/${userId}/roles`, body);
}


export function updateUser(body) {
  return apiPatch(`${USERS_URL}/${userId}`, body);
}


export function deleteUser(userId) {
  return apiDelete(`${USERS_URL}/${userId}`);
}
