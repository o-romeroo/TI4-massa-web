<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <v-card class="d-flex flex-column align-center pa-6 relative" outlined>
          <v-btn icon @click="$emit('click')" class="absolute top-0 right-0" variant="plain">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <img :src="imageUrl" alt="File type image" style="max-height: 100px; max-width: 100px" />

          <div class="text-center font-weight-medium">
            {{ name }}
            <p>({{ formatFileSize(size) }})</p>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
  name: String,
  size: Number
});

const emit = defineEmits(["click"]);

const getType = (name) => {
  return name.split('.').pop().toLowerCase();
};

const formatFileSize = (size) => {
  if (size < 1024) {
    return size + ' bytes';
  } else if (size < 1048576) {
    return (size / 1024).toFixed(2) + ' KB';
  } else {
    return (size / 1048576).toFixed(2) + ' MB';
  }
};

const imageUrl = computed(() => {
  return new URL(`../assets/fileTypes/${getType(props.name)}.png`, import.meta.url).href;
});
</script>


<style scoped>
.relative {
  position: relative;
}

.absolute {
  position: absolute;
}
</style>