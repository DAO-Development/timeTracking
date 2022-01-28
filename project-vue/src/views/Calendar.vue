<template>
  <div class="flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Календарь</h1>
      <v-btn class="action-btn" color="primary" @click="formTitle='Добавление'; addForm = true">Добавить событие</v-btn>
      <div class="calendar">
        <v-row class="fill-height">
          <v-col>
            <v-sheet height="64">
              <v-toolbar flat>
                <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
                  Сегодня
                </v-btn>
                <v-btn fab text small color="grey darken-2" @click="$refs.calendar.prev()">
                  <v-icon small> mdi-chevron-left</v-icon>
                </v-btn>
                <v-btn fab text small color="grey darken-2" @click="$refs.calendar.next()">
                  <v-icon small> mdi-chevron-right</v-icon>
                </v-btn>
                <v-toolbar-title v-if="$refs.calendar">
                  {{ $refs.calendar.title }}
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-menu bottom right>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn outlined color="grey darken-2" v-bind="attrs" v-on="on">
                      <span>{{ typeToLabel[type] }}</span>
                      <v-icon right> mdi-menu-down</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="type = 'day'">
                      <v-list-item-title> День</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="type = 'month'">
                      <v-list-item-title>Месяц</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-toolbar>
            </v-sheet>
            <v-sheet height="600">
              <v-calendar ref="calendar" v-model="focus" color="primary" :events="events"
                          :type="type"
                          @click:event="showEvent"
                          @click:more="viewDay"
                          @click:date="viewDay"
              ></v-calendar>
              <v-menu v-model="selectedOpen" :close-on-content-click="false" :activator="selectedElement" offset-x>
                <v-card color="grey lighten-4" min-width="350px" flat>
                  <v-toolbar :color="selectedEvent.color" dark>
                    <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn icon @click="openEditForm">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon @click="confirmDeleteDialog=true">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-toolbar>
                  <v-card-text>
                    <span v-html="selectedEvent.description"></span>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn text color="secondary" @click="selectedOpen = false">
                      Закрыть
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-menu>
            </v-sheet>
          </v-col>
        </v-row>
      </div>
    </section>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="addForm = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="form" :model="newEvent">
            <h3>Для кого событие</h3>
            <v-row>
              <v-checkbox v-if="$parent.$parent.admin" label="Для себя" v-model="newEvent.self"
                          :disabled="newEvent.group !== null || newEvent.profile !== null || newEvent.all"></v-checkbox>
              <v-checkbox v-if="$parent.$parent.admin" label="Для всех" v-model="newEvent.all"
                          :disabled="newEvent.group !== null || newEvent.profile !== null || newEvent.self"></v-checkbox>
            </v-row>
            <v-row>
              <v-autocomplete v-if="$parent.$parent.admin" v-model="newEvent.group" label="Для группы"
                              :items="groups" item-text="name" item-value="id" :rules="userGroupRules"
                              :disabled="newEvent.profile !== null || newEvent.self|| newEvent.all"
                              clearable></v-autocomplete>
              <v-autocomplete v-if="$parent.$parent.admin" v-model="newEvent.profile" label="Для пользователя"
                              :items="profiles" item-text="label" item-value="id" :rules="userGroupRules"
                              :disabled="newEvent.group !== null  || newEvent.self || newEvent.all"
                              clearable></v-autocomplete>
            </v-row>
            <v-text-field v-model="newEvent.name" label="Название" :rules="reqRules"></v-text-field>
            <h3>Сроки</h3>
            <v-checkbox label="Весь день" v-model="newEvent.allDay"></v-checkbox>
            <v-row>
              <v-menu ref="dateStartMenu" v-model="menus.dateStartMenu"
                      :close-on-content-click="false"
                      :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newEvent.date_start" label="Дата" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="newEvent.date_start" @input="menus.dateStartMenu = false"></v-date-picker>
              </v-menu>
              <v-menu v-if="!newEvent.allDay" ref="menuStartTime" v-model="menus.timeStartMenu"
                      :close-on-content-click="false" :nudge-right="40" :return-value.sync="newEvent.time_start"
                      transition="scale-transition" offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newEvent.time_start" label="Время" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules" required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeStartMenu" v-model="newEvent.time_start" full-width format="24hr"
                               @click:minute="$refs.menuStartTime.save(newEvent.time_start)"></v-time-picker>
              </v-menu>
            </v-row>
            <v-row>
              <v-menu ref="dateEndMenu" v-model="menus.dateEndMenu"
                      :close-on-content-click="false"
                      :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newEvent.date_end" label="Дата конца" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="newEvent.date_end" @input="menus.dateEndMenu = false"></v-date-picker>
              </v-menu>
              <v-menu v-if="!newEvent.allDay" ref="menuEndTime" v-model="menus.timeEndMenu"
                      :close-on-content-click="false"
                      :nudge-right="40" :return-value.sync="newEvent.time_end" transition="scale-transition"
                      offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newEvent.time_end" label="Время конца" readonly v-bind="attrs"
                                v-on="on" outlined required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeEndMenu" v-model="newEvent.time_end" full-width format="24hr"
                               @click:minute="$refs.menuEndTime.save(newEvent.time_end)"></v-time-picker>
              </v-menu>
            </v-row>
            <v-autocomplete v-model="newEvent.color" :items="colors" label="Цвет" :rules="reqRules">
              <template v-slot:item="data">
                <v-list-item-avatar>
                  <v-chip :color="data.item"/>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{ data.item }}</v-list-item-title>
                </v-list-item-content>
              </template>
            </v-autocomplete>
            <v-textarea label="Описание" v-model="newEvent.description"></v-textarea>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addEvent">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление события
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить выбранное событие? Отменить это действие будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteEvent">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Header from "../components/Header";
import $ from "jquery";

export default {
  name: "Calendar",
  components: {Header},
  data: () => ({
    events: [],
    groups: [],
    profiles: [],
    focus: '',
    type: 'month',
    typeToLabel: {
      month: 'Месяц',
      day: 'День',
    },
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
    newEvent: {
      id: 0,
      self: false,
      all: false,
      group: null,
      profile: null,
      name: '',
      date_start: '',
      time_start: '',
      date_end: '',
      time_end: '',
      allDay: false,
      color: '',
      description: ''
    },
    menus: {
      dateStartMenu: false,
      dateEndMenu: false,
      timeStartMenu: false,
      timeEndMenu: false,
    },
    formTitle: 'Добавление',
    addForm: false,
    confirmDeleteDialog: false,
    alertError: false,
    alertMsg: "",
    reqRules: [
      v => !!v || 'Необходимо заполнить поле'
    ],
  }),
  computed: {
    userGroupRules() {
      const rules = []
      const rule =
          v => !!v || !!this.newEvent.group || !!this.newEvent.profile || this.newEvent.self || this.newEvent.all || 'Выберите для кого событие'
      rules.push(rule)
      return rules
    },
  },
  mounted() {
    this.$refs.calendar.checkChange()
  },
  created() {
    console.log("init Calendar")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      // if (this.$parent.$parent.read.indexOf('Бухгалтерия') === -1)
      //   this.$router.push({name: "Index"})
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      this.loadGroups()
      this.loadProfiles()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/calendar",
        type: "GET",
        success: (response) => {
          this.events = response.data.data
          this.events.forEach(event => {
            if (event.allDay) {
              event.start = event.start.substr(0, 10)
              event.end = event.end.substr(0, 10)
            } else {
              event.start = event.start.substr(0, 10) + ' ' + event.start.substr(11, 5)
              if (event.end !== null)
                event.end = event.end.substr(0, 10) + ' ' + event.end.substr(11, 5)
            }
            event.timed = !event.allDay
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
        }
      })
    },
    loadGroups() {
      $.ajax({
        url: this.$hostname + "time-tracking/groups",
        type: "GET",
        success: (response) => {
          this.groups = response.data.groups
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
    loadProfiles() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles/active",
        type: "GET",
        success: (response) => {
          this.profiles = response.data.data
          this.profiles.forEach(user => {
            user.label = user.lastname + ' ' + user.name + ', ' + user.position.name
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
        }
      })
    },
    addEvent() {
      if (this.$refs.form.validate()) {
        if (this.newEvent.self || this.newEvent.all) {
          this.newEvent.group = null
          this.newEvent.profile = null
        }
        this.newEvent.start = null
        this.newEvent.end = null
        if (this.newEvent.allDay) {
          this.newEvent.start = this.newEvent.date_start + ' ' + '00:00'
          if (this.newEvent.date_end !== '')
            this.newEvent.end = this.newEvent.date_end + ' ' + '00:00'
        } else {
          this.newEvent.start = this.newEvent.date_start + ' ' + this.newEvent.time_start
          if (this.newEvent.date_end !== '')
            this.newEvent.end = this.newEvent.date_end + ' ' + this.newEvent.time_end
        }
        if (this.newEvent.id) {
          this.putEvent()
        } else {
          $.ajax({
            url: this.$hostname + "time-tracking/calendar",
            type: "POST",
            data: {
              self: this.newEvent.self,
              group: this.newEvent.group,
              profile: this.newEvent.profile,
              name: this.newEvent.name,
              start: this.newEvent.start,
              end: this.newEvent.end,
              allDay: this.newEvent.allDay,
              color: this.newEvent.color,
              description: this.newEvent.description
            },
            success: () => {
              this.loadData()
              this.addForm = false
              this.newEvent = {
                self: false,
                group: null,
                profile: null,
                name: '',
                date_start: '',
                time_start: '',
                date_end: '',
                time_end: '',
                allDay: false,
                color: '',
                description: ''
              }
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
            }
          })
        }
      } else {
        this.alertMsg = "Заполните все необходимые поля"
        this.alertError = true
      }
    },
    putEvent() {
      $.ajax({
        url: this.$hostname + "time-tracking/calendar",
        type: "PUT",
        data: {
          id: this.newEvent.id,
          group: this.newEvent.group,
          profile: this.newEvent.profile,
          name: this.newEvent.name,
          start: this.newEvent.start,
          end: this.newEvent.end,
          allDay: this.newEvent.allDay,
          color: this.newEvent.color,
          description: this.newEvent.description
        },
        success: () => {
          this.loadData()
          this.addForm = false
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
        }
      })
    },
    deleteEvent() {
      $.ajax({
        url: this.$hostname + "time-tracking/calendar",
        type: "DELETE",
        data: {
          id: this.selectedEvent.id
        },
        success: () => {
          this.loadData()
          this.confirmDeleteDialog = false
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
        }
      })
    },
    openEditForm() {
      this.newEvent = this.selectedEvent
      this.newEvent.date_start = this.newEvent.start.substr(0, 10)
      this.newEvent.time_start = this.newEvent.start.substr(11, 5)
      if (this.newEvent.end !== null) {
        this.newEvent.date_end = this.newEvent.end.substr(0, 10)
        this.newEvent.time_end = this.newEvent.end.substr(11, 5)
      } else {
        this.newEvent.date_end = ''
        this.newEvent.time_end = ''
      }
      if (this.newEvent.group == null && this.newEvent.profile == null) {
        this.newEvent.all = true
      }
      this.addForm = true
    },
    viewDay({date}) {
      this.focus = date
      this.type = 'day'
    },
    getEventColor(event) {
      return event.color
    },
    setToday() {
      this.focus = ''
    },
    showEvent({nativeEvent, event}) {
      const open = () => {
        this.selectedEvent = event
        this.selectedElement = nativeEvent.target
        requestAnimationFrame(() => requestAnimationFrame(() => this.selectedOpen = true))
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        requestAnimationFrame(() => requestAnimationFrame(() => open()))
      } else {
        open()
      }

      nativeEvent.stopPropagation()
    },
  },
}
</script>

<style scoped>

</style>