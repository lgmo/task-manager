<script lang="ts" setup>
  import type { StatusOptions, Task } from '../types/task'
  import { onMounted, ref, type Ref } from 'vue'
  import { useTasks } from '../composables/useTasks'

  const { tasks, statusOptions, loadTasks, addTask, removeTask, updateTask } = useTasks()

  const newTask: Ref<Task> = ref({ title: '', description: '', status: 'todo' } as Task)
  const selectedTask = ref<Task | null>(null)
  const editDialog = ref(false)

  const openEditDialog = (task: Task) => {
    selectedTask.value = { ...task }
    editDialog.value = true
  }

  onMounted(() => {
    loadTasks()
  })

  function handleCreateTask () {
    addTask(newTask.value)
  }

  function handleDelete () {
    if (!selectedTask.value) return
    removeTask(selectedTask.value.id)
    editDialog.value = false
  }

  function handleUpdate () {
    if (!selectedTask.value) return
    updateTask(selectedTask.value)
    editDialog.value = false
  }

  function statusClass (status: string) {
    if (status === 'done') {
      return 'bg-primary text-white'
    }
    return ''
  }
</script>

<template>
  <v-card>
    <v-card-title>
      <h1>My tasks</h1>
    </v-card-title>
    <v-card-text>
      <v-form @submit.prevent="handleCreateTask">
        <v-text-field v-model="newTask.title" label="Title" required />
        <v-text-field
          v-model="newTask.description"
          label="Description"
          required
        />
        <v-select
          v-model="newTask.status"
          dense
          :items="statusOptions"
          label="Status"
          outlined
        />
        <v-btn color="primary" type="submit">Add</v-btn>
      </v-form>
      <v-card class="mt-6 pa-4" elevation="4" width="100%">
        <v-card-title class="text-h6 font-weight-medium mb-2">
          Task List
        </v-card-title>

        <v-divider class="mb-3" />

        <v-list v-if="tasks.length > 0" lines="two">
          <v-list-item
            v-for="task in tasks"
            :key="task.id"
            class="mb-2 rounded"
            :class="statusClass(task.status)"
            :value="task"
            variant="tonal"
            @click="openEditDialog(task)"
          >
            <v-list-item-title class="font-weight-bold">
              {{ task.title }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ task.description }}
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>

        <v-alert v-else class="mt-3" type="info" variant="tonal">
          Nenhuma tarefa encontrada.
        </v-alert>
      </v-card>

    </v-card-text>
  </v-card>

  <v-dialog v-model="editDialog" max-width="500">
    <v-card>
      <v-card-title class="text-h6 font-weight-medium">
        Editar Tarefa
      </v-card-title>
      <v-card-text v-if="selectedTask">
        <v-text-field
          v-model="selectedTask.title"
          label="Title"
          required
        />
        <v-text-field
          v-model="selectedTask.description"
          label="Description"
          required
        />
        <v-select
          v-model="selectedTask.status"
          :items="statusOptions"
          label="Status"
          variant="outlined"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="editDialog = false">Cancelar</v-btn>
        <v-btn color="primary" @click="handleUpdate">Salvar</v-btn>
        <v-btn color="red" @click="handleDelete">Remover</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
