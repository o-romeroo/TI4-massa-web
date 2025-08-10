<template>
  <div class="content-banner"> 
    <div class="container">
      <div class="gradient-overlay">
        <div class="text-overlay">
          <h1 v-if="title" class="title">{{ title }}</h1>
          <p v-if="description" class="description">
            <small>{{ description }}</small>
          </p>
          <v-btn v-if="buttonText" @click="onClick" class="button" max-width="200">{{ buttonText }}</v-btn>
        </div>
      </div>
      <img src="../assets/banner.png" alt="background image">
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

defineProps({
  title: String,
  description: String,
  buttonText: String
})

const emit = defineEmits(["buttonClicked"])

function onClick() {
  emit("buttonClicked");
}
</script>

<style scoped>
.content-banner {
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items: start;
  width: 100vw;
}

.container {
  position: relative; 
  width: 100vw;
  min-height: 250px; 
  overflow: hidden; 
}

.text-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-height: 100%; 
  overflow: hidden; 
  text-overflow: ellipsis; 
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(71, 115, 143, 0.9) 0%, rgba(1, 24, 38, 0.9) 75%);
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.title {
  font-size: 2.3rem;
  color: #fff;
}

.description {
  color: #fff;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}

.button {
  background-color: #fff;
  color: #062033;
  font-weight: bold;
  font-size: 0.9rem;
  padding: 1.2rem 2rem;
  border-radius: 5px;
  line-height: 0;
}
</style>