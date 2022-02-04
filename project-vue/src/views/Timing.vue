<template>
  <div class="timing flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Отчетность по проделанной работе</h1>
      <v-btn class="action-btn" color="primary" @click="addForm = true; formTitle='Добавление'">Добавить</v-btn>
      <div class="calendar">
        <v-row class="fill-height">
          <v-col>
            <v-sheet height="64">
              <v-toolbar flat>
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
                <!--                <v-menu bottom right>-->
                <!--                  <template v-slot:activator="{ on, attrs }">-->
                <!--                    <v-btn outlined color="grey darken-2" v-bind="attrs" v-on="on">-->
                <!--                      <span>{{ typeToLabel[type] }}</span>-->
                <!--                      <v-icon right> mdi-menu-down</v-icon>-->
                <!--                    </v-btn>-->
                <!--                  </template>-->
                <!--                  <v-list>-->
                <!--                    <v-list-item @click="type = 'day'">-->
                <!--                      <v-list-item-title> День</v-list-item-title>-->
                <!--                    </v-list-item>-->
                <!--                    <v-list-item @click="type = 'month'">-->
                <!--                      <v-list-item-title>Месяц</v-list-item-title>-->
                <!--                    </v-list-item>-->
                <!--                  </v-list>-->
                <!--                </v-menu>-->
              </v-toolbar>
            </v-sheet>
            <v-sheet height="600">
              <v-calendar ref="calendar" v-model="focus" color="primary" :events="timings"
                          :type="type"
                          @click:event="showEvent"
              ></v-calendar>
              <v-menu v-model="selectedOpen" :close-on-content-click="false" :activator="selectedElement" offset-x>
                <v-card color="grey lighten-4" min-width="350px" flat>
                  <v-toolbar color="primary" dark>
                    <v-toolbar-title v-html="selectedEvent.position"></v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn v-if="$parent.$parent.admin" icon
                           @click="newTiming=selectedEvent; addForm=true;formTitle='Редактирование'">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn v-if="$parent.$parent.admin" icon @click="confirmDeleteDialog=true">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-toolbar>
                  <v-card-text>
                    <div>{{ selectedEvent.date }} {{ selectedEvent.time_start }}-{{ selectedEvent.time_end }}</div>
                    <span v-html="selectedEvent.comment"></span>
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
        <h3>Добавление</h3>
        <v-card-text>
          <v-form ref="form" :model="newTiming">
            <v-row>
              <v-menu ref="dateMenu" v-model="menus.dateMenu"
                      :close-on-content-click="false"
                      :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newTiming.date" label="Дата" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="newTiming.date" @input="menus.dateMenu = false"></v-date-picker>
              </v-menu>
            </v-row>
            <v-autocomplete label="Выберите объект" v-model="newTiming.objects_id" :items="objects" item-text="label"
                            item-value="id" :rules="reqRules"></v-autocomplete>
            <v-combobox label="Профиль работ" v-model="newTiming.position" :items="positions"
                        :rules="reqRules"></v-combobox>
            <v-row>
              <v-menu ref="menuStartTime" v-model="menus.timeStartMenu"
                      :close-on-content-click="false" :nudge-right="40" :return-value.sync="newTiming.time_start"
                      transition="scale-transition" offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newTiming.time_start" label="Время начала" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules" required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeStartMenu" v-model="newTiming.time_start" full-width format="24hr"
                               @click:minute="$refs.menuStartTime.save(newTiming.time_start)"></v-time-picker>
              </v-menu>
              <v-menu ref="menuEndTime" v-model="menus.timeEndMenu" :close-on-content-click="false"
                      :nudge-right="40" :return-value.sync="newTiming.time_end" transition="scale-transition"
                      offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newTiming.time_end" label="Время окончания" readonly v-bind="attrs"
                                v-on="on" outlined required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeEndMenu" v-model="newTiming.time_end" full-width format="24hr"
                               @click:minute="$refs.menuEndTime.save(newTiming.time_end)"></v-time-picker>
              </v-menu>
            </v-row>
            <v-textarea label="Описание" v-model="newTiming.comment"></v-textarea>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="openConfirmAdd">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmAddDialog" max-width="500">
      <v-card>
        <v-card-title>
          Подтверждение
        </v-card-title>
        <v-card-text>Проверьте корректность всех данных. Внести изменения сможет только администратор</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmAddDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="addTiming">Подтвердить</v-btn>
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
import $ from "jquery";

export default {
  name: "Timing",
  components: {Header},
  data() {
    return {
      timings: [],
      objects: [],
      positions: [],
      newTiming: {
        id: 0,
        date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        time_start: '',
        time_end: '',
        position: '',
        objects_id: '',
        user_profile_id: null,
        comment: ''
      },
      focus: '',
      type: 'month',
      selectedEvent: {},
      selectedOpen: false,
      selectedElement: null,
      menus: {
        dateMenu: false,
        timeStartMenu: false,
        timeEndMenu: false,
      },
      formTitle: '',
      addForm: false,
      confirmAddDialog: false,
      confirmDeleteDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
    }
  },
  created() {
    console.log("init Timing")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      // if (this.$parent.$parent.read.indexOf('Бухгалтерия') === -1)
      //   this.$router.push({name: "Index"})
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      this.loadObjects()
      this.loadPositions()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/time-reports",
        type: "GET",
        success: (response) => {
          this.timings = response.data.data
          this.timings.forEach(timing => {
            timing.start = timing.date + ' ' + timing.time_start
            timing.end = timing.date + ' ' + timing.time_end
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
    loadObjects() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "GET",
        success: (response) => {
          this.objects = response.data.data
          this.objects.forEach(object => {
            object.label = object.city + ' ' + object.street + ' ' + object.house
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
    loadPositions() {
      $.ajax({
        url: this.$hostname + "time-tracking/time-reports/positions",
        type: "GET",
        success: (response) => {
          this.positions = response.data.positions
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
    openConfirmAdd() {
      if (this.$refs.form.validate()) {
        if (this.$parent.$parent.admin) {
          this.addTiming()
        } else
          this.confirmAddDialog = true
      } else {
        this.alertMsg = "Заполните все необходимые поля"
        this.alertError = true
      }
    },
    addTiming() {
      if (this.newTiming.id !== 0) {
        this.putTiming()
      } else {
        $.ajax({
          url: this.$hostname + "time-tracking/time-reports",
          type: "POST",
          data: this.newTiming,
          success: () => {
            this.loadData()
            this.loadPositions()
            this.addForm = false
            this.confirmAddDialog = false
            this.newTiming = {
              date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
              time_start: '',
              time_end: '',
              position: '',
              objects_id: '',
              user_profile_id: '',
              comment: ''
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
          },
        })
      }
    },
    putTiming() {
      $.ajax({
        url: this.$hostname + "time-tracking/time-reports",
        type: "PUT",
        data: this.newTiming,
        success: () => {
          this.loadData()
          this.loadPositions()
          this.addForm = false
          this.confirmAddDialog = false
          this.newTiming = {
            date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
            time_start: '',
            time_end: '',
            position: '',
            objects_id: '',
            user_profile_id: '',
            comment: ''
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
        },
      })
    },
    deleteTiming() {
      $.ajax({
        url: this.$hostname + "time-tracking/time-reports",
        type: "DELETE",
        data: {id: this.selectedEvent.id},
        success: () => {
          this.loadData()
          this.loadPositions()
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
        },
      })
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
  }
}
</script>

<style scoped>

</style>