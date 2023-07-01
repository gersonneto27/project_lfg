<template>
  <v-container>
    <v-form @submit.prevent="submitForm">
      <v-col>
        <v-sheet>
          <v-text-field
            v-model="name"
            :counter="10"
            label="Nome Completo"
            required
          ></v-text-field>
        </v-sheet>
      </v-col>

      <v-col>
        <v-sheet>
          <v-text-field
            v-model="birth_date"
            :counter="10"
            v-mask="['##/##/####']"
            label="Data de Nascimento"
            required
            :type="date"
          ></v-text-field>
        </v-sheet>
      </v-col>

      <v-col>
        <v-sheet>
          <v-text-field
            v-model="proposal_value"
            v-mask="[
              '#.###.###.###,##',
              '###.###.###,##',
              '##.###.###,##',
              '#.###.###,##',
              '###.###,##',
              '##.###,##',
              '#.###,##',
              '###,##',
              '##,##',
              '#,##',
            ]"
            label="Valor da Proposta"
            required
          ></v-text-field>
        </v-sheet>
      </v-col>

      <v-col>
        <v-sheet>
          <v-text-field
            v-model="document"
            v-mask="[
              '###.###.###',
              '##.###.###',
              '#.###.###',
              '###.###',
              '##.###',
              '#.###',
              '###',
            ]"
            label="Documento de Identidade"
            required
          ></v-text-field>
        </v-sheet>
      </v-col>

      <v-col v-for="field in proposalConfigFields" :key="field.id">
        <v-sheet>
          <v-text-field
            v-model="form[field.name].value"
            :label="field.name"
            :type="fieldType(field.field_type)"
            outlined
          ></v-text-field>
        </v-sheet>
      </v-col>

      <v-col>
        <v-sheet>
          <v-btn block type="submit">Enviar Proposta</v-btn>
        </v-sheet>
      </v-col>
      <v-alert v-if="successMessage" type="success" dense>
        {{ successMessage }}
      </v-alert>
    </v-form>
  </v-container>
</template>

<script>
import { mask } from "vue-the-mask";
import { parse, format } from "date-fns";
export default {
  directives: {
    mask,
  },
  data() {
    return {
      name: "",
      birth_date: "",
      proposal_value: "",
      document: "",
      form: {},
      proposalConfigFields: [],
    };
  },

  created() {
    this.loadProposalConfigFields();
  },

  methods: {
    loadProposalConfigFields() {
      fetch("http://localhost:8000/api/proposal-configs/")
        .then((response) => response.json())
        .then((data) => {
          this.proposalConfigFields = data;
          this.initForm();
        })
        .catch((error) => {
          console.error("Error loading proposal config fields:", error);
        });
    },

    initForm() {
      // Inicializar o objeto de formulário com os campos do formulário
      this.form = {}; // Inicializar como objeto vazio

      for (const field of this.proposalConfigFields) {
        this.form[field.name] = { value: "" };
      }
    },
    fieldType(fieldType) {
      if (fieldType === "char") {
        return "text";
      } else if (fieldType === "integer") {
        return "number";
      } else {
        return "text";
      }
    },

    submitForm() {
      const brazilianDate = parse(this.birth_date, "dd/MM/yyyy", new Date());
      const americanDate = format(brazilianDate, "yyyy-MM-dd");
      const proposalData = [];
      for (const field of this.proposalConfigFields) {
        const value = this.form[field.name]?.value;
        proposalData.push({ field: field.id, value: value });
      }

      this.proposal_value_formatted = this.proposal_value.replace(/[.,]/g, "");

      const payload = {
        name: this.name,
        birth_date: americanDate,
        document: this.document,
        proposal_value: this.proposal_value_formatted,
        dados_proposta: proposalData,
      };

      fetch("http://localhost:8000/api/proposals/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.proposal_id) {
            this.successMessage = "Proposta enviada com sucesso!";
            console.log("Form submitted successfully:", data);
          }
        })
        .catch((error) => {
          console.error("Error submitting form:", error);
        });
    },
  },
};
</script>
<style>
.d-flex {
  display: flex;
}

.justify-center {
  justify-content: center;
}

.align-center {
  align-items: center;
}

.v-container {
  height: 100vh;
}

.pa-4 {
  padding: 1rem;
  margin-right: 1rem;
  margin-left: 1rem;
}
</style>
