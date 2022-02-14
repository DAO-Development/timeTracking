<template>
  <div class="index news flex-content">
    <Header/>
    <div class="summary-box">
      <h1>{{ $vuetify.lang.t('$vuetify.index.h1Label') }}</h1>
      <section v-if="auth">
        <div class="index__hello">
          {{ $vuetify.lang.t('$vuetify.index.hello') }} {{ user.name }} {{ user.lastname }}
        </div>
        <div class="index__today">
          <h2>{{ $vuetify.lang.t('$vuetify.index.todayLabel') }}</h2>
          <ul class="today-list">
            <li>
              <span class="today__unit bold-text">{{ $vuetify.lang.t('$vuetify.index.statistics.news.label') }}</span>
              <span class="today__quantity">{{ statistics.news }}
                {{ $vuetify.lang.t('$vuetify.index.statistics.news.text') }}</span>
            </li>
            <li>
              <span class="today__unit bold-text">{{ $vuetify.lang.t('$vuetify.index.statistics.workers.label') }}</span>
              <span class="today__quantity">{{ statistics.workers.all }} {{ $vuetify.lang.t('$vuetify.index.statistics.workers.all') }}</span>
              <span class="today__now">{{ $vuetify.lang.t('$vuetify.index.statistics.workers.new') }}: {{ statistics.workers.today }}</span>
              <span class="today__now">{{ $vuetify.lang.t('$vuetify.index.statistics.workers.text') }} {{ statistics.workers.in_work }}</span>
            </li>
            <li>
              <span class="today__unit bold-text">{{ $vuetify.lang.t('$vuetify.index.statistics.clients.label') }}</span>
              <span class="today__quantity">{{ statistics.clients.all }} {{ $vuetify.lang.t('$vuetify.index.statistics.clients.all') }}</span>
              <span class="today__now">{{ $vuetify.lang.t('$vuetify.index.statistics.clients.new') }}: {{ statistics.clients.today }}</span>
            </li>
            <li>
              <span class="today__unit bold-text">{{ $vuetify.lang.t('$vuetify.index.statistics.objects.label') }}</span>
              <span class="today__quantity">{{ statistics.objects.all }} {{ $vuetify.lang.t('$vuetify.index.statistics.objects.all') }}</span>
              <span class="today__now">{{ $vuetify.lang.t('$vuetify.index.statistics.objects.text') }}: {{ statistics.objects.in_work }}</span>
            </li>
            <li>
              <span class="today__unit bold-text">{{ $vuetify.lang.t('$vuetify.index.statistics.calendar.label') }}</span>
              <span class="today__quantity">12 {{ $vuetify.lang.t('$vuetify.index.statistics.calendar.all') }}</span>
              <span class="today__now">{{ $vuetify.lang.t('$vuetify.index.statistics.calendar.week') }}: </span>
              <span class="today__now">{{ $vuetify.lang.t('$vuetify.index.statistics.calendar.today') }}:</span>
            </li>
          </ul>
        </div>
      </section>
      <section v-if="auth" class="widgets">
        <div class="unit-title">
          <h1>{{ $vuetify.lang.t('$vuetify.widgets.h1Label') }}</h1>
          <v-btn color="primary" fab x-small @click="addWidgetForm = true">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </div>
        <div class="index__widgets">
          <template v-for="(note, i) in notes">
            <div class="widgets-single" :key="note.id">
              <div class="widgets-single__header">
                <h3>{{ $vuetify.lang.t('$vuetify.widgets.noteLabel') }} {{ i + 1 }}</h3>
                <div class="widgets-single__actions">
                  <v-btn color="error" fab x-small @click="deleteNote(note.id)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                  <v-btn color="primary" fab x-small>
                    <v-icon>mdi-autorenew</v-icon>
                  </v-btn>
                </div>
              </div>
              <div class="widgets-single__content">
                <div class="note__header">
                  {{ $vuetify.lang.t('$vuetify.widgets.lastSave') }}:
                  <span>{{ note.last_save }}</span>
                  <div class="widgets-single__actions">
                    <v-btn color="secondary" fab x-small @click="newNote = note; addNoteForm = true">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </div>
                </div>
                <div class="note__content" :style="'background: '+note.color">
                  <pre>{{ note.text }}</pre>
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
          <h2>Блокнот</h2>
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
      this.$emit('load-functions')
      this.$emit('load-settings')
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
        last_save: "",
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
            note.last_save = text + ' ' + date.toISOString().substring(0, 10) + ' ' + date.getHours() + ':' + date.getMinutes()
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
      this.newNote.color = this.color
      this.newNote.last_save = new Date().toISOString()
      if (this.newNote.id === 0)
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
      else
        this.putNote()
    },
    putNote() {
      $.ajax({
        url: this.$hostname + "time-tracking/notes",
        type: "PUT",
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
    deleteNote(id) {
      $.ajax({
        url: this.$hostname + "time-tracking/notes",
        type: "DELETE",
        headers: {"Authorization": "Token " + (localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token"))},
        data: {
          id: id
        },
        success: () => {
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