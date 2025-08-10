import axios from 'axios';
import API_URL from '@/config/api';
import { useMassaStore } from '@/stores/massa';
import { useDialogStore } from '@/stores/dialog';
import { useAuthStore } from '@/stores/auth';

class ExecutionService {
  massaStore = useMassaStore();
  dialogStore = useDialogStore();
  authStore = useAuthStore();

  async uploadFile() {

    if (this.massaStore.file === null) {
      this.dialogStore.showDialog('File not selected', 'Please select a file');
      return
    }

    const formData = new FormData();
    formData.append("file", this.massaStore.file);

    try {
      const response = await axios.post(`${API_URL}/executions/create`, formData, {
        headers: {
          Authorization: `Bearer ${this.authStore.token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      const data = response.data;

      this.massaStore.params.biological_activities = [];
      this.massaStore.options.biologicalActivities = data.arguments.biological_activities;
      this.massaStore.params.execution_id = data.arguments.execution_id;

      return true;

    } catch (err) {
        console.error('Failed to load data: ' + err.message);
        this.dialogStore.showDialog('Error processing file', 'Try again!');
    }

  }

  async updateArguments() { 
    try {
      await axios.put(`${API_URL}/executions/update`, this.massaStore.params);
    } catch (error) {
      console.error("Error sending arguments:", error);
      this.dialogStore.showDialog('Error processing arguments', 'Try again!')
    }
  }

  async runMassa() {

    if (this.massaStore.params.biological_activities.length === 0) {
      this.dialogStore.showDialog('Biological activity not selected', 'Please select the biological activity');
      return
    }

    await this.updateArguments();

    const formData = new FormData();
    formData.append("file", this.massaStore.file);

    try {
        const response = await axios.post(`${API_URL}/executions/start?execution_id=${this.massaStore.params.execution_id}`, formData);
        this.massaStore.setGraphics(response.data.images);

        return true;

    } catch (error) {
        console.error("Error sending file:", error);
        this.dialogStore.showDialog('Error processing file', 'Try again!');
    }
}

  downloadFile = async () => {
    try {
        const response = await axios.get(`${API_URL}/executions/download-pdf/${this.massaStore.params.execution_id}`);
        const contentType = response.headers['content-type'];
        const filename =  contentType.includes('zip') ? 'results.zip' : (contentType.includes('pdf') ? 'results.pdf' : 'results');  
        const blob = new Blob([response.data], { type: contentType }); 
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename); 
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url); 
    } catch (error) {
      console.error("Error downloading file:", error);
      this.dialogStore.showDialog(`Error downloading file`, 'Try again!');
    }
  };
}


export default ExecutionService;