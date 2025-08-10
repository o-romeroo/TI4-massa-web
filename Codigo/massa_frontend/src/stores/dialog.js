import { defineStore } from 'pinia';
import { reactive } from 'vue';

export const useDialogStore = defineStore('dialog', () => {
    
    const dialog = reactive({
        visible: false,
        title: '',
        message: '',
    });

    function showDialog(title, message) {
        dialog.visible = true;
        dialog.title = title;
        dialog.message = message;
    }

    function closeDialog() {
        dialog.visible = false;
        dialog.title = '';
        dialog.message = '';
    }

    return {
        dialog, showDialog, closeDialog
    };
});
