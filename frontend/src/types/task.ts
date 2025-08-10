export type StatusOptions = "todo" | "done";

export interface Task {
  id: string;
  title: string;
  description: string;
  status: StatusOptions;
}
