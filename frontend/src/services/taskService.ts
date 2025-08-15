import type { Task } from "@/types/task.ts";

import api from "@/api/client.ts";

export async function fetchTasks() {
  return api.get<Task[]>("/tasks/").then((res) => res.data);
}

export async function createTask(task: Omit<Task, "id">) {
  return api.post("/tasks/", task).then((res) => res.data);
}

export async function updateTask(id: string, task: Omit<Task, "id">) {
  return api.patch(`/tasks/${id}/`, task).then((res) => res.data);
}

export async function deleteTask(id: string) {
  return api.delete(`/tasks/${id}/`);
}
