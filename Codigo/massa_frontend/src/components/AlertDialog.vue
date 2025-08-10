<template>
  <v-dialog width="600" v-model="store.dialog.visible">
    <v-card>
      <v-card-title class="text-h5 font-weight-bold text-center">
        {{ store.dialog.title }}
      </v-card-title>
      <v-card-text class="text-body-1">
        {{ store.dialog.message }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="#062033" variant="elevated" @click="close">OK</v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { useDialogStore } from '@/stores/dialog';

const store = useDialogStore();

function close() {
  store.closeDialog();
}

</script>

