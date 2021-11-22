<template>
  <div class="index news flex-content">
    <Header/>
    <div class="summary-box">
      <h1>Главная</h1>
      <section v-if="auth">
        <div class="index__hello">
          Добро пожаловать, {{ user.name }} {{ user.lastname }}
        </div>
        <div class="index__today">
          <h2>На сегодня</h2>
          <ul class="today-list">
            <li>
              <span class="today__unit bold-text">Новости:</span>
              <span class="today__quantity">{{ statistics.news }} новостей</span>
            </li>
            <li>
              <span class="today__unit bold-text">Работники:</span>
              <span class="today__quantity">{{ statistics.workers.all }} работников</span>
              <span class="today__now">Новых на сегодня: {{ statistics.workers.today }}</span>
              <span class="today__now">Работает: {{ statistics.workers.in_work }}</span>
            </li>
            <li>
              <span class="today__unit bold-text">Клиенты:</span>
              <span class="today__quantity">{{ statistics.clients.all }} клиентов</span>
              <span class="today__now">Новых на сегодня: {{ statistics.clients.today }}</span>
            </li>
            <li>
              <span class="today__unit bold-text">Объекты:</span>
              <span class="today__quantity">{{ statistics.objects.all }} объектов</span>
              <span class="today__now">В работе: {{ statistics.objects.in_work }}</span>
            </li>
            <li>
              <span class="today__unit bold-text">Календарь:</span>
              <span class="today__quantity">12 события</span>
              <span class="today__now">На этой неделе: </span>
              <span class="today__now">Сегодня:</span>
            </li>
          </ul>
        </div>
      </section>
      <section v-if="auth" class="widgets">
        <div class="unit-title">
          <h1>Виджеты</h1>
          <v-btn color="primary" fab x-small @click="addWidgetForm = true">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </div>
        <div class="index__widgets">
          <template v-for="(note, i) in notes">
            <div class="widgets-single" :key="note.id">
              <div class="widgets-single__header">
                <h3>Блокнот {{ i + 1 }}</h3>
                <div class="widgets-single__actions">
                  <v-btn color="error" fab x-small @click="addWidgetForm = true">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                  <v-btn color="primary" fab x-small @click="addWidgetForm = true">
                    <v-icon>mdi-autorenew</v-icon>
                  </v-btn>
                </div>
              </div>
              <div class="widgets-single__content">
                <div class="note__header">
                  Последнее сохранение:
                  <span>{{ note.last_save }}</span>
                  <div class="widgets-single__actions">
                    <v-btn color="secondary" fab x-small @click="addWidgetForm = true">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </div>
                </div>
                <div class="note__content" :style="'background: '+note.color">
                  {{ note.text }}
                </div>
              </div>
            </div>
          </template>
        </div>
      </section>
      <div v-if="!auth" class="news-all all">
        <div class="news-all__grid">
          <template v-for="item in news">
            <v-card class="news-single" :key="item.id" color="primary" v-if="item.photo_path"
                    @click="$router.push({name: 'NewOpen', params: {id: item.id}})"
                    v-bind:style="{'background-image': 'url('+$hostname+'media'+item.photo_path+ ')', 'background-size': 'cover', 'background-position': 'center'}">
              <div class="news-single__title">{{ item.title }}</div>
              <div class="news-single__text" v-html="item.text"></div>
            </v-card>
            <v-card class="news-single" :key="item.id" color="primary" v-else
                    @click="$router.push({name: 'NewOpen', params: {currentNew: item, id: item.id}})">
              <div class="news-single__title">{{ item.title }}</div>
              <div class="news-single__text" v-html="item.text"></div>
            </v-card>
          </template>
        </div>
      </div>
    </div>

    <v-btn v-if="!auth" class="action-btn" color="primary" @click="goLogin">Войти</v-btn>
    <v-dialog max-width="500px" v-model="addWidgetForm">
      <v-card>
        <v-card-title>
          Выберите виджет
        </v-card-title>
        <v-card-text>
          <v-list dense>
            <v-list-item-group>
              <v-list-item @click="openAddNote">
                <v-list-item-icon>
                  <v-icon>mdi-text</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Блокнот</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog max-width="500px" v-model="addNoteForm">
      <v-card>
        <v-card-text>
          <v-textarea v-model="newNote.text" filled :style="'background: '+color"></v-textarea>
          <!--          <v-menu ref="menu_color" v-model="color" :close-on-content-click="true"-->
          <!--                  :return-value.sync="color"-->
          <!--                  transition="scale-transition" offset-y min-width="auto">-->
          <!--            <template v-slot:activator="{ on, attrs }">-->
          <!--              <v-text-field v-model="color" placeholder="Цвет" readonly v-bind="attrs"-->
          <!--                            v-on="on" outlined></v-text-field>-->
          <!--            </template>-->
          <v-color-picker v-model="color"></v-color-picker>
          <!--          </v-menu>-->
        </v-card-text>
        <v-card-actions>
          <v-btn color="secondary" @click="closeNoteForm">Отменить</v-btn>
          <v-btn color="primary" @click="saveNote">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import $ from "jquery";
import Header from "../components/Header";

export default {
  name: "Index",
  components: {Header},
  created() {
    console.log("init Index")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.auth = true
    }
    this.loadData()
  },
  data() {
    return {
      auth: false,
      news: {},
      user: {},
      statistics: {
        news: 0,
        workers: {},
        clients: {},
        objects: {},
      },
      widgets: [],
      notes: [],
      newNote: {
        id: 0,
        color: "",
        text: "",
      },
      addWidgetForm: false,
      addNoteForm: false,
      hex: '#FFC6C6',
    }
  },
  computed: {
    color: {
      get() {
        return this['hex']
      },
      set(v) {
        this['hex'] = v
      },
    },
  },
  methods: {
    goLogin() {
      this.$router.push({name: "Login"})
    },
    loadData() {
      if (this.auth) {
        $.ajax({
          url: this.$hostname + "time-tracking/user",
          type: "GET",
          headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
          success: (response) => {
            this.user = response.data.data
          },
          error: (response) => {
            if (response.status === 500) {
              this.alertMsg = "Ошибка соединения с сервером"
            } else if (response.status === 401) {
              this.$refresh()
            } else {
              this.alertMsg = "Непредвиденная ошибка"
            }
            this.alertError = true
          },
        })
        this.loadStatistics()
        this.loadNotes()
      } else {
        $.ajax({
          url: this.$hostname + "time-tracking/news",
          type: "GET",
          success: (response) => {
            this.news = response.data.data
          },
          error: (response) => {
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            console.log(response.data)
          },
        })
      }
    },
    loadStatistics() {
      $.ajax({
        url: this.$hostname + "time-tracking/statistics",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          this.statistics = response.data
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    },
    loadNotes() {
      $.ajax({
        url: this.$hostname + "time-tracking/notes",
        type: "GET",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        success: (response) => {
          this.notes = response.data.data
          this.notes.forEach(note => {
            let date = new Date(note.last_save)
            let text = ''
            switch (date.getDay()) {
              case 1:
                text += 'Понедельник'
                break
              case 2:
                text += 'Вторник'
                break
              case 3:
                text += 'Среда'
                break
              case 4:
                text += 'Четверг'
                break
              case 5:
                text += 'Пятница'
                break
              case 6:
                text += 'Суббота'
                break
              case 7:
                text += 'Воскресенье'
                break
            }
            note.last_save = text + ' ' + date.toISOString().substring(0, 10) + ' ' + date.toISOString().substring(11, 16)
          })
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    },
    saveNote() {
      console.log(this.color)
      console.log(this.newNote.text)
      this.newNote.color = this.color
      $.ajax({
        url: this.$hostname + "time-tracking/notes",
        type: "POST",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        data: this.newNote,
        success: () => {
          this.closeNoteForm()
          this.loadNotes()
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else if (response.status === 401) {
            this.$refresh()
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        },
      })
    },
    closeNoteForm() {
      this.addNoteForm = false
      this.newNote = {
        id: 0,
        color: "",
        text: ""
      }
    },
    openAddNote() {
      this.addWidgetForm = false
      this.addNoteForm = true
    },
  }
}
</script>

<style scoped>

</style>