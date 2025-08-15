import { useAuth } from "@/composables/useAuth";
import {
  createRouter,
  createWebHistory,
  type NavigationGuard,
} from "vue-router";
import { routes } from "vue-router/auto-routes";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const authGuard: NavigationGuard = async (to) => {
  const { isAuthenticated } = useAuth();
  const authStatus = await isAuthenticated();

  if (to.name === "/Tasks" && !authStatus) {
    return {
      path: "/",
    };
  }
  return undefined;
};

router.beforeEach(authGuard);

export default router;
