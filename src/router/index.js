import { createRouter, createWebHashHistory } from 'vue-router'

// 路由配置
const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { titleKey: 'routes.dashboard', icon: 'dashboard' }
  },
  {
    path: '/realtime',
    name: 'Realtime',
    component: () => import('../views/Realtime.vue'),
    meta: { titleKey: 'routes.realtime', icon: 'monitor' }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue'),
    meta: { titleKey: 'routes.history', icon: 'history' }
  },
  {
    path: '/annotation',
    name: 'Annotation',
    component: () => import('../views/Annotation.vue'),
    meta: { titleKey: 'routes.annotation', icon: 'edit' }
  },
  {
    path: '/model',
    name: 'Model',
    component: () => import('../views/Model.vue'),
    meta: { titleKey: 'routes.model', icon: 'model_training' }
  },
  {
    path: '/model/test/:id',
    name: 'ModelTest',
    component: () => import('../views/Model.vue'),
    props: route => ({
      mode: 'test',
      modelId: parseInt(route.params.id)
    }),
    meta: { titleKey: 'routes.modelTest', parent: 'Model' }
  },
  {
    path: '/cv-operations',
    name: 'CVOperations',
    component: () => import('../views/CVOperation.vue'),
    meta: { titleKey: 'routes.cvOperations', icon: 'science' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { titleKey: 'routes.settings', icon: 'settings' }
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { titleKey: 'routes.notFound' }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router