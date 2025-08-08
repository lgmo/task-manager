import type { Task } from '@/types/task.ts'
// services/taskService.ts
import api from '../api/client.ts'

export async function fetchTasks () {
  return api.get<Task[]>('/tasks/').then(res => res.data)
}

export async function createTask (task: Omit<Task, 'id'>) {
  return api.post('/tasks/', task).then(res => res.data)
}

export async function updateTask (id: number, task: Omit<Task, 'id'>) {
  return api.put(`/tasks/${id}/`, task).then(res => res.data)
}

export async function deleteTask (id: number) {
  return api.delete(`/tasks/${id}/`)
}
