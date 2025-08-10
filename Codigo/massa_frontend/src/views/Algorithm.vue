<template>
  <div style="width: 100%; justify-content: center; display: flex;">
      <ContentBanner :title="banner.title" :description="banner.description" :buttonText="banner.buttonText"
        @buttonClicked="openArticle()" />
  </div>
  <div class="content">
    <p class="text-h4 font-weight-medium">The Massa Algorithm</p>
    <p class="text-justify"> The MASSA Algorithm is a tool designed to improve the rational selection of training and test data for QSAR (Quantitative Structure-Activity Relationship), QSPR (Quantitative Structure-Property Relationship) and other machine learning models for drug design. The algorithm integrates biological activity of molecules with their structural and physicochemical properties to sample datasets using clustering techniques (HCA and K-modes) and principal component analysis (PCA). This three-dimensional approach to exploring biological, physicochemical, and structural spaces enables sampling of training and test sets in a way that maximizes model performance and minimizes variability across subsets.

    Overall, in comparison to other sampling methods, MASSA produces models with better validation metrics and reduced variability across multiple replicates. It demonstrates superior performance in metrics such as Q²internal, Q²F1, Q²F2, Q²F3, and CCC, especially when compared to other sampling methods like Kennard-Stone, SPXY, Sphere Exclusion and random sampling. Notably, the algorithm achieves these results even when the descriptors used for QSAR/QSPR modeling differ from those used for the data separation, highlighting its versatility across various QSAR/QSPR techniques.

    Additionally, the MASSA Algorithm generates insightful visual representations of the data distribution, which aids in understanding the dataset’s structure and the reasoning behind the training and test set division. This tool is also particularly valuable when the QSAR descriptors are unavailable or when the goal is to construct multiple models with consistent training and test sets, leading to models with improved performance and more reliable predictions.

    Finally, we kindly request that you cite our work after use, as shown in the examples in the section “How the algorithm works”, subsection “Cite the tool”.
    </p>
  </div>

  <!-- <div class="text-center" style="padding-bottom: 2rem;">
    <p class="text-h4 font-weight-bold">Tutorials</p>
  </div>

  <v-row>
    <v-col cols="12" md="4">
      <v-card class="mx-auto" prepend-icon="$vuetify" width="400" href="https://github.com/vuetifyjs/vuetify/"
        rel="noopener" target="_blank">
        <template v-slot:title>
          <span class="font-weight-black">How to see the results</span>
        </template>

        <v-card-text class="bg-surface-light pt-4">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi, ratione debitis quis est labore
          voluptatibus! Eaque
          cupiditate minima, at placeat totam, magni doloremque veniam neque porro libero rerum unde voluptatem!
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-card class="mx-auto" prepend-icon="$vuetify" width="400" href="https://github.com/vuetifyjs/vuetify/"
        rel="noopener" target="_blank">
        <template v-slot:title>
          <span class="font-weight-black">How to see the results</span>
        </template>

        <v-card-text class="bg-surface-light pt-4">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi, ratione debitis quis est labore
          voluptatibus!
          Eaque cupiditate minima, at placeat totam, magni doloremque veniam neque porro libero rerum unde voluptatem!
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="12" md="4">
      <v-card class="mx-auto" prepend-icon="$vuetify" width="400" href="https://github.com/vuetifyjs/vuetify/"
        rel="noopener" target="_blank">
        <template v-slot:title>
          <span class="font-weight-black">How to see the results</span>
        </template>

        <v-card-text class="bg-surface-light pt-4">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi, ratione debitis quis est labore
          voluptatibus!
          Eaque cupiditate minima, at placeat totam, magni doloremque veniam neque porro libero rerum unde voluptatem!
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
  <div>

  </div> -->
</template>

<script setup>
import ContentBanner from '@/components/ContentBanner.vue';
const banner = {
  title: "The Massa Algorithm",
  description: "Access the full article on the rational sampling method",
  buttonText: "ARTICLE",
};

function openArticle() {
  window.open("https://link.springer.com/article/10.1007/s10822-023-00536-y", "_blank");
}
</script>

<style>
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("../assets/logo_pizza.svg");
  background-size: contain;
  background-attachment: fixed;
  background-position: center;
  opacity: 0.05;
  /* Aplica opacidade apenas à imagem */
  z-index: 1;
}

.content {
  position: relative;
  z-index: 2;
  /* Coloca o conteúdo acima da imagem */
  padding: 1rem;
  width: 100%;
}

.text-justify {
  margin: 1rem;

}

.mx-auto {
  margin-left: auto;
  margin-right: auto;

}

.text-center {
  display: flex;
  position: relative;
  align-items: center;
  flex-direction: column;
}

.button {
  margin-bottom: 1rem;
  width: 400px;
}
</style>
