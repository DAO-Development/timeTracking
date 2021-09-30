<template>
  <div class="flex-main">
    <Menu class="flex-sidebar"/>
    <div class="objects flex-content">
      <div class="summary-box">
        <div class="summary-box__title">
          <h3>Объекты</h3>
          <div class="addition-btn" @click="all = true" v-if="!all">
            К списку объектов
            <back-icon/>
          </div>
        </div>
        <div class="objects-all" v-if="all">
          <div class="content-list__filters">
            <v-text-field placeholder="Адрес" v-model="filter.address" outlined></v-text-field>
            <v-select v-model="filter.client" :items="selects" outlined></v-select>
            <v-menu ref="menu_filter" v-model="datePickers.menu_filter" :close-on-content-click="false"
                    :return-value.sync="filter.dates"
                    transition="scale-transition" offset-y min-width="auto">
              <template v-slot:activator="{ on, attrs }">
                <v-text-field v-model="filter.dates" placeholder="Начало работ" readonly v-bind="attrs"
                              v-on="on" outlined></v-text-field>
              </template>
              <v-date-picker v-model="filter.dates" no-title scrollable range color="primary">
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="datePickers.menu_filter = false"> Cancel</v-btn>
                <v-btn text color="primary" @click="$refs.menu_filter.save(filter.dates)">OK</v-btn>
              </v-date-picker>
            </v-menu>
          </div>
          <v-list three-line class="objects__list content-list" v-if="all">
            <template v-for="object in objects">
              <v-list-item :key="object.id"
                           v-if="object.active === archive && (object.city + ' ' + object.street + ' ' + object.house).includes(filter.address) && (filter.client==='Все' || object.client_id.name===filter.client) && ((typeof(filter.dates[0]) === 'undefined' || object.date_start >= filter.dates[0]) && (object.date_start <= filter.dates[1] || typeof(filter.dates[1]) === 'undefined'))">
                <v-list-item-content @click="openObject(object)">
                  <v-list-item-title>{{ object.city }} {{ object.street }} {{ object.house }}</v-list-item-title>
                  <v-list-item-subtitle>
                    <span>{{ object.date_start }} - {{ object.date_end }}</span><br>
                    <span>{{ object.client_id.name }}</span>
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-icon color="grey lighten-1" @click="openConfirmDeleteDialog(object.id)">$deleteIcon</v-icon>
                </v-list-item-action>
              </v-list-item>
            </template>
            <div class="content-list__btns">
              <v-list-item v-if="!archive" class="content-list__btns-add" @click="addForm=true">
                <v-list-item-icon>
                  <v-icon>mdi-plus</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Добавить объект</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-if="!archive" class="content-list__btns-add" @click="archive=!archive">
                <v-list-item-icon>
                  <v-icon>$archive</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Архив</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-else class="content-list__btns-add" @click="archive=!archive">
                <v-list-item-icon>
                  <v-icon>$archive</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Выйти из архива</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </div>
          </v-list>
        </div>
        <div class="objects-open" v-else>
          <!--          <div class="objects-open__image profile__image">-->
          <!--            <v-img v-if="photo != null" :lazy-src="require('../../../media'+photo)"-->
          <!--                   :src="require('../../../media'+photo)"></v-img>-->
          <!--            <div class="profile__change-photo">Добавить фото</div>-->
          <!--          </div>-->
          <div class="objects-open__info profile__info">
            <h3>Информация об объекте</h3>
            <ul>
              <li>
                <span class="profile__info-title">Объект сдан</span>
                <v-checkbox v-model="currentObject.active" @change="openConfirmArchiveDialog"></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Клиент</span>
                <span class="profile__info-content">{{ currentObject.client_id.name }}</span>
              </li>
              <li>
                <span class="profile__info-title">Начало работ</span>
                <span class="profile__info-content">{{ currentObject.date_start }}</span>
              </li>
              <li>
                <span class="profile__info-title">Окончание работ</span>
                <span class="profile__info-content">{{ currentObject.date_end }}</span></li>
            </ul>
            <h3>Адрес</h3>
            <ul>
              <li>
                <span class="profile__info-title">Улица</span>
                <span class="profile__info-content">{{ currentObject.street }}</span>
              </li>
              <li>
                <span class="profile__info-title">Дом</span>
                <span class="profile__info-content">{{ currentObject.house }}</span>
              </li>
              <li>
                <span class="profile__info-title">Подъезд</span>
                <span class="profile__info-content">{{ currentObject.entrance }}</span>
              </li>
              <li>
                <span class="profile__info-title">Квартира</span>
                <span class="profile__info-content">{{ currentObject.flat }}</span>
              </li>
              <li>
                <span class="profile__info-title">Город</span>
                <span class="profile__info-content">{{ currentObject.city }}</span>
              </li>
              <li>
                <span class="profile__info-title">Индекс</span>
                <span class="profile__info-content">{{ currentObject.index }}</span>
              </li>
            </ul>
            <h3>Работники</h3>
            <ul>

            </ul>
            <h3>Фото объекта</h3>
            <v-slide-group class="pa-4 objects-open__slider" v-model="photos" active-class="slide-active" show-arrows>
              <v-slide-item v-for="ph in photos" :key="ph.id">
                <v-card class="ma-4" height="250" width="300">
                  <v-row class="fill-height" align="center" justify="center">
                    <v-scale-transition>
                      <v-img :src="require('../../../media'+ph.photo_path)"></v-img>
                    </v-scale-transition>
                  </v-row>
                </v-card>
              </v-slide-item>
            </v-slide-group>
          </div>
        </div>
      </div>
      <v-dialog v-model="addForm" persistent>
        <v-card>
          <v-toolbar flat>
            <v-spacer></v-spacer>
            <v-btn icon @click="closeForm">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-toolbar>
          <h3>Добавление объекта</h3>
          <v-card-text>
            <v-text-field placeholder="Индекс*" v-model="newObject.index" :rules="reqRules" required
                          outlined></v-text-field>
            <v-text-field placeholder="Город*" v-model="newObject.city" :rules="reqRules"
                          required outlined></v-text-field>
            <v-text-field placeholder="Улица*" v-model="newObject.street" :rules="reqRules" required
                          outlined></v-text-field>
            <v-text-field placeholder="Дом*" v-model="newObject.house" :rules="reqRules"
                          required outlined></v-text-field>
            <v-text-field placeholder="Подъезд" v-model="newObject.entrance" outlined></v-text-field>
            <v-text-field placeholder="Квартира" v-model="newObject.flat" outlined></v-text-field>
            <v-menu ref="menu_start" v-model="datePickers.menu_start" :close-on-content-click="false"
                    :return-value.sync="newObject.date_start"
                    transition="scale-transition" offset-y min-width="auto">
              <template v-slot:activator="{ on, attrs }">
                <v-text-field v-model="newObject.date_start" placeholder="Начало работ*" readonly v-bind="attrs"
                              v-on="on" outlined></v-text-field>
              </template>
              <v-date-picker v-model="newObject.date_start" no-title scrollable color="primary">
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="datePickers.menu_start = false"> Cancel</v-btn>
                <v-btn text color="primary" @click="$refs.menu_start.save(newObject.date_start)">OK</v-btn>
              </v-date-picker>
            </v-menu>
            <v-menu ref="menu_end" v-model="datePickers.menu_end" :close-on-content-click="false"
                    :return-value.sync="newObject.date_end"
                    transition="scale-transition" offset-y min-width="auto">
              <template v-slot:activator="{ on, attrs }">
                <v-text-field v-model="newObject.date_end" placeholder="Окончание работ" readonly v-bind="attrs"
                              v-on="on" outlined></v-text-field>
              </template>
              <v-date-picker v-model="newObject.date_end" no-title scrollable color="primary">
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="datePickers.menu_end = false"> Cancel</v-btn>
                <v-btn text color="primary" @click="$refs.menu_end.save(newObject.date_end)">OK</v-btn>
              </v-date-picker>
            </v-menu>
            <v-select ref="positionCombobox" v-model="newObject.client_id" :items="clients" item-text="name"
                      item-value="id" placeholder="Клиент*" outlined dense></v-select>
          </v-card-text>
          <v-card-actions>
            <div class="addition-btn">
              <add-photo-icon/>
              Загрузить изображение
            </div>
            <v-spacer></v-spacer>
            <v-btn class="action-btn" color="primary" @click="addObject">Добавить объект</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="confirmDeleteDialog" max-width="500">
        <v-card>
          <v-card-title>
            Удаление объекта
          </v-card-title>
          <v-card-text>Вы действительно хотите удалить объект? Отменить это действие будет невозможно</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
            <v-btn color="primary" text @click="deleteObject">Подтвердить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="confirmArchiveDialog" max-width="500">
        <v-card>
          <v-card-title>
            Сдача объекта
          </v-card-title>
          <v-card-text>
            Вы действительно хотите сдать объект? После подтверждения объект будет перемещен в архив
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="cancelConfirmArchiveDialog">
              Отменить
            </v-btn>
            <v-btn color="primary" text @click="editObjectArchive">Подтвердить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
import Menu from "../components/Menu";
import AddPhotoIcon from "../components/icons/addPhotoIcon";
import BackIcon from "../components/icons/backIcon";

export default {
  name: "Objects",
  components: {BackIcon, AddPhotoIcon, Menu},
  data() {
    return {
      page: 'objects',
      objects: '',
      all: true,
      archive: false,
      newObject: {
        id: 0,
        index: '',
        city: '',
        street: '',
        house: '',
        entrance: '',
        flat: '',
        date_start: '',
        date_end: '',
        active: false,
        client_id: ''
      },
      currentObject: {
        id: 0,
        index: '',
        city: '',
        street: '',
        house: '',
        entrance: '',
        flat: '',
        date_start: '',
        date_end: '',
        active: false,
        client_id: '',
      },
      photo: "/objects/A3DPhhAL6Zg.png",
      photos: "",
      clients: ["ООО \"Праздник\""],
      selects: ["Все", "ООО \"Праздник\"", "ООО \"Цветы\""],
      filter: {
        address: "",
        client: "Все",
        dates: []
      },
      datePickers: {
        menu_filter: false,
        menu_start: false,
        menu_end: false
      },
      formTitle: "Добавление объекта",
      formBtnText: "Добавить объект",
      addForm: false,
      confirmArchiveDialog: false,
      confirmDeleteDialog: false,
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
    }
  },
  created() {
    if (localStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + localStorage.getItem("auth_token")}
      })
      this.loadData()
      this.loadClients()
    } else if (sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + sessionStorage.getItem("auth_token")}
      })
      this.loadData()
      this.loadClients()
    } else {
      this.$router.push({name: "Login"})
    }
  }
  ,
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "GET",
        success: (response) => {
          this.objects = response.data.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    loadClients() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "GET",
        success: (response) => {
          this.clients = response.data.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    addObject() {
      if (this.newObject.id === 0)
        $.ajax({
          url: this.$hostname + "time-tracking/objects",
          type: "POST",
          data: {
            index: this.newObject.index,
            city: this.newObject.city,
            street: this.newObject.street,
            house: this.newObject.house,
            entrance: this.newObject.entrance,
            flat: this.newObject.flat,
            date_start: this.newObject.date_start,
            date_end: this.newObject.date_end,
            active: this.newObject.active,
            client_id: this.newObject.client_id
          },
          success: () => {
            console.log("Объект добавлен ")
            this.loadData()
            this.closeForm()
          },
          error: (response) => {
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            console.log(response.data)
          },
        })
      else
        this.editObject()
    },
    editObject() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "PUT",
        data: this.newObject,
        //     {
        //   index: this.newObject.index,
        //   city: this.newObject.city,
        //   street: this.newObject.street,
        //   house: this.newObject.house,
        //   entrance: this.newObject.entrance,
        //   flat: this.newObject.flat,
        //   date_start: this.newObject.date_start,
        //   date_end: this.newObject.date_end,
        //   active: this.newObject.active,
        //   client_id: this.newObject.client_id
        // },
        success: () => {
          console.log("Объект изменен ")
          this.loadData()
          this.closeForm()
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    editObjectArchive() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "PUT",
        data: this.currentObject,
        success: () => {
          console.log("Объект перемещен в архив")
          this.loadData()
          this.confirmArchiveDialog = false
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    deleteObject() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "DELETE",
        data: {
          id: this.currentObject.id
        },
        success: () => {
          console.log("Объект удален")
          this.loadData()
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    openObject(item) {
      this.currentObject = item
      this.photo = this.loadPhoto(item.id)
      this.all = false
    },
    loadPhoto(id) {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/photos/" + id,
        type: "GET",
        success: (response) => {
          this.photos = response.data.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    openAddForm() {
      this.formTitle = "Добавление объекта"
      this.formBtnText = "Добавить объект"
      this.addForm = true
    },
    openEditForm(item) {
      this.formTitle = "Редактирование объекта"
      this.formBtnText = "Сохранить объект"
      this.newObject = item
      this.addForm = true
    },
    openConfirmArchiveDialog() {
      if (this.currentObject.active) {
        this.confirmArchiveDialog = true
      } else {
        this.editObjectArchive()
      }
    },
    cancelConfirmArchiveDialog() {
      this.currentObject.active = false
      this.confirmArchiveDialog = false
    },
    openConfirmDeleteDialog(id) {
      this.currentObject.id = id
      this.confirmDeleteDialog = true
    },
    closeForm() {
      this.addForm = false
      this.newObject = {
        id: 0,
        index: '',
        city: '',
        street: '',
        house: '',
        entrance: '',
        flat: '',
        date_start: '',
        date_end: '',
        active: false,
        client_id: ''
      }
    },
  }
}
</script>

<style scoped>

</style>