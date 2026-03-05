const API_URL = 'http://localhost:3000';

async function test() {
  console.log('--- N+1 Problem ---');
  let requests = 0;
  
  const postsRes = await fetch(`${API_URL}/posts`);
  const posts = await postsRes.json();
  requests++;

  for (const post of posts) {
     const userRes = await fetch(`${API_URL}/users/${post.userId}`);
     const user = await userRes.json();
     requests++;
     console.log(`[Bad] Post ${post.id}: ${post.title} (by ${user.name})`);
  }
  console.log(`Total requests: ${requests}\n`);

  console.log('--- Eager Loading ---');
  const optimizedRes = await fetch(`${API_URL}/posts?_expand=user`);
  const optimizedPosts = await optimizedRes.json();
  
  for (const post of optimizedPosts) {
      console.log(`[Good] Post ${post.id}: ${post.title} (by ${post.user.name})`);
  }
  console.log('Total requests: 1');
}

test().catch(console.error);
