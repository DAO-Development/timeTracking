<template>
  <div class="timing flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Отчетность по проделанной работе</h1>
      <v-btn class="action-btn" color="primary" @click="addForm = true">Добавить</v-btn>
      {{ timings }}
    </section>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="addForm = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>Добавление</h3>
        <v-card-text>
          <v-form ref="form" :model="newTiming">
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addTiming">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление путевого листа
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить часовой отчет? Отменить это действие будет невозможно</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteTiming">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Header from "../components/Header";

export default {
  name: "Timing",
  components: {Header},
  data() {
    return {
      timings: [],
      newTiming: {},
      formTitle: '',
      addForm: false,
      confirmDeleteDialog: false
    }
  },
  methods: {
    loadData() {

    },
    addTiming() {

    },
    putTiming() {

    },
    deleteTiming() {

    },

  }
}
</script>

<style scoped>

</style>