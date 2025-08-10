import { defineStore } from 'pinia';
import { reactive, ref, computed } from 'vue';

import { useDialogStore } from './dialog';

export const useMassaStore = defineStore('massa', () => {

    const dialogStore = useDialogStore();
    const file = ref(null);

    const options = reactive({
        biologicalActivities: [],
        SVDSolvers: ['auto', 'full', 'covariance_eigh', 'arpack', 'randomized'],
        HCALinkageMethods: ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']
    });

    const params = reactive({
        execution_id: null,
        percentage_of_molecules: 0.8,
        biological_activities: [],
        number_of_PCs: 0.85,
        svd_solver_for_PCA: 'full',
        dendrograms_x_axis_font_size: 5,
        bar_plots_x_axis_font_size: 12,
        linkage_method: 'complete',
        plot_dendrogram: true
    });

    const graphics = ref(null);

    const molPercentageSlider = computed({
        get() {
            return params.percentage_of_molecules * 100;
        },
        set(value) {
            params.percentage_of_molecules = value / 100;
        },
    });

    function isValidFileType() {
        const allowedExtensions = ['mol2', 'sdf', 'mol', 'xls', 'xlsx', 'csv'];
        const fileExtension = file.value.name.split('.').pop().toLowerCase();

        return allowedExtensions.includes(fileExtension);
    }

    function setFile(newFile) {
        file.value = newFile;

        if (!this.isValidFileType()) { 
            file.value = null;
            dialogStore.showDialog('Invalid file type', 'Please upload a valid file: .mol2, .sdf, .mol, .xls, .xlsx, .csv');
        }
    }

    function removeFile() {
        file.value = null;
    }

    function setGraphics(newGraphics) {
        graphics.value = newGraphics;
    }

    return {
        file, options, params, graphics, molPercentageSlider, isValidFileType, setFile, removeFile, setGraphics
    };
});