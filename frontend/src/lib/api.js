const BASE_URL = 'http://localhost:8000';

export async function getPosts() {
  const res = await fetch(`${BASE_URL}/posts`);
  return res.json();
}

export async function createPost(token, content, link) {
  const res = await fetch(`${BASE_URL}/posts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ content, link })
  });

  return res.json();
}

export async function vote(token, post_id, direction) {
  const res = await fetch(`${BASE_URL}/vote`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ post_id, direction })
  });

  return res.json();
}