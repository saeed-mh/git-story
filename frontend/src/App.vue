<template>
  <div class="container">
    <header>
      <h1>📖 Git Story</h1>
      <p>Turn any GitHub repository into a human story.</p>
    </header>

    <div class="input-section">
      <input
        v-model="githubUrl"
        type="text"
        placeholder="https://github.com/username/repo"
        @keyup.enter="generateStory"
      />
      <button @click="generateStory" :disabled="loading">
        {{ loading ? "Generating..." : "Generate Story" }}
      </button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="loading" class="loader">
      <div class="spinner"></div>
      <p>{{ loadingMessage }}</p>
    </div>

    <div v-if="story" class="story">
      <div class="story-header">
        <h2>{{ story.repo }}</h2>
        <span
          >{{ story.total_commits }} commits ·
          {{ story.total_chapters }} chapters</span
        >
      </div>

      <div v-for="chapter in story.story" :key="chapter.month" class="chapter">
        <div class="chapter-meta">
          <h3>{{ chapter.month }}</h3>
          <span>{{ chapter.total_commits }} commits</span>
        </div>
        <p>{{ chapter.narrative }}</p>
        <div class="authors">
          <span
            v-for="author in chapter.top_authors"
            :key="author.name"
            class="author"
          >
            {{ author.name }} ({{ author.commits }})
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const githubUrl = ref("");
const loading = ref(false);
const error = ref("");
const story = ref(null);
const loadingMessage = ref('')  // ← add this

const loadingMessages = [
  'Cloning repository...',
  'Extracting commits...',
  'Grouping into chapters...',
  'Generating narrative...',
  'Almost there...',
]

let messageInterval = null  // ← add this


async function generateStory() {
  if (!githubUrl.value.trim()) return

  loading.value = true
  error.value = ''
  story.value = null
  loadingMessage.value = loadingMessages[0]

  // Cycle through messages every 4 seconds
  let i = 0
  messageInterval = setInterval(() => {
    i = (i + 1) % loadingMessages.length
    loadingMessage.value = loadingMessages[i]
  }, 4000)

  try {
    const response = await fetch('http://localhost:8000/story', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ github_url: githubUrl.value })
    })

    const data = await response.json()
    if (!response.ok) throw new Error(data.detail)
    story.value = data

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
    clearInterval(messageInterval)
  }
}

</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

header p {
  color: #888;
  font-size: 1.1rem;
}

.input-section {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

input {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #333;
  background: #1a1a1a;
  color: #e0e0e0;
  font-size: 1rem;
  outline: none;
}

input:focus {
  border-color: #555;
}

button {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  background: #e0e0e0;
  color: #0f0f0f;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  color: #ff6b6b;
  font-size: 0.9rem;
}

.story-header {
  margin: 2rem 0 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #222;
}

.story-header h2 {
  font-size: 1.2rem;
  margin-bottom: 0.25rem;
}

.story-header span {
  color: #888;
  font-size: 0.9rem;
}

.chapter {
  padding: 1.5rem 0;
  border-bottom: 1px solid #1a1a1a;
}

.chapter-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.chapter-meta h3 {
  font-size: 1rem;
  color: #e0e0e0;
}

.chapter-meta span {
  color: #555;
  font-size: 0.85rem;
}

.chapter p {
  color: #bbb;
  line-height: 1.7;
  margin-bottom: 0.75rem;
}

.authors {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.author {
  font-size: 0.8rem;
  padding: 0.2rem 0.6rem;
  background: #1a1a1a;
  border-radius: 20px;
  color: #888;
}



.loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 0;
  color: #888;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #222;
  border-top-color: #e0e0e0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
