export type StatusOptions = 'todo' | 'done'

export interface Task {
  id: number
  title: string
  description: string
  status: StatusOptions
}
