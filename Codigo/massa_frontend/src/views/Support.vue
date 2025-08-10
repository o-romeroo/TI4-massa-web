<template>
  <div style="width: 100%; justify-content: center; display: flex;">
    <ContentBanner :title="banner.title" :description="banner.description" :buttonText="banner.buttonText"
      @buttonClicked="openForm" />
  </div>

  <v-container>
    <h2 class="text-center pb-10">What is your question about?</h2>
    <v-row class="d-flex justify-center">
      <v-col v-for="item in items" cols="2">
        <v-btn size="140" :prepend-icon="item.icon" stacked @click="selectCategory(item.category)" class="mb-5">
          {{ item.text }}
        </v-btn>
      </v-col>
    </v-row>

    <v-text-field v-model="searchQuery" label="Search Questions" prepend-inner-icon="mdi-magnify"
      class="my-5"></v-text-field>

    <div class="panel">
      <v-expansion-panels variant="accordion">
        <v-expansion-panel v-for="(question, index) in filteredAndSearchedQuestions" :key="index"
          :title="question.title" :text="question.text" />
      </v-expansion-panels>
    </div>
  </v-container>

  <v-dialog v-model="isDialogOpen" max-width="600">
    <v-card class="mx-auto">
      <v-card-title class="text-center mt-3">
        <h2>Contact Us</h2>
      </v-card-title>
      <v-form v-model="isFormValid" @submit.prevent="sendEmail">
        <v-card-text>
          <v-row>
            <v-col cols="12" class="input-group">
              <v-text-field label="Name" v-model="form.name"></v-text-field>
            </v-col>
            <v-col cols="12" class="input-group">
              <v-text-field label="Email" v-model="form.email" :rules="[rules.email]"></v-text-field>
            </v-col>
            <v-col cols="12" class="input-group">
              <v-text-field label="Telephone" v-model="form.telephone" :rules="[rules.telephone]"
                @input="applyPhoneMask" maxlength="15"></v-text-field>
            </v-col>
            <v-col cols="12" class="input-group">
              <v-text-field label="Subject" v-model="form.subject" :rules="[rules.required]"></v-text-field>
            </v-col>
            <v-col cols="12" class="input-group">
              <v-textarea label="Description" v-model="form.description" :rules="[rules.required]"></v-textarea>
            </v-col>
            <v-col cols="4" offset="5">
              <v-btn color="#0A2E49" @click="sendEmail" :disabled="!isFormValid">Send</v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-form>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="showSnackbar" :timeout="3000" color="success" top>
    Email sent successfully!
  </v-snackbar>
</template>

<script setup>
import ContentBanner from '@/components/ContentBanner.vue';
import { ref, computed, watch } from 'vue';
import emailjs from 'emailjs-com';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const searchQuery = ref('');

const filteredAndSearchedQuestions = computed(() => {
  const categoryQuestions = questions.value[category.value];
  if (searchQuery.value === '') {
    return categoryQuestions;
  } else {
    return categoryQuestions.filter(question => {
      return question.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        question.text.toLowerCase().includes(searchQuery.value.toLowerCase());
    });
  }
});

const items = [
  {
    category: 'massa',
    text: 'Massa',
    icon: 'mdi-atom',
  },
  {
    category: 'results',
    text: 'Results',
    icon: 'mdi-chart-line',
  },
  {
    category: 'security',
    text: 'Security',
    icon: 'mdi-shield-check',
  },
  {
    category: 'technicalSupport',
    text: 'Technical Support',
    icon: 'mdi-headset',
  }
];

const category = ref('massa');

function selectCategory(type) {
  category.value = type;
}

const filteredQuestions = computed(() => {
  return questions.value[category.value];
});

const questions = ref({
  massa: [
    {
      title: 'What is MASSA Algorithm Web?',
      text: 'MASSA Algorithm Web is a user-friendly web application that allows researchers to easily apply the MASSA Algorithm for rational sampling of datasets in drug discovery and related fields. It simplifies the process of dividing a dataset into training and test sets for building robust and predictive QSAR/QSPR models.'
    },
    {
      title: 'Do I need programming knowledge to use MASSA Web?',
      text: 'No, MASSA Web is designed to be accessible to users with diverse technical backgrounds. It features an intuitive graphical interface that guides you through the entire process, from uploading your dataset to visualizing the results.'
    },
    {
      title: 'How do I upload my dataset?',
      text: 'You can easily upload your dataset in various formats, such as .sdf, .csv, or .xlsx, through a simple drag-and-drop interface or by selecting the file from your computer.'
    },
    {
      title: 'What analysis options are available?',
      text: 'MASSA Web offers various analysis options, including hierarchical clustering analysis (HCA), principal component analysis (PCA), and k-modes clustering. You can choose the methods that best suit your data and research question.'
    },
    {
      title: 'Can I customize the analysis parameters?',
      text: 'Yes, MASSA Web allows for customization of various analysis parameters, such as the percentage of molecules in each set, the distance metric for clustering, and the number of principal components. This flexibility ensures you have control over the sampling process.'
    },
    {
      title: 'How long does it take to process the analysis?',
      text: 'The analysis time depends on the size and complexity of your dataset and the chosen analysis options. However, MASSA Web is optimized for speed and efficiency, typically providing results within minutes.'
    }
  ],
  results: [
    {
      title: 'How can I visualize the results of the analysis?',
      text: 'MASSA Web provides interactive visualizations of the results, including dendrograms, bar charts, heatmaps, and scatter plots. These visualizations facilitate the interpretation of the data and identification of patterns.'
    },
    {
      title: 'How do I interpret the different types of charts and tables?',
      text: 'The web application provides clear explanations and interpretations for each type of chart and table generated. Additionally, you can access tooltips and interactive features that provide further details.'
    },
    {
      title: 'Can I download the results of the analysis?',
      text: 'Yes, you can download the results of the analysis, including the clustered data, generated models, and visualizations, in various formats, such as .csv, .xlsx, and .png, for further analysis or reporting.'
    }
  ],
  security: [
    {
      title: 'How do I create an account on MASSA Web?',
      text: 'Simply click on the "Sign Up" button on the homepage and follow the instructions to create a free account. You will need to provide a valid email address and choose a secure password.'
    },
    {
      title: 'I forgot my password. How can I recover it?',
      text: 'Click on the "Forgot Password" link on the login page. You will receive an email with instructions on how to reset your password.'
    },
    {
      title: 'Is my data safe on MASSA Web?',
      text: 'Yes, data security is a top priority. MASSA Web uses industry-standard security measures, including encryption and secure storage, to protect your data from unauthorized access.'
    }
  ],
  technicalSupport: [
    {
      title: 'Where can I find the complete documentation for MASSA Algorithm Web?',
      text: 'Comprehensive documentation, including tutorials and FAQs, is available on the MASSA Web website. You can access it directly from the application.'
    },
    {
      title: 'I found an error in the application. How can I report it?',
      text: 'You can report any errors or technical issues directly through the "CONTACT US" feature within the application. Please provide detailed information to help us resolve the issue quickly.'
    },
    {
      title: 'How can I contact support if I need further assistance?',
      text: 'Our dedicated support team is available to assist you. You can reach us via email or through the contact form on the MASSA website.'
    }
  ]
});

const banner = {
  title: "Welcome to the help center",
  description: "Get all your questions answered or contact our support channels",
  buttonText: "CONTACT US"
};

const isDialogOpen = ref(false);
const showSnackbar = ref(false);

const form = ref({
  email: '',
  name: '',
  telephone: '',
  subject: '',
  description: ''
});

function sendEmail() {
  if (!isFormValid.value)
    return;

  emailjs.send(import.meta.env.VITE_EMAILJS_SERVICE_ID, import.meta.env.VITE_EMAILJS_TEMPLATE_ID, {
    from_name: form.value.name,
    from_email: form.value.email,
    subject: form.value.subject,
    message: form.value.description,
    telephone: form.value.telephone
  }, import.meta.env.VITE_EMAILJS_USER_ID)
  .then((response) => {
    console.log('SUCCESS!', response.status, response.text);
    isDialogOpen.value = false;
    showSnackbar.value = true;
  }, (error) => {
    console.log('FAILED...', error);
  });
}

const isFormValid = ref(false);

watch(isDialogOpen, (newValue) => {
  if (newValue && authStore.isAuthenticated) {
    form.value.name = authStore.username;
  } else if (!newValue) {
    form.value = {
      email: '',
      name: '',
      telephone: '',
      subject: '',
      description: ''
    };

    isFormValid.value = false;
  }
});

const rules = {
  email: (value) => {
    if (!value) return 'Email is required.';
    if (!/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/.test(value)) return 'Invalid email format.';
    return true;
  },
  telephone: (value) => {
    if (!value) return 'Telephone is required.';

    const rawValue = value.replace(/\D/g, '');

    if (!/^(\d{2})(\d{4,5})(\d{4})$/.test(rawValue))
      return 'Invalid phone number. Use format: (99) 99999-9999 or (99) 9999-9999.';

    return true;
  },
  required: (value) => {
    return !!value || 'This field is required.';
  }
};

function openForm() {
  isDialogOpen.value = true;
}

function applyPhoneMask() {
  let rawValue = form.value.telephone.replace(/\D/g, '');

  if (rawValue.length > 10) {
    form.value.telephone = rawValue.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  } else if (rawValue.length > 5) {
    form.value.telephone = rawValue.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
  } else if (rawValue.length > 2) {
    form.value.telephone = rawValue.replace(/(\d{2})(\d{0,5})/, '($1) $2');
  } else {
    form.value.telephone = rawValue.replace(/(\d{0,2})/, '($1');
  }
}
</script>

<style scoped>
.input-group {
  margin-bottom: -15px
}
</style>