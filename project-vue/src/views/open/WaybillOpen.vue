<template>
  <div class="waybill flex-content">
    <Header/>
    <section class="summary-box">
      <div class="summary-box__title">
        <h1>Путевые листы</h1>
        <div class="addition-btn" @click="$router.push({name: 'Waybill'})">
          <span>К списку путевых листов</span>
          <back-icon/>
        </div>
      </div>
      <ul>
        <li>
          <span class="title">Начало поездки</span>
          <span class="content">{{ newWaybill.date_start }} {{ newWaybill.time_start }}</span>
        </li>
        <li>
          <span class="title">Конец поездки</span>
          <span class="content">{{ newWaybill.date_end }}-{{ newWaybill.time_end }}</span>
        </li>
        <li>
          <span class="title">Пункт отправления</span>
          <span class="content">{{ newWaybill.departure }}</span>
        </li>
        <li>
          <span class="title">Пункт назначения</span>
          <span class="content">{{ newWaybill.destination }}</span>
        </li>
        <li>
          <span class="title">Километраж</span>
          <span class="content">{{ newWaybill.kilometrage_end - newWaybill.kilometrage_start }}</span>
        </li>
        <li>
          <span class="title">Работник</span>
          <span class="content">{{ newWaybill.user_profile.name }}
            {{ newWaybill.user_profile.lastname }} ({{ newWaybill.user_profile.position.name }})</span>
        </li>
        <li>
          <span class="title">Цель поездки</span>
          <span class="content">{{ newWaybill.goal.name }}</span>
        </li>
        <h3>Автомобиль</h3>
        <li>
          <span class="title">Марка</span>
          <span class="content">{{ newWaybill.auto_mark }}</span>
        </li>
        <li>
          <span class="title">Коробка</span>
          <span class="content">{{ newWaybill.auto_type }}</span>
        </li>
        <li>
          <span class="title">Топливо</span>
          <span class="content">{{ newWaybill.auto_fuel }}</span>
        </li>
      </ul>
      <v-btn class="action-btn" color="primary" @click="loadGoals; addForm = true"
             v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1">
        Редактировать
      </v-btn>
      <v-btn class="action-btn" color="primary" @click="confirmDeleteDialog = true"
             v-if="$parent.$parent.edit.indexOf('Бухгалтерия') !== -1">
        Удалить
      </v-btn>
    </section>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="addForm = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>Редактирование</h3>
        <v-card-text>
          <v-form ref="form" :model="newWaybill">
            <v-row>
              <v-menu ref="dateStartMenu" v-if="$parent.$parent.admin" v-model="menus.dateStartMenu"
                      :close-on-content-click="false"
                      :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newWaybill.date_start" label="Дата начала поездки" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="newWaybill.date_start" @input="menus.dateStartMenu = false"></v-date-picker>
              </v-menu>
              <v-menu ref="dateEndMenu" v-if="$parent.$parent.admin" v-model="menus.dateEndMenu"
                      :close-on-content-click="false"
                      :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newWaybill.date_end" label="Дата окончания поездки" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="newWaybill.date_end" @input="menus.dateEndMenu = false"></v-date-picker>
              </v-menu>
            </v-row>
            <v-text-field v-if="!$parent.$parent.admin" v-model="newWaybill.date_start" label="Дата начала поездки"
                          outlined
                          disabled></v-text-field>
            <v-text-field v-if="!$parent.$parent.admin" v-model="newWaybill.date_end" label="Дата окончания поездки"
                          outlined
                          disabled></v-text-field>
            <v-text-field v-model="newWaybill.departure" label="Пункт отправления" outlined :rules="reqRules"
                          required></v-text-field>
            <v-text-field v-model="newWaybill.destination" label="Пункт назначения" outlined :rules="reqRules"
                          required></v-text-field>
            <h3>Километраж</h3>
            <v-row>
              <v-text-field type="number" v-model="newWaybill.kilometrage_start" label="Перед поездкой" outlined
                            :rules="reqRules"
                            required></v-text-field>
              <v-text-field type="number" v-model="newWaybill.kilometrage_end" label="После поездки" outlined
                            :rules="reqRules"
                            required></v-text-field>
              <div>{{ newWaybill.kilometrage_end - newWaybill.kilometrage_start }}</div>
            </v-row>
            <v-row>
              <v-menu ref="menuStartTime" v-model="menus.timeStartMenu" :close-on-content-click="false"
                      :nudge-right="40" :return-value.sync="newWaybill.time_start" transition="scale-transition"
                      offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newWaybill.time_start" label="Время начала поездки" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules" required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeStartMenu" v-model="newWaybill.time_start" full-width format="24hr"
                               @click:minute="$refs.menuStartTime.save(newWaybill.time_start)"></v-time-picker>
              </v-menu>
              <v-menu ref="menuEndTime" v-model="menus.timeEndMenu" :close-on-content-click="false"
                      :nudge-right="40" :return-value.sync="newWaybill.time_end" transition="scale-transition"
                      offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newWaybill.time_end" label="Время конца поездки" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules" required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeEndMenu" v-model="newWaybill.time_end" full-width format="24hr"
                               @click:minute="$refs.menuEndTime.save(newWaybill.time_end)"></v-time-picker>
              </v-menu>
            </v-row>
            <v-autocomplete v-model="newWaybill.goal" :items="goals" item-text="name" item-value="id"
                            label="Цель поездки" :rules="reqRules" required outlined>
              <template v-slot:no-data>
                <v-list-item>
                  <v-list-item-title>
                    Искомая цель поездки не создана. Обратитесь к администратору
                  </v-list-item-title>
                </v-list-item>
              </template>
            </v-autocomplete>
            <h3>Автомобиль</h3>
            <v-row>
              <v-text-field v-model="newWaybill.auto_mark" label="Марка" outlined :rules="reqRules"
                            required></v-text-field>
              <v-select v-model="newWaybill.auto_type" label="Тип коробки" outlined :rules="reqRules"
                        required :items="selectType"></v-select>
              <v-select v-model="newWaybill.auto_fuel" label="Тип топлива" outlined :rules="reqRules"
                        required :items="selectFuel"></v-select>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn class="action-btn" color="primary" @click="putWaybill">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление путевого листа
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить путевой лист? Отменить это действие будет невозможно</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteWaybill">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Header from "../../components/Header";
import $ from "jquery";
import BackIcon from "../../components/icons/backIcon";

export default {
  name: "WaybillOpen",
  components: {BackIcon, Header},
  props: {
    id: [String, Number]
  },
  data() {
    return {
      goals: [],
      newWaybill: {
        id: 0,
        date_start: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        date_end: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        departure: '',
        destination: '',
        kilometrage_start: '',
        kilometrage_end: '',
        time_start: '',
        time_end: '',
        goal: '',
        auto_mark: '',
        auto_type: '',
        auto_fuel: '',
        user_profile: {
          name: '',
          lastname: '',
          position: {name: ''}
        },
      },
      selectType: ['Автомат', 'Механика'],
      selectFuel: ['Дизель', 'Бензин', 'Электро'],
      menus: {
        dateStartMenu: false,
        dateEndMenu: false,
        timeStartMenu: false,
        timeEndMenu: false,
      },
      addForm: false,
      confirmDeleteDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
    }
  },
  created() {
    console.log("init Waybills")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      if (this.$parent.$parent.read.indexOf('Бухгалтерия') !== -1)
        this.loadGoals()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/waybill/" + this.id,
        type: "GET",
        success: (response) => {
          this.newWaybill = response.data.data[0]
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
        }
      })
    },
    loadGoals() {
      $.ajax({
        url: this.$hostname + "time-tracking/waybill/goal",
        type: "GET",
        success: (response) => {
          this.goals = response.data.data
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
        }
      })
    },
    putWaybill() {
      if (this.$refs.form.validate()) {
        $.ajax({
          url: this.$hostname + "time-tracking/waybill",
          type: "PUT",
          data: this.newWaybill,
          success: () => {
            this.loadData()
            this.addForm = false
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
          }
        })
      }
    },
    deleteWaybill() {
      $.ajax({
        url: this.$hostname + "time-tracking/waybill",
        type: "DELETE",
        data: {
          id: this.id,
        },
        success: () => {
          this.confirmDeleteDialog = false
          this.$router.push({name: 'Waybill'})
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
        }
      })
    },
  }
}
</script>

<style scoped>

</style>