<template>
    <div class="banner-content" style="width: 100%; justify-content: center; display: flex;">
        <ContentBanner :title="banner.title" :description="banner.description" :buttonText="banner.buttonText"
            @buttonClicked="openExecutionComponent()" />
    </div>

    <div class="tab-component" style="width: 100%;">
        <v-card>
            <v-tabs v-model="tab" align-tabs="center" bg-color="#092F47">
                <v-tab value="one">Molecules count</v-tab>
                <v-tab value="two">City and Country Infos</v-tab>
            </v-tabs>

            <v-card-text>
                <v-tabs-window v-model="tab">
                    <v-tabs-window-item value="one">
                        <v-card title="Number of biological activities" style="flex-direction: column;" class="mb-14">
                            <div class="d-flex align-center" style="margin-left: 15px;">
                                <span class="text-subtitle-1">Average number of molecules per biological
                                    activity:</span>
                                <v-chip class="text-subtitle-1" :value="moleculeCountAvg" variant="text">
                                    {{ moleculeCountAvg }}
                                </v-chip>
                            </div>
                            <div class="d-flex align-center " style="margin-left: 15px; margin-bottom: 15px;">
                                <span class="text-subtitle-1">Number of biological activities analysed so far:</span>
                                <v-chip class="text-subtitle-1" :value="biologicalActivityTotal" variant="text">
                                    {{ biologicalActivityTotal }}
                                </v-chip>
                            </div>
                        </v-card>


                        <v-card class="my-8 mx-auto overflow-visible" max-width="400" elevation="4" rounded="lg">
                            <v-sheet color="#092F47" class="mx-auto rounded-t-lg pa-4" height="150">
                                <v-sparkline :labels="labels" :model-value="values" color="white" line-width="2" smooth
                                    auto-draw></v-sparkline>
                            </v-sheet>

                            <v-card-text class="pt-0 pb-4">
                                <div class="text-h6 font-weight-medium mb-2">
                                    User Runs
                                </div>
                                <div class="text-body-2 font-weight-light text-grey-darken-1">
                                    Number of biological activities analysed
                                </div>

                            </v-card-text>
                        </v-card>

                    </v-tabs-window-item>

                    <v-tabs-window-item value="two">
                        <v-card>
                            <v-card-title class="text-h5 py-4">
                                <v-icon icon="mdi-city" class="me-2"></v-icon>
                                Users Cities
                            </v-card-title>
                            <v-card-subtitle class="pb-4">
                                The cities that Massa Software users are from:
                            </v-card-subtitle>
                            <v-card-text>
                                <v-text-field v-model="search" density="compact" label="Search City"
                                    prepend-inner-icon="mdi-magnify" variant="outlined" hide-details
                                    single-line></v-text-field>

                                <v-data-table v-model:search="search" :items="cities" :page="page"
                                    :items-per-page="itemsPerPage" class="mt-4">
                                    <template v-slot:header="{ props: { headers } }">
                                        <tr v-for="(header, index) in headers" :key="index">
                                            <th :class="['text-' + header.align]"> {{ header.title }}</th>

                                        </tr>


                                    </template>


                                    <template v-slot:item.name="{ item }">
                                        <div class="text-capitalize"> </div>
                                        {{ item.name }}
                                    </template>

                                    <template v-slot:item.rating="{ item }">
                                        <v-rating :model-value="item.rating" color="amber" density="compact"
                                            size="small" readonly half-increments></v-rating>
                                    </template>

                                    <template v-slot:bottom>
                                        <div class="text-center pt-2">
                                            <v-pagination v-model="page" :length="pageCount"></v-pagination>
                                        </div>
                                    </template>
                                </v-data-table>
                            </v-card-text>
                        </v-card>

                    </v-tabs-window-item>
                </v-tabs-window>
            </v-card-text>
        </v-card>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import ContentBanner from '@/components/ContentBanner.vue';
import { getIpInfos } from '@/services/Geolocation';
import { getCountryName } from '@/services/Geolocation';
import { useStatsStore } from '@/stores/stats';
import { useGeolocationStore } from '@/stores/geolocation';

const statsStore = useStatsStore();
const geolocationStore = useGeolocationStore();

const banner = {
    title: "User Data",
    description: "Data collected from users",
};

const tab = ref(null);

const stats = ref(null);
const statsError = ref(null);

const ipInfo = ref(null);
const ipError = ref(null);

const cities = ref([]);
const page = ref(1);
const itemsPerPage = 10;
const search = ref('');
const pageCount = ref(0);



const biologicalActivitiesPerDay = ref({});
const labels = ref(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
const values = ref([0, 0, 0, 0, 0, 0, 0]);


const moleculeCountAvg = computed(() => stats.value?.molecule_count_avg || 0);
const biologicalActivityTotal = computed(() => stats.value?.biological_activity_total || 0);

async function fetchStats() {
    try {
        stats.value = await statsStore.fetchStats();
        const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        values.value = daysOfWeek.map(day => stats.value.biological_activities_per_day[day] || 0);
    } catch (error) {
        statsError.value = error;
    }
}


async function fillIpInfos() {
    try {
        ipInfo.value = await geolocationStore.fetchUsersIpInfos();
    } catch (error) {
        ipError.value = error;
        return;
    }

    ipInfo.value.forEach(element => {
        cities.value.push({
            name: element.city,
            country: element.country,
        });
    })

    pageCount.value = Math.ceil(cities.value.length / itemsPerPage);
}

onMounted(async () => {

    await Promise.all([
        fillIpInfos(),
        fetchStats()
    ])

});
</script>

<style scoped>
.tab-component {
    width: 100%;
    justify-content: center;
    margin-top: 20px;
}

.v-sheet--offset {
    top: -24px;
    position: relative;
}
</style>
