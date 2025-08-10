<template>
  <v-container>
    <v-stepper v-model="step" alt-labels>
      
      <!-- Header Stepper -->
      <v-stepper-header>
          <v-stepper-item title="Upload file" value="1" editable @click="step = 0" />
          <v-divider/>
          <v-stepper-item title="Optional Arguments" value="2" :editable="step2validations" @click="step = 1" />
          <v-divider/>
          <v-stepper-item title="Results and download" value="3" :editable="step3validations" @click="step = 2" />
      </v-stepper-header>


      <v-stepper-window>

        <AlertDialog/>
        
        <!-- Upload File (Step 1)-->
        <v-stepper-window-item value="1">

          <v-card class="d-flex flex-column align-center" flat>
            <ExecutionTutorial :showModal=viewTutorial />
            <v-card-text class="text-center">
                <v-btn v-if="!massaStore.file" class="upload-button d-flex" @click="fileInput.click()" append-icon="mdi-upload"> UPLOAD FILE </v-btn>
                <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none" />

                <div class="d-flex">
                    <CardFile v-if="massaStore.file" :name='massaStore.file.name' :size="massaStore.file.size" @click="removeFileInput" />
                </div>
            </v-card-text>
        </v-card>

        </v-stepper-window-item>

        <!-- Optional Arguments (Step 2)-->
        <v-stepper-window-item value="2">
          <div>
            
            <v-form>
              <v-container>
                <h1 class="section-title">MAIN PARAMETERS OF ALGORITHM</h1>
                <v-row class="mb-5 elevation-2">
                  <v-spacer></v-spacer>
                  <v-col cols="12" md="8" class="my-2">
                    <span>Percentage of molecules in training set</span>
                    <v-hover v-slot:default="{ isHovering, props }">
                      <div class="d-inline-block" v-bind="props">
                        <v-icon 
                          color="#062033"
                          small
                          size="15"
                          class="ml-2"
                        >
                          mdi-information
                        </v-icon>
                        <div 
                          v-if="isHovering" 
                          class="tooltip-content" 
                        >
                          This variable controls the percentage of molecules allocated to the training set. 
                          The percentage of molecules in the test set is calculated as 100% minus the percentage assigned to the training set. 
                          We recommend setting this value between 70% and 90%, depending on the size of your dataset, with the default value set at 80%.
                        </div>
                      </div>
                    </v-hover>
                    <v-slider 
                      v-model="massaStore.molPercentageSlider" 
                      thumb-label 
                      min="0" 
                      max="100" 
                      color="#062033"
                    ></v-slider>
                  </v-col>
                  <v-col cols="12" md="2" class="mt-3">
                    <v-text-field 
                      variant="solo-filled" 
                      v-model="massaStore.molPercentageSlider" 
                      type="number" 
                      style="width: 80px;" 
                      min="0"
                      max="100" 
                      suffix="%"
                    ></v-text-field>
                  </v-col>
                  <v-spacer></v-spacer>
                </v-row>
                
                <h1 class="section-title">CLUSTERIZATION PARAMETERS</h1>

                <v-row class="mb-5 elevation-2">
                  <v-spacer></v-spacer>
                  <v-col cols="12" md="9" class="mt-2">
                    <span class="pb-3">Biological activities for separation</span>
                    <v-hover v-slot:default="{ isHovering, props }">
                      <div class="d-inline-block" v-bind="props">
                        <v-icon 
                          color="#062033"
                          small
                          size="15"
                          class="ml-2"
                        >
                          mdi-information
                        </v-icon>
                        <div 
                          v-if="isHovering" 
                          class="tooltip-content"
                        >
                        The biological activity(ies) or other y-property(ies) used for QSAR or machine learning modeling. The algorithm can handle one or more properties; however, 
                        these properties must be represented as either integers or floating-point numbers. If your dataset is represented in classes (e.g., active or inactive; 
                        soluble, partially soluble, or insoluble), you should represent them as integers (e.g., 0 or 1; 1, 2, or 3).
                        </div>
                      </div>
                    </v-hover>
                    <v-select 
                    class="mt-3"
                      clearable
                      chips
                      :items="massaStore.options.biologicalActivities"
                      multiple
                      variant="solo-filled"
                      v-model="massaStore.params.biological_activities"
                    ></v-select>
                  </v-col>

                  <v-spacer></v-spacer>
                  <v-spacer></v-spacer>
                  
                  <v-col cols="12" md="4" offset="1" style="max-width: 300px;">
                    <span class="smaller-text">Nº of principal components in PCA</span>
                    <v-hover v-slot:default="{ isHovering, props }">
                      <div class="d-inline-block" v-bind="props">
                        <v-icon 
                          color="#062033"
                          small
                          size="15"
                          class="ml-2"
                        >
                          mdi-information
                        </v-icon>
                        <div 
                          v-if="isHovering" 
                          class="tooltip-content" 
                        >
                        Defines the number of principal components to reduce the dimensionality of variables related to biological, physicochemical and structural domains. 
                        If the value is a decimal between 0 and 1, the number of principal components is what explains &lt;input number&gt;*100&#37;
                        of the variance. If the value is greater than 1, the number of PCs will be exactly the input integer, <b>but please note:</b>
                        <p><b>a.</b> If the number of PCs is an integer and equal to or greater than the number of physicochemical properties (7), the PCA step will be bypassed for this domain. The same applies to the biological domain.</p>
                        <p><b>b.</b> If the number of biological activities is less than 3, the PCA step will be bypassed for this domain.</p>
                        </div>
                      </div>
                    </v-hover>
                    <v-text-field class="mt-3" v-model="massaStore.params.number_of_PCs" type="number" min="0" variant="solo-filled"></v-text-field>
                  </v-col>
                  <v-col cols="12" md="3">
                    <span>SVD solver for PCA</span>
                    <v-hover v-slot:default="{ isHovering, props }">
                      <div class="d-inline-block" v-bind="props">
                        <v-icon 
                          color="#062033"
                          small
                          size="15"
                          class="ml-2"
                        >
                          mdi-information
                        </v-icon>
                        <div 
                          v-if="isHovering" 
                          class="tooltip-content" 
                        >
                        In the web version of the MASSA algorithm, the only available option is the default setting: "full." However, if you wish to modify this parameter in the command-line version, please refer to the “sklearn.decomposition.PCA” 
                        section <a href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" target="_blank">here</a> for more information.
                        </div>
                      </div>
                    </v-hover>
                    <v-select class="mt-3" :items="massaStore.options.SVDSolvers" v-model="massaStore.params.svd_solver_for_PCA" variant="solo-filled" disabled></v-select>
                  </v-col>

                  <v-col cols="12" md="3">
                    <span>HCA linkage method</span>
                    <v-hover v-slot:default="{ isHovering, props }">
                      <div class="d-inline-block" v-bind="props">
                        <v-icon 
                          color="#062033"
                          small
                          size="15"
                          class="ml-2"
                        >
                          mdi-information
                        </v-icon>
                        <div 
                          v-if="isHovering" 
                          class="tooltip-content" 
                        >
                        The linkage criterion to use in hierarchical clustering analysis (HCA). The algorithm will merge the pairs of clusters that minimize this criterion. For more information, please refer to the “scipy.cluster.hierarchy.linkage” topic 
                        <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html?highlight=linkage#scipy.cluster.hierarchy.linkage" target="_blank">here</a> for more information.
                        </div>
                      </div>
                    </v-hover>
                    <v-select class="mt-3"  :items="massaStore.options.HCALinkageMethods" variant="solo-filled" v-model="massaStore.params.linkage_method"></v-select>
                  </v-col>

                  <v-spacer></v-spacer>
                </v-row>

                <h1 class="section-title">PLOT PARAMETERS</h1>

                <v-row class="mb-5 elevation-2">
                  <v-spacer></v-spacer>
                  <v-spacer></v-spacer>
                  <v-col cols="12" md="3" class="mt-2 pb-2">
                    <span>Plot dendrogram</span>
                    <v-switch class="mt-2" v-model="massaStore.params.plot_dendrogram" variant="solo-filled"
                    :color="massaStore.params.plot_dendrogram ? '#062033' : 'grey'" ></v-switch>
                  </v-col>
                  <v-spacer></v-spacer>
                  <v-col cols="12" md="3" class="mt-2 pb-2">
                    <span >X-axis font for Dendrograms</span>
                    <v-text-field  class="mt-2" v-model="massaStore.params.dendrograms_x_axis_font_size" variant="solo-filled" type="number" style="width: 70px;" 
                    min="0" :disabled="!massaStore.params.plot_dendrogram"></v-text-field>
                  </v-col>
                  <v-spacer></v-spacer>
                  <v-col cols="12" md="4" class="mt-2 pb-2">
                    <span>X-axis font for Bar Charts</span>
                    <v-text-field class="mt-2" v-model="massaStore.params.bar_plots_x_axis_font_size" variant="solo-filled" type="number" style="width: 70px;" 
                    min="0" :disabled="!massaStore.params.plot_dendrogram"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </div>
        </v-stepper-window-item>

        <!-- Results and download (Step 3)-->
        <v-stepper-window-item value="3">

          <div v-if="massaStore.graphics">
            <div class="d-flex  relative"> 
              <h2 v-if="massaStore.params.plot_dendrogram" class="ml-10 py-5">Dendrograms:</h2>  
              <v-col cols="auto" class="absolute top-0 right-0">
              <v-btn color="#062033" prepend-icon="mdi-open-in-new" @click="service.downloadFile"> DOWNLOAD </v-btn>
            </v-col>
            </div> 
            <div v-for="(image, key) in massaStore.graphics.dendrograms" :key="key">
              <img v-if="image" :src="`data:image/png;base64,${image}`" alt="Dendrogram" class="image" />
            </div>

            <div class="d-flex"> 
              <h2 class="ml-10 pt-10">Distance Plots:</h2>
            </div>
            <div  class="my-3" v-for="(values, key) in massaStore.graphics.distance_plot" :key="key">
              <LineChart 
                :xLabels="values.x"
                :yValues="values.y"
                :title="values.title"
                :chartKey="key"
              />
            </div>

            <div class="d-flex"> 
              <h2 class=" ml-10 pt-7">Distribution Plots:</h2>
            </div>
            <div class="pa-4 my-3" v-for="(values, key) in massaStore.graphics.distribution_plots" :key="key">
                <BarChart :chartData="values"/>
            </div>
          </div>
        </v-stepper-window-item>

        <v-progress-linear v-if="loading" indeterminate color="#062033"></v-progress-linear>

      </v-stepper-window>

      <v-stepper-actions 
        @click:next="handleNext" 
        @click:prev="step = step - 1">
      </v-stepper-actions>

    </v-stepper>
  </v-container>
</template>

<script setup>

import { ref } from 'vue';

import ExecutionTutorial from './ExecutionTutorial.vue';
import LineChart from '@/components/LineChart.vue';
import BarChart from '@/components/BarChart.vue';
import CardFile from '@/components/CardFile.vue';
import AlertDialog from '@/components/AlertDialog.vue';
import { useMassaStore } from '@/stores/massa';
import ExecutionService from '@/services/ExecutionService';


const massaStore = useMassaStore();

const service = new ExecutionService();

const fileInput = ref(null); 
const viewTutorial = ref(false);

const step = ref(0);
const step2validations = ref(false);
const step3validations = ref(false);

const loading = ref(false);

function handleFileUpload(event) {
  massaStore.setFile(event.target.files[0]);
  fileInput.value.value = null;
}

function removeFileInput() {
  massaStore.removeFile();
  step2validations.value = false;
  fileInput.value.value = null;
}

async function handleNext() {
  var success = false;

  switch (step.value)
  {
    case 0:
      loading.value = true;
      success = await service.uploadFile();
      loading.value = false;

      if(success){
        step2validations.value = true;
        step.value = 1;
      }

      break;

    case 1:
      loading.value = true;
      success = await service.runMassa();
      loading.value = false;

      if(success){
        step3validations.value = true;
        step.value = 2;
      }

      break;
  }
}

</script>


<style scoped>
.upload-button {
  grid-column: 2;
  grid-row: 1;
  justify-self: end;
  display: flex;
  align-items: center;
  cursor: pointer;
  background-color: #d9d9d9;
}

.image-container {
  margin-bottom: 20px;
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.image {
  display: flex;
  width: 1000px;   
  height: 500px;  
  object-fit: cover; 
  margin: 10px auto; 
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Título das imagens */
h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

h3 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #555;
}

.relative {
  position: relative;
}

.absolute {
  position: absolute;
}

.tooltip-content {
  position: absolute; 
  background: #062033;
  color: #ffffff;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000; 
  max-width: 380px;
  line-height: 1.5;
  font-size: 14px;
  white-space: normal;
}

.section-title {
    margin-bottom: 16px; 
    margin-top: 32px;
    font-size: 24px;     
    font-weight: bold;   
  }




</style>