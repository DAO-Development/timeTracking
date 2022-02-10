<template>
  <div class="groups flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Управление группами пользователей</h1>
      <v-btn class="action-btn" color="primary" @click="addGroupForm=true">Добавить группу</v-btn>
      <v-list class="groups__list">
        <v-list-group v-for="group in groups" :key="group.id" v-model="group.active" no-action>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="group.name"></v-list-item-title>
            </v-list-item-content>
          </template>
          <template v-for="func in functions[group.name]">
            <div class="groups-single__functions" :key="func.text">
              <span class="bold-text">{{ func.name }}</span>
              <v-checkbox v-model="func.data.read" label="Чтение" @change="putFunction(func.data)"></v-checkbox>
              <v-checkbox v-model="func.data.edit" label="Редактирование" @change="putFunction(func.data)"></v-checkbox>
            </div>
          </template>
          <div class="groups-single__action">
            <v-btn class="action-btn" color="error" @click="currentGroup = group.id; confirmDeleteGroup = true">Удалить
              группу
            </v-btn>
          </div>
        </v-list-group>
      </v-list>
    </section>
    <v-dialog v-model="addGroupForm" max-width="500">
      <v-card>
        <v-card-title>
          Введите название новой группы
        </v-card-title>
        <v-card-text>
          <v-form ref="addForm">
            <v-text-field placeholder="Название*" v-model="newGroup.name"
                          outlined :rules="reqRules"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="addGroupForm=false">Отменить</v-btn>
          <v-btn color="primary" text @click="addGroup">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteGroup" max-width="500">
      <v-card>
        <v-card-title>
          Удаление группы пользователей
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить выбранную группу пользователей? Отменить это действие будет
          невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteGroup = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteGroup">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>

    </v-dialog>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";

export default {
  name: "Groups",
  components: {Header},
  created() {
    console.log("init Groups")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  data() {
    return {
      groups: [],
      functions: [],
      newGroup: {
        id: 0,
        name: ''
      },
      currentGroup: 0,
      addGroupForm: false,
      confirmDeleteGroup: false,
      alertError: false,
      alertMsg: '',
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/groups",
        type: "GET",
        success: (response) => {
          this.groups = response.data.groups
          this.functions = response.data.functions
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    },
    putFunction(func) {
      $.ajax({
        url: this.$hostname + "time-tracking/groups-functions",
        type: "PUT",
        data: func,
        success: (response) => {
          console.log("Данные обновлены")
          func.id = response.data.id
          this.$emit('load-functions')
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    },
    addGroup() {
      if (this.$refs.addForm.validate()) {
        $.ajax({
          url: this.$hostname + "time-tracking/group",
          type: "POST",
          data: this.newGroup,
          success: () => {
            console.log("Даннные добавлены")
            this.loadData()
            this.addGroupForm = false
            this.newGroup = {
              id: 0,
              name: ''
            }
          },
          error: (response) => {
            switch (response.status) {
              case 500:
                this.alertMsg = "Ошибка соединения с сервером"
                break
              case 400:
                this.alertMsg = "Ошибка в данных"
                break
              case 401:
                this.$refresh()
                break
              case 403:
                this.alertMsg = "Нет доступа"
                break
              default:
                this.alertMsg = "Непредвиденная ошибка"
            }
            this.alertError = true
          },
        })
      } else {
        console.log("Заполните обязательные поля")
        this.alertMsg = "Заполните обязательные поля"
        this.alertError = true
      }
    },
    deleteGroup() {
      console.log("Удаляется группа " + this.currentGroup)
      $.ajax({
        url: this.$hostname + "time-tracking/group",
        type: "DELETE",
        data: {
          id: this.currentGroup
        },
        success: () => {
          console.log("Даннные удалены")
          this.confirmDeleteGroup = false
          this.loadData()
        },
        error: (response) => {
          switch (response.status) {
            case 500:
              this.alertMsg = "Ошибка соединения с сервером"
              break
            case 400:
              this.alertMsg = "Ошибка в данных"
              break
            case 401:
              this.$refresh()
              break
            case 403:
              this.alertMsg = "Нет доступа"
              break
            default:
              this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    }
  },
}
</script>

<style scoped>

</style>