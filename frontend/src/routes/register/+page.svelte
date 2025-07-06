<script>
  import { goto } from '$app/navigation';
  

  let username = '';
  let password = '';

  async function register() {
    const res = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (res.ok) {
      alert('Registration successful!');
      goto('/login');
    } else {
      const data = await res.json();
      alert('Error: ' + data.detail);
    }
  }
</script>

<h1>Register</h1>
<input bind:value={username} placeholder="Username" />
<input bind:value={password} placeholder="Password" type="password" />
<button on:click={register}>Register</button>