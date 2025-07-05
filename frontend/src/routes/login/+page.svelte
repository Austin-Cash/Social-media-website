<script>
  import { goto } from '$app/navigation';
  import { token, username as usernameStore } from '$lib/store';

  let username = '';
  let password = '';

  async function login() {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    });

    const data = await res.json();
    if (res.ok) {
      token.set(data.access_token);
      usernameStore.set(username);
      goto('/');
    } else {
      alert('Login failed: ' + data.detail);
    }
  }
</script>

<h1>Login</h1>
<input bind:value={username} placeholder="Username" />
<input bind:value={password} type="password" placeholder="Password" />
<button on:click={login}>Login</button>