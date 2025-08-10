<template>
  <div style="width: 100%; justify-content: center; display: flex;">
    <ContentBanner :title="banner.title" :description="banner.description" />
  </div>
  <div class="content">
    <div class="about">

      <v-card class="massa-algorithm">
        <v-list lines="two">
          <v-list-subheader>Massa Algorithm</v-list-subheader>

          <v-list-item :prepend-avatar="foto_perfil_gverissimo" title="Gabriel Veríssimo">
            <template v-slot:subtitle>
              <p class="text-subtitle-2">Email:<a>gabrielverissimo@ufmg.br</a></p>
              <p class="text-subtitle-2">LinkedIn:<a href="https://www.linkedin.com/in/gabrielcverissimo/" target="_blank">Gabriel Veríssimo</a></p>
            </template>
          </v-list-item>

          <v-divider inset></v-divider>

          <v-list-item :prepend-avatar="foto_perfil_vmaltarollo" title="Vinicius Maltarollo">
            <template v-slot:subtitle>
              <p class="text-subtitle-2">Email:<a>maltarollo@ufmg.br</a></p>
              <p class="text-subtitle-2">LinkedIn:<a href="https://www.linkedin.com/in/vinicius-maltarollo-5740bb10/" target="_blank">Vinicius Maltarollo</a></p>
            </template>
          </v-list-item>
        </v-list>
      </v-card>

      <v-card class="massa-software">
        <v-list lines="two">
          <v-list-subheader>Massa Software</v-list-subheader>

          <v-list-item :prepend-avatar="foto_perfil_dg" title="Douglas Galvão">
            <template v-slot:subtitle>
              <p class="text-subtitle-2">Email:<a>douglas-mad@live.com</a></p>
              <p class="text-subtitle-2">LinkedIn:<a href="https://www.linkedin.com/in/douglasgmachado/" target="_blank">Douglas Galvão</a></p>
            </template>
          </v-list-item>

          <v-divider inset></v-divider>

          <v-list-item :prepend-avatar="foto_perfil_gramos" title="Gabriel Ramos">
            <template v-slot:subtitle>
              <p class="text-subtitle-2">Email:<a>gabrielrmzf@gmail.com</a></p>
              <p class="text-subtitle-2">LinkedIn:<a href="https://www.linkedin.com/in/gramos22/" target="_blank">Gabriel Ramos</a></p>
            </template>
          </v-list-item>

          <v-divider inset></v-divider>

          <v-list-item :prepend-avatar="foto_perfil_jp" title="João Pedro Braga">
            <template v-slot:subtitle>
              <p class="text-subtitle-2">Email:<a>joao.psbraga6@gmail.com</a></p>
              <p class="text-subtitle-2">LinkedIn:<a href="https://www.linkedin.com/in/jo%C3%A3o-pedro-braga-6a9264276/" target="_blank">João Pedro Braga</a></p>
            </template>
          </v-list-item>

          <v-divider inset></v-divider>

          <v-list-item :prepend-avatar="foto_perfil_romero" title="João Vitor Romero">
            <template v-slot:subtitle>
              <p class="text-subtitle-2">Email:<a>joaovitor.rome@gmail.com</a></p>
              <p class="text-subtitle-2">LinkedIn:<a href="https://www.linkedin.com/in/jo%C3%A3o-vitor-romero-sales-269544210/" target="_blank">João Vitor Romero</a></p>
            </template>
          </v-list-item>

          <v-divider inset></v-divider>

          <v-list-item :prepend-avatar="foto_perfil_lrandazzo" title="Lucas Randazzo">
            <template v-slot:subtitle>
              <p class="text-subtitle-2">Email:<a>lucasrandazzo2@gmail.com</a></p>
              <p class="text-subtitle-2">LinkedIn:<a href="https://www.linkedin.com/in/lucas-randazzo-13ba92264/" target="_blank">Lucas Randazzo</a></p>
            </template>
          </v-list-item>
        </v-list>
      </v-card>

    </div>
  </div>

</template>

<style>
.content {
  position: relative;
  z-index: 2;
  /* Coloca o conteúdo acima da imagem */
  padding: 1rem;
  width: 100%;
}

.massa-algorithm,
.massa-software {
  width: 100%;
  margin: 1rem;
}

.about {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}
</style>

<script setup>
import ContentBanner from "@/components/ContentBanner.vue";

import foto_perfil_gverissimo from '@/assets/fileTypes/foto_perfil_gverissimo.jpeg';
import foto_perfil_vmaltarollo from '@/assets/fileTypes/foto_perfil_vmaltarollo.jpeg';
import foto_perfil_dg from '@/assets/fileTypes/foto_perfil_dg.jpg';
import foto_perfil_gramos from '@/assets/fileTypes/foto_perfil_gramos.jpg';
import foto_perfil_jp from '@/assets/fileTypes/foto_perfil_jp.jpg';
import foto_perfil_romero from '@/assets/fileTypes/foto_perfil_romero.jpg';
import foto_perfil_lrandazzo from '@/assets/fileTypes/foto_perfil_lrandazzo.jpeg';

const banner = {
  title: "Who created Massa?",
  description: "Our team is composed of Pharmacy college teachers and reaserchers from the Federal University of Minas Gerais (UFMG) and Software Engineer students from the Pontifical Catholic University of Minas Gerais (PUC-MG).",
};
</script>
