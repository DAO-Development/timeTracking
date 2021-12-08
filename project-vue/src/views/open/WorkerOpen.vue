<template>
  <div class="clients flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Работники</h3>
        <div class="addition-btn" @click="$router.push({name: 'Workers'})">
          <span>К списку клиентов</span>
          <back-icon/>
        </div>
      </div>
      <div class="workers-open">
        <div class="profile__image">
          <v-img
              v-if="currentProfile.photo_path" :lazy-src="$hostname+'media'+currentProfile.photo_path"
              :src="$hostname+'media'+currentProfile.photo_path"></v-img>
          <div class="profile__change-photo" @click="photoDialog = true">Сменить фото</div>
        </div>
        <div class="profile__info">
          <h3>Личная информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Имя</span>
              <span class="profile__info-content">{{ currentProfile.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Фамилия</span>
              <span class="profile__info-content">{{ currentProfile.lastname }}</span>
            </li>
            <li>
              <span class="profile__info-title">Дата рождения</span>
              <span class="profile__info-content">{{ currentProfile.birthdate }}</span>
            </li>
            <li>
              <span class="profile__info-title">Гражданство</span>
              <span class="profile__info-content">{{ currentProfile.citizenship }}</span>
            </li>
            <li>
              <span class="profile__info-title">Должность</span>
              <span class="profile__info-content">{{ currentProfile.position.name }}</span>
            </li>
            <li @click="changeGroupForm = true">
              <span class="profile__info-title">Роль</span>
              <span class="profile__info-content">{{ currentGroup.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Номер соц. страхования</span>
              <span class="profile__info-content">{{ currentProfile.social_code_own }}</span>
            </li>
            <li>
              <span class="profile__info-title">Финский номер соц. страхования</span>
              <span class="profile__info-content">{{ currentProfile.social_code_fin }}</span>
            </li>
            <li>
              <span class="profile__info-title">Работает</span>
              <v-checkbox v-model="currentProfile.active" :disabled="$parent.$parent.edit.indexOf('Работники') === -1"
                          @change="openConfirmArchiveDialog"></v-checkbox>
            </li>
          </ul>
          <h3>Контакты</h3>
          <ul>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentProfile.phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">Телефон в Финляндии</span>
              <span class="profile__info-content">{{ currentProfile.phone_fin }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentProfile.auth_user_id.email }}</span>
            </li>
          </ul>
          <h3>Банковская информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Налоговый номер</span>
              <span class="profile__info-content">{{ currentProfile.tax_number }}</span>
            </li>
            <li>
              <span class="profile__info-title">Счет в банке</span>
              <span class="profile__info-content">{{ currentProfile.bank_account }}</span>
            </li>
          </ul>
          <div class="profile__info profile__info-full" v-if="full">
            <h3>Адреса</h3>
            <ul>
              <li>
                <span class="profile__info-title">Адрес в своей стране</span>
                <span class="profile__info-content"
                      v-if="currentProfile.address_own !== null && currentProfile.address_own.city !== ''">{{
                    currentProfile.address_own.index
                  }} {{ currentProfile.address_own.country }}, г.{{
                    currentProfile.address_own.city
                  }}, {{ currentProfile.address_own.street }}, д.{{
                    currentProfile.address_own.house
                  }}, {{ currentProfile.address_own.entrance }}, кв.{{ currentProfile.address_own.flat }}</span>
              </li>
              <li>
                <span class="profile__info-title">Адрес в Финляндии</span>
                <span class="profile__info-content"
                      v-if="currentProfile.address_fin !== null && currentProfile.address_fin.city !== ''">{{
                    currentProfile.address_fin.index
                  }} {{ currentProfile.address_fin.country }}, г.{{
                    currentProfile.address_fin.city
                  }}, {{ currentProfile.address_fin.street }}, д.{{
                    currentProfile.address_fin.house
                  }}, {{ currentProfile.address_fin.entrance }}, кв.{{ currentProfile.address_fin.flat }}</span>
              </li>
            </ul>
            <h3>Одежда (размеры)</h3>
            <ul>
              <li>
                <span class="profile__info-title">Ботинки</span>
                <span class="profile__info-content">{{ currentProfile.boots }}</span>
              </li>
              <li>
                <span class="profile__info-title">Куртка</span>
                <span class="profile__info-content">{{ currentProfile.jacket }}</span>
              </li>
              <li>
                <span class="profile__info-title">Штаны</span>
                <span class="profile__info-content">{{ currentProfile.pants }}</span>
              </li>
              <li>
                <span class="profile__info-title">Футболка</span>
                <span class="profile__info-content">{{ currentProfile.shirt }}</span>
              </li>
            </ul>
            <h3>Языки</h3>
            <ul>
              <li>
                <span class="profile__info-title">Русский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.russian" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Английский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.english" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Эстонский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.estonian" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Финский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.finnish" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Другие</span>
                <span class="profile__info-content">{{ currentProfile.other_language }}</span>
              </li>
            </ul>
            <h3>Другое</h3>
            <ul>
              <li>
                <span class="profile__info-title">Свой автомобиль</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.auto" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Свой инструмент</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.tool" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Навыки</span>
                <span class="profile__info-content">{{ currentProfile.skills }}</span>
              </li>
            </ul>
          </div>
          <div class="open__actions">
            <div class="addition-btn" @click="full = !full">
              <span v-if="full">Скрыть полную информацию</span>
              <span v-if="!full">Показать полную информацию</span>
            </div>
            <div class="addition-btn"
                 @click="$router.push({name: 'Documents', params: {type: 'worker', id: currentProfile.id}})">
              Документы
            </div>
          </div>
          <div v-if="$parent.$parent.edit.indexOf('Работники') !== -1" class="news-open__actions open__actions">
            <div class="addition-btn" @click="openEditForm()">
              <edit-icon/>
              Редактировать работника
            </div>
            <div class="addition-btn" @click="confirmDeleteDialog = true">
              <waste-icon/>
              Удалить работника
            </div>
          </div>
        </div>
      </div>
    </div>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="addForm=false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="addForm" :model="currentProfile">
            <v-row>
              <v-text-field placeholder="Фамилия*" v-model="currentProfile.lastname" :rules="reqRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Имя*" v-model="currentProfile.name" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Гражданство*" v-model="currentProfile.citizenship" :rules="reqRules"
                            required outlined></v-text-field>
              <v-menu ref="menu" v-model="menu" :close-on-content-click="false"
                      :return-value.sync="currentProfile.birthdate"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="currentProfile.birthdate" readonly v-bind="attrs" v-on="on"
                                placeholder="Дата рождения*" :rules="reqRules" outlined></v-text-field>
                </template>
                <v-date-picker v-model="currentProfile.birthdate" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="menu = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu.save(currentProfile.birthdate)"> OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-row>
            <v-row>
              <v-text-field placeholder="Номер социального страхования" v-model="currentProfile.social_code_own"
                            outlined></v-text-field>
              <v-text-field placeholder="Номер соц. страхования в Финляндии*" v-model="currentProfile.social_code_fin"
                            :rules="reqRules" required outlined></v-text-field>
            </v-row>
            <h4>Адрес в своей стране</h4>
            <v-row>
              <v-text-field placeholder="Страна" v-model="currentProfile.address_own.country" outlined></v-text-field>
              <v-text-field placeholder="Город" v-model="currentProfile.address_own.city" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Улица" v-model="currentProfile.address_own.street" outlined></v-text-field>
              <v-text-field placeholder="Индекс" v-model="currentProfile.address_own.index" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом" v-model="currentProfile.address_own.house" outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="currentProfile.address_own.entrance" outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="currentProfile.address_own.flat" outlined></v-text-field>
            </v-row>
            <h4>Адрес в Финляндии</h4>
            <v-row>
              <v-text-field placeholder="Страна" v-model="currentProfile.address_fin.country" outlined></v-text-field>
              <v-text-field placeholder="Город" v-model="currentProfile.address_fin.city" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Улица" v-model="currentProfile.address_fin.street" outlined></v-text-field>
              <v-text-field placeholder="Индекс" v-model="currentProfile.address_fin.index" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом" v-model="currentProfile.address_fin.house" outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="currentProfile.address_fin.entrance" outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="currentProfile.address_fin.flat" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Телефон" v-model="currentProfile.phone" :rules="phoneRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Телефон в Финляндии*" v-model="currentProfile.phone_fin" :rules="phoneFinRules"
                            required outlined></v-text-field>
            </v-row>
            <v-text-field placeholder="Почта*" v-model="currentProfile.auth_user_id.email" :rules="emailRules" required
                          outlined></v-text-field>
            <v-text-field placeholder="Номер счета в банке*" v-model="currentProfile.bank_account" :rules="reqRules"
                          required outlined></v-text-field>
            <v-text-field placeholder="Налоговый номер*" v-model="currentProfile.tax_number" :rules="reqRules" required
                          outlined></v-text-field>
            <v-row>
              <v-checkbox label="Свой автомобиль" v-model="currentProfile.auto"></v-checkbox>
              <v-checkbox label="Свой инструмент" v-model="currentProfile.tool"></v-checkbox>
            </v-row>
            <h4>Языки</h4>
            <v-row>
              <v-checkbox label="Английский" v-model="currentProfile.english"></v-checkbox>
              <v-checkbox label="Финский" v-model="currentProfile.finnish"></v-checkbox>
              <v-checkbox label="Русский" v-model="currentProfile.russian"></v-checkbox>
              <v-checkbox label="Эстонский" v-model="currentProfile.estonian"></v-checkbox>
            </v-row>
            <v-text-field placeholder="Другие языки" v-model="currentProfile.other_language" outlined></v-text-field>
            <v-combobox ref="positionCombobox" v-model="currentProfile.position" :items="positions"
                        item-value="id" item-text="name" placeholder="Должность*" outlined dense
                        :rules="reqRules"></v-combobox>
            <v-textarea placeholder="Что умеете делать?" v-model="currentProfile.skills" outlined></v-textarea>
            <h4>Одежда</h4>
            <v-row>
              <v-text-field placeholder="Ботинки" v-model="currentProfile.boots" outlined></v-text-field>
              <v-text-field placeholder="Куртка" v-model="currentProfile.jacket" outlined></v-text-field>
              <v-text-field placeholder="Штаны" v-model="currentProfile.pants" outlined></v-text-field>
              <v-text-field placeholder="Футболка" v-model="currentProfile.shirt" outlined></v-text-field>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="editProfile">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление работника
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить профиль? Отменить это действие будет невозможно</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteUser">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmArchiveDialog" max-width="500">
      <v-card>
        <v-card-title>
          Увольнение работника
        </v-card-title>
        <v-card-text>
          Вы действительно хотите уволить работника? После подтверждения профиль будет перемещен в архив
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="cancelConfirmArchiveDialog">
            Отменить
          </v-btn>
          <v-btn color="primary" text @click="editProfile">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="photoDialog" max-width="500">
      <v-card>
        <v-card-title>
          Сменить фото
        </v-card-title>
        <v-card-text>
          <v-file-input v-model="photoField" placeholder="Фото профиля" accept="image/*"
                        prepend-icon="" outlined></v-file-input>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="savePhoto">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="changeGroupForm" max-width="500">
      <v-card>
        <v-card-title>Поменять роль пользователя
        </v-card-title>
        <v-card-text>
          <v-select v-model="currentGroup.id"
                    :items="groups" item-text="name" item-value="id" outlined>
          </v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="changeGroupForm = false">Отмена</v-btn>
          <v-btn color="primary" text @click="putUserGroup">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import BackIcon from "../../components/icons/backIcon";
import $ from "jquery";
import EditIcon from "../../components/icons/editIcon";
import WasteIcon from "../../components/icons/wasteIcon";

export default {
  name: "WorkerOpen",
  components: {WasteIcon, EditIcon, BackIcon},
  props: {
    id: [String, Number],
  },
  data() {
    return {
      page: 'workers',
      currentProfile: {
        id: 0,
        lastname: "",
        name: "",
        citizenship: "",
        birthdate: "",
        social_code_own: "",
        social_code_fin: "",
        address_own: {
          index: '',
          country: '',
          city: '',
          street: '',
          house: '',
          entrance: '',
          flat: '',
        },
        address_fin: {
          index: '',
          country: '',
          city: '',
          street: '',
          house: '',
          entrance: '',
          flat: '',
        },
        phone: "",
        phone_fin: "",
        email: "",
        bank_account: "",
        tax_number: "",
        auto: false,
        tool: false,
        english: false,
        estonian: false,
        finnish: false,
        russian: false,
        other_language: "",
        position: "",
        skills: "",
        boots: null,
        jacket: null,
        pants: null,
        shirt: null,
        photo_path: null,
        auth_user_id: {
          email: "",
          is_staff: "",
          groups: {
            id: 0,
            name: ""
          }
        }
      },
      currentGroup: {
        id: 0,
        name: ""
      },
      groups: [],
      positions: [],
      full: false,
      formTitle: "Добавление работника",
      formBtnText: "Сохранить",
      addForm: false,
      confirmDeleteDialog: false,
      confirmArchiveDialog: false,
      photoField: null,
      photoDialog: false,
      changeGroupForm: false,
      menu: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      emailRules: [
        v => !!v || 'Необходимо заполнить поле',
        v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'Некорректный E-mail',
      ],
      phoneRules: [
        // v => !!v || '',
        v => /^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$/.test(v) || 'Некорректный номер телефона'
      ],
      phoneFinRules: [
        v => !!v || 'Необходимо заполнить поле',
        v => /^((([+][\s]{0,1})|([0]{2}[\s-]{0,1}))([358]{3})([\s-]{0,1})|([0]{1}))(([1-9]{1}[0-9]{0,1})([\s-]{0,1})([0-9]{2,4})([\s-]{0,1})([0-9]{2,4})([\s-]{0,1}))([0-9]{0,3}){1}$/.test(v) || 'Некорректный номер телефона'
      ],
    }
  },
  created() {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      if (this.$parent.$parent.read.indexOf('Работники') === -1)
        this.$router.push({name: "Index"})
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      this.loadPositions()
    } else {
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentProfile = response.data.data[0]
          if (this.currentProfile.address_fin == null)
            this.currentProfile.address_fin = {
              index: '',
              country: '',
              city: '',
              street: '',
              house: '',
              entrance: '',
              flat: '',
            }
          if (this.currentProfile.address_own == null)
            this.currentProfile.address_own = {
              index: '',
              country: '',
              city: '',
              street: '',
              house: '',
              entrance: '',
              flat: '',
            }
          this.loadGroups()
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
    loadPositions() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles/positions",
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
    loadGroups() {
      $.ajax({
        url: this.$hostname + "time-tracking/groups",
        type: "GET",
        success: (response) => {
          this.groups = response.data.groups
          this.groups.forEach(group => {
            if (this.currentProfile.auth_user_id.groups[0] === group.id) {
              this.currentGroup.name = group.name
              this.currentGroup.id = group.id
            }
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
    editProfile() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "PUT",
        data: this.currentProfile,
        success: () => {
          console.log("Профиль изменен")
          if (this.addForm) {
            this.editUser()
          } else {
            this.confirmArchiveDialog = false
            this.loadData()
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
    editUser() {
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "PUT",
        data: {
          id: this.currentProfile.auth_user_id.id,
          username: this.currentProfile.auth_user_id.email,
          email: this.currentProfile.auth_user_id.email,
        },
        success: () => {
          console.log("Пользователь изменен")
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
        },
      })
    },
    savePhoto() {
      const axios = require('axios')
      // чтение файла в formData
      let fd = new FormData();
      let avatar = this.photoField;
      if (avatar !== undefined) {
        fd.append('image', avatar)
      } else {
        console.log("ERROR")
        return
      }
      axios({
        method: 'put',
        url: this.$hostname + "time-tracking/profiles/" + this.currentProfile.id,
        headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
        data: fd
      })
          .then(response => {
            console.log(response.data.data)
            this.photoDialog = false
            this.photoField = null
            this.currentProfile.photo_path = response.data.data.name
            this.loadData()
          });
    },
    putUserGroup() {
      $.ajax({
        url: this.$hostname + "time-tracking/user-groups",
        type: "PUT",
        data: {
          auth_user_id: this.currentProfile.auth_user_id.id,
          group_id: this.currentGroup.id
        },
        success: (response) => {
          console.log(response.data.data)
          this.currentGroup.name = response.data.data[0]
          this.changeGroupForm = false
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
    deleteUser() {
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "DELETE",
        data: {
          email: this.currentProfile.auth_user_id.email,
        },
        success: () => {
          this.alertMsg = "Пользователь удален"
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
        },
      })
    },
    openEditForm() {
      this.formTitle = "Редактирование работника"
      this.formBtnText = "Сохранить работника"
      this.addForm = true
    },
    openConfirmArchiveDialog() {
      if (!this.currentProfile.active) {
        this.currentProfile.active = false
        this.confirmArchiveDialog = true
      } else {
        this.editProfile()
      }
    },
    cancelConfirmArchiveDialog() {
      this.currentProfile.active = true
      this.confirmArchiveDialog = false
    },
  }
}
</script>

<style scoped>

</style>