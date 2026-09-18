import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import AcademicCalendar from '../views/AcademicCalendar.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/academic-calendar',
    name: 'AcademicCalendar',
    component: AcademicCalendar
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
