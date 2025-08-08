import { createRouter, createWebHistory } from "vue-router";
import { routes } from "vue-router/auto-routes";

// const customRoutes = [
//   {
//     path: '/tasks',
//     name: 'Tasks',
//     component: TasksList,
//   },
// ]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // customRoutes,
});

export default router;
