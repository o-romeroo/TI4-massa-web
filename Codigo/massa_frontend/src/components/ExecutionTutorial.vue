<template>
  <v-container class="tutorial">
    <v-row>
      <v-col cols="12" md="4">
        <v-card v-if="showModalLeft" append-icon="mdi-close" @click:append="closeModalLeft" variant="tonal">
          <v-card-title>Algorithm Steps</v-card-title>
          <v-card-text>
            Here we have all steps that the algorithm takes to generate the
            desired output, from the parameter file upload, till the histograms
            and dendograms.
          </v-card-text>
        </v-card>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" md="6">
        <div v-if="showModalCenter" class="modal-overlay">
          <div class="modal-content" @click.stop>
            <button class="close-button" @click="closeModal()">&times;</button>
            <h2>WELCOME TO MASSA!</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Conubia
              posuere interdum felis efficitur enim mattis congue. Semper egestas
              vel ornare maximus; facilisi nostra nibh. Rutrum nulla leo accumsan
              pharetra metus parturient inceptos vestibulum. Vitae ultricies massa
              vitae mauris risus semper morbi. Maximus quisque sapien mattis
              pellentesque eu a varius montes. Platea imperdiet leo tortor himenaeos
              duis. Curabitur nisl leo, luctus nam nunc sodales.
            </p>
            <button class="start-button" @click="closeModal">
              LET'S GET STARTED!
            </button>
          </div>
        </div>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" md="5">
        <v-card v-if="showModalRight" append-icon="mdi-close" @click:append="closeModalRight" variant="tonal">
          <v-card-title>Get Started</v-card-title>
          <v-card-text>
            To get started in this flow, it is necessary to upload a parameter
            file containing all the molecule required information's.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ExecutionTutorial',
  props: {
    showModal: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      showModalLeft: false,
      showModalRight: false,
      showModalCenter: this.showModal
    };
  },
  methods: {
    closeModal() {
      this.showModalLeft = true;
      this.showModalRight = true;
      this.showModalCenter = false;
    },
    closeModalLeft() {
      this.showModalLeft = false;
    },
    closeModalRight() {
      this.showModalRight = false;
    },
  }
}
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background-color: #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  width: 600px;
  max-width: 90%;
  text-align: center;
  position: relative;
  z-index: 2001;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}

.start-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: black;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
</style>