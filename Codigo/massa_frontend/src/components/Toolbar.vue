<template>
  <RouterView>
    <v-toolbar-title>

      <div style="align-items: center; display: flex">
        <img src="../assets/logo_massa.svg" alt="Logo" width="max-content" />
        <div class="conjuntoTitlesMassa">
          <h1 class="titleMassa">{{ title1 }}</h1>
          <h4 class="titleMassa2">{{ title2 }}</h4>
        </div>
      </div>

      
    </v-toolbar-title>

    <v-toolbar-items class="hidden-sm-and-down">

      <v-btn variant="plain" to="/"><p style="color: black">Home</p></v-btn>
      <v-btn variant="plain" to="/teste"><p style="color: black">Teste</p></v-btn>
      <v-btn variant="plain" to="/algorithm"><p style="color: black">Algorithm</p></v-btn>
      <v-btn variant="plain" to="/about"><p style="color: black">About</p></v-btn>
      <v-btn variant="plain" to="/support"><p style="color: black">Support</p></v-btn>

    </v-toolbar-items>
  </RouterView>
</template>

<style>
</style>

<script>
export default {
  name: "Toolbar",
  props: {
    title1: String,
    title2: String,
    redirects: Array,
  },
};
</script>

