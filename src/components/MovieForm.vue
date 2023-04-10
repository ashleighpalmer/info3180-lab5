<template>
  <form @submit.prevent="saveMovie" id="movieForm">
    <div class="form-group mb-3">
      <label for="title" class="form-label">Movie Title</label>
      <input type="text" name="title" class="form-control" v-model="movie.title" />
    </div>
    <div class="form-group mb-3">
      <label for="poster" class="form-label">Movie Poster</label>
      <input type="file" name="poster" class="form-control" ref="posterInput" @change="onPosterChange" />
    </div>
    <div class="form-group mb-3">
      <label for="description" class="form-label">Movie Description</label>
      <textarea name="description" class="form-control" v-model="movie.description"></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Save Movie</button>
  </form>
</template>
<script setup>
import { ref, onMounted } from 'vue'

let csrf_token = ref('')
const movie = ref({
  title: '',
  poster: null,
  description: ''
})
const formErrors = ref([])

function saveMovie() {
  const formData = new FormData()
  formData.append('title', movie.value.title)
  formData.append('poster', movie.value.poster)
  formData.append('description', movie.value.description)

  let movieForm = document.getElementById('movieForm');
  let form_data = new FormData(movieForm);

  fetch('/api/v1/movies', {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      return response.json()
    })
    .then(data => {
      console.log(data)
      // display success message
    })
    .catch(error => {
      console.log(error)
      // display error message
    })
}


function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      return response.json()
    })
    .then(data => {
      csrf_token.value = data.csrf_token
    })
    .catch(error => {
      console.log(error)
      // handle error here, e.g. display error message to user
    })
}


onMounted(() => {
  getCsrfToken()
})
</script>