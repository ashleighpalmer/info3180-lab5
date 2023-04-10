<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>All Movies</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-md-4 mb-3" v-for="movie in movies" :key="movie.id">
        <div class="card">
          <img :src="movie.poster" class="card-img-top" alt="Movie Poster">
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies() {
  fetch("/api/v1/movies")
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(data => {
      movies.value = data.movies;
    })
    .catch(error => {
      console.log(error);
      // handle error here, e.g. display error message to user
    });
}

onMounted(() => {
  fetchMovies();
});
</script>
