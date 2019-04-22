import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Airbnb from '@/components/Airbnb';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/airbnb',
      name: 'airbnb',
      component: Airbnb,
    },
  ],
  mode: 'history',
});
