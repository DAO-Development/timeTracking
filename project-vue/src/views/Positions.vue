<template>
  <div class="positions flex-content">
    <Header/>
    <section class="summary-box">
      <h1>{{ title }}</h1>
      <v-btn class="action-btn" color="primary" @click="addForm=true">Добавить</v-btn>
      <v-list class="content-list">
        <template v-for="position in positions">
          <v-list-item :key="position.id">
            <v-list-item-content>
              <v-list-item-title>{{ position.name }}</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action v-if="$parent.$parent.edit.indexOf('Работники') !== -1">
              <v-icon color="grey lighten-1" @click="currentPosition = position.id; confirmDeleteDialog = true">
                $deleteIcon
              </v-icon>
            </v-list-item-action>
          </v-list-item>
        </template>
      </v-list>
      <v-dialog v-model="addForm" max-width="520">
        <v-card>
          <v-card-title>
            Введите новую специальность/должность
          </v-card-title>
          <v-card-text>
            <v-form ref="addForm">
              <v-text-field placeholder="Название*" v-model="newPosition"
                            outlined :rules="reqRules"></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="addForm=false">Отменить</v-btn>
            <v-btn color="primary" text @click="addPosition">Сохранить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="confirmDeleteDialog" max-width="500">
        <v-card>
          <v-card-title>
            Удаление группы пользователей
          </v-card-title>
          <v-card-text>Вы действительно хотите удалить выбранную группу пользователей? Отменить это действие будет
            невозможно
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
            <v-btn color="primary" text @click="deletePosition">Подтвердить</v-btn>
          </v-card-actions>
        </v-card>

      </v-dialog>
    </section>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "Positions",
  props: {
    table: String
  },
  data() {
    return {
      title: '',
      url: '',
      positions: [],
      newPosition: '',
      currentPosition: 0,
      addForm: false,
      confirmDeleteDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
    }
  },
  created: function () {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      // if (this.$parent.$parent.read.indexOf('Контакты') === -1)
      //   this.$router.push({name: "Index"})
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      if (this.table === 'profile') {
        this.url = "time-tracking/profiles/positions"
        this.title = 'Специальности профилей'
      } else if (this.table === 'client') {
        this.url = "time-tracking/clients-employees/positions"
        this.title = 'Должности контактов'
      }
      this.loadData()
    } else {
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + this.url,
        type: "GET",
        success: (response) => {
          this.positions = response.data.positions
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    addPosition() {
      if (this.$refs.addForm.validate())
        $.ajax({
          url: this.$hostname + this.url,
          type: "POST",
          data: {name: this.newPosition},
          success: () => {
            this.addForm = false
            this.loadData()
            this.newPosition = ''
          },
          error: (response) => {
            console.log(response)
            if (response.status === 500) {
              this.alertMsg = "Ошибка соединения с сервером"
            } else if (response.status === 401) {
              this.$refresh()
            } else {
              this.alertMsg = "Непредвиденная ошибка"
            }
            this.alertError = true
          }
        })
    },
    deletePosition() {
      $.ajax({
        url: this.$hostname + this.url,
        type: "DELETE",
        data: {id: this.currentPosition},
        success: () => {
          this.confirmDeleteDialog = false
          this.loadData()
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
  }
}
</script>

<style scoped>

</style>