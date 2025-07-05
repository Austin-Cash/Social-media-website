import { writable } from 'svelte/store';

export const token = writable(
  typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null
);

token.subscribe((value) => {
  if (typeof localStorage !== 'undefined') {
    if (value) {
      localStorage.setItem('token', value);
    } else {
      localStorage.removeItem('token');
    }
  }
});

export const username = writable(
  typeof localStorage !== 'undefined' ? localStorage.getItem('username') : ''
);

username.subscribe((value) => {
  if (typeof localStorage !== 'undefined') {
    if (value) {
      localStorage.setItem('username', value);
    } else {
      localStorage.removeItem('username');
    }
  }
});