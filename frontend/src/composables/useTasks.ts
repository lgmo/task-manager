// composables/useTasks.ts
import type { StatusOptions, Task } from '@/types/task'
import { ref } from 'vue'
import * as taskService from '../services/taskService'

export function useTasks () {
  const tasks = ref<Task[]>([])
  const statusOptions: StatusOptions[] = ['todo', 'done']

  async function loadTasks () {
    tasks.value = await taskService.fetchTasks()
  }

  async function addTask (newTask: Omit<Task, 'id'>) {
    const task = await taskService.createTask(newTask)
    tasks.value.push(task)
  }

  async function removeTask (id: number) {
    await taskService.deleteTask(id)
    tasks.value = tasks.value.filter(t => t.id !== id)
  }

  async function updateTask (updatedTask: Task) {
    const task = await taskService.updateTask(updatedTask.id, updatedTask)
    const index = tasks.value.findIndex(t => t.id === task.id)
    if (index !== -1) {
      tasks.value[index] = task
    }
  }

  return {
    tasks,
    statusOptions,
    loadTasks,
    addTask,
    removeTask,
    updateTask,
  }
}
