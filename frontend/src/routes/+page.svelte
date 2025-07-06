<script>
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';

  import { token, username } from '$lib/store';
  import { getPosts, createPost, vote } from '$lib/api';
  

  let posts = [];
  let content = '';
  let link = '';
  let error = '';

  // Load posts when component mounts
  async function loadPosts() {
    posts = await getPosts();
  }

  // Submit a new post
  async function submitPost() {
    const currentToken = get(token);
    if (!currentToken) {
      error = 'You must be logged in to post.';
      return;
    }

    const res = await createPost(currentToken, content, link);
    if (res.msg) {
      content = '';
      link = '';
      error = '';
      await loadPosts();
    } else {
      error = res.detail || 'Post failed.';
    }
  }

  // Cast vote on a post
  async function castVote(id, dir) {
    const currentToken = get(token);
    if (!currentToken) {
      error = 'Login required to vote.';
      return;
    }

    const res = await vote(currentToken, id, dir);
    if (res.msg) {
      await loadPosts();
    } else {
      error = res.detail || 'Vote failed.';
    }
  }

  // Handle logout
  function logout() {
    token.set(null);
    username.set('');
    goto('/login');
  }

  async function deletePost(id) {
  const currentToken = get(token);
  if (!currentToken) {
    error = 'Login required to delete.';
    return;
  }

  const res = await fetch(`http://localhost:8000/posts/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${currentToken}`
    }
  });

  const data = await res.json();
  if (res.ok) {
    await loadPosts(); // refresh post list
  } else {
    error = data.detail || 'Delete failed.';
  }
}

  onMount(loadPosts);
</script>

<h1>Community Feed</h1>


{#if $token}
  <p>Welcome, {$username}! <button on:click={logout}>Logout</button></p>

  <form on:submit|preventDefault={submitPost}>
    <input type="text" bind:value={content} placeholder="Say something..." required />
    <input type="url" bind:value={link} placeholder="Optional link" />
    <button type="submit">Post</button>
  </form>
{:else}
  <p><a href="/login">Login</a> or <a href="/register">Register</a> to post or vote.</p>
{/if}

{#if error}
  <p style="color: red;">{error}</p>
{/if}

<ul>
  

    {#each posts as post}
  <div class="post">
    <div class="vote-column">
      <button on:click={() => castVote(post.id, 1)}>⬆️</button>
      <div>{post.votes}</div>
      <button on:click={() => castVote(post.id, -1)}>⬇️</button>
    </div>
    <div class="post-content">
      <p>{post.content}</p>
      {#if post.link}
        <a href={post.link} target="_blank">{post.link}</a>
      {/if}
      {#if $username === post.owner}
        <button on:click={() => deletePost(post.id)}>🗑️ Delete</button>
      {/if}
    </div>
  </div>
{/each}


</ul>