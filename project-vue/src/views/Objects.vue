<template>
  <div class="objects flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Объекты</h3>
        <div class="addition-btn" @click="all = true" v-if="!all">
          <span>К списку объектов</span>
          <back-icon/>
        </div>
        <div class=" addition-btn content-list__filters-mobile" v-if="all"
             @click="openFilters">Фильтры
        </div>
      </div>
      <div class="objects-all all" v-if="all">
        <div class="content-list__filters">
          <v-icon color="grey lighten-1" @click="closeFilters">
            $deleteIcon
          </v-icon>
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
        <v-list three-line class="objects__list content-list">
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
                <v-icon color="grey lighten-1" @click="openConfirmDeleteDialog(object)">$deleteIcon</v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
        <v-list class="content-list__btns">
          <v-list-item v-if="!archive" class="content-list__btns-add" @click="openAddForm">
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
        </v-list>
      </div>
      <div class="objects-open" v-else>
        <div class="objects-open__info profile__info">
          <h3>Информация об объекте</h3>
          <div class="news-open__actions open__actions">
            <div class="addition-btn" @click="openEditForm(currentObject)">
              <edit-icon/>
              Редактировать объект
            </div>
            <div class="addition-btn" @click="deleteObject(currentObject.id)">
              <waste-icon/>
              Удалить объект
            </div>
          </div>
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
              <span class="profile__info-content">{{ currentObject.date_end }}</span>
            </li>
            <li>
              <span class="profile__info-title">Описание работ</span>
              <span class="profile__info-content">{{ currentObject.work_description }}</span>
            </li>
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
          <h3>Контактное лицо</h3>
          <ul>
            <li>
              <span class="profile__info-title">Фамилия</span>
              <span class="profile__info-content">{{ currentObject.contact_id.lastname }}</span>
            </li>
            <li>
              <span class="profile__info-title">Имя</span>
              <span class="profile__info-content">{{ currentObject.contact_id.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentObject.contact_id.work_phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentObject.contact_id.work_email }}</span>
            </li>
          </ul>
          <h3>Дополнительная информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Жилье</span>
              <span class="profile__info-content">{{ currentObject.habitation }}</span>
            </li>
            <li>
              <span class="profile__info-title">Страховка от несчастных случаев</span>
              <span class="profile__info-content">{{ currentObject.accident_insurance }}</span>
            </li>
            <li>
              <span class="profile__info-title">Страховка здоровья</span>
              <span class="profile__info-content">{{ currentObject.health_insurance }}</span>
            </li>
          </ul>
          <h3>Работники</h3>
          <v-list three-line class="workers__list content-list">
            <template v-for="worker in objectWorkers">
              <v-list-item :key="worker.id">
                <v-list-item-content @click="openWorker(worker)">
                  <v-list-item-title>{{ worker.user_profile_id.lastname }} {{ worker.user_profile_id.name }}
                    ({{ worker.user_profile_id.phone }})
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <span>{{ worker.start_date }} - {{ worker.end_date }}</span><br>
                    <span>{{ worker.comment }}</span>
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-icon color="grey lighten-1" @click="openEditWorkerForm(worker)">
                    $edit
                  </v-icon>
                  <v-icon color="grey lighten-1" @click="openConfirmDeleteWorkerDialog(worker)">
                    $waste
                  </v-icon>
                </v-list-item-action>
              </v-list-item>
            </template>
          </v-list>
          <v-list class="content-list__btns">
            <v-list-item class="content-list__btns-add" @click="openAddWorkerForm">
              <v-list-item-icon>
                <v-icon>mdi-plus</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Добавить работника</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <!--          <h3>Фото объекта</h3>-->
          <!--          <v-slide-group class="pa-4 objects-open__slider" v-model="photos" active-class="slide-active" show-arrows>-->
          <!--            <v-slide-item v-for="ph in photos" :key="ph.id">-->
          <!--              <v-card class="ma-4" height="250" width="300">-->
          <!--                <v-row class="fill-height" align="center" justify="center">-->
          <!--                  <v-scale-transition>-->
          <!--                    <v-img :src="require('../../../media'+ph.photo_path)"></v-img>-->
          <!--                  </v-scale-transition>-->
          <!--                </v-row>-->
          <!--              </v-card>-->
          <!--            </v-slide-item>-->
          <!--          </v-slide-group>-->
          <h3>Комментарии</h3>
          <div class="objects-open__comments">
            <div class="objects-open__comments-single" v-for="com in comments" :key="com.id">
              <h4> {{ com.user_profile_id.lastname }} {{ com.user_profile_id.name }}
                ({{ com.user_profile_id.position }})</h4>
              <div v-html="com.text"></div>
              <div class="open__actions">
                <div class="addition-btn">
                  Ответить
                </div>
                <div class="addition-btn">
                  Удалить
                </div>
              </div>
            </div>
          </div>
          <div class="objects-open__comments-add">
            <v-editor v-model="newComment.text" :config="editorConfig"></v-editor>
            <v-btn class="action-btn" color="secondary" @click="addComment">
              Добавить
            </v-btn>
          </div>
        </div>
      </div>
    </div>
    <v-dialog v-model="addForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeForm">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="form">
            <v-text-field placeholder="Индекс*" v-model="newObject.index" :rules="reqRules" required
                          outlined></v-text-field>
            <v-row>
              <v-text-field placeholder="Город*" v-model="newObject.city" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Улица*" v-model="newObject.street" :rules="reqRules" required
                            outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом*" v-model="newObject.house" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="newObject.entrance" outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="newObject.flat" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-menu ref="menu_start" v-model="datePickers.menu_start" :close-on-content-click="false"
                      :return-value.sync="newObject.date_start"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newObject.date_start" placeholder="Начало работ*" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
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
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="newObject.date_end" no-title scrollable color="primary">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="datePickers.menu_end = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu_end.save(newObject.date_end)">OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-row>
            <v-row>
              <v-select v-model="newObject.client_id" :items="clients" item-text="name" item-value="id"
                        :rules="reqRules" placeholder="Клиент*" outlined dense
                        @change="loadContacts(newObject.client_id)"></v-select>
              <v-select v-model="newObject.contact_id" :items="contacts" item-value="id" item-text="label"
                        no-data-text="Выберите клиента" placeholder="Контактное лицо*" :rules="reqRules" outlined
                        dense></v-select>
            </v-row>
            <v-text-field placeholder="Жилье" v-model="newObject.habitation" outlined></v-text-field>
            <v-row>
              <v-text-field placeholder="Страховка от несчастных случаев" v-model="newObject.accident_insurance"
                            outlined></v-text-field>
              <v-text-field placeholder="Страховка здоровья" v-model="newObject.health_insurance"
                            outlined></v-text-field>
            </v-row>
            <v-textarea placeholder="Описание работ" v-model="newObject.work_description" outlined></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addObject">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="addWorkerForm" max-width="500">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeForm">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="workerForm">
            <v-select v-model="addWorker.user_profile_id" :items="workers" item-value="id" item-text="label"
                      no-data-text="Нет свободных работников" placeholder="Выберите работника*" :rules="reqRules"
                      outlined dense></v-select>
            <v-row>
              <v-menu ref="worker_start" v-model="datePickers.worker_start" :close-on-content-click="false"
                      :return-value.sync="addWorker.start_date"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="addWorker.start_date" placeholder="Начало работ*" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="addWorker.start_date" no-title scrollable color="primary">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="datePickers.worker_start = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.worker_start.save(addWorker.start_date)">OK</v-btn>
                </v-date-picker>
              </v-menu>
              <v-menu ref="worker_end" v-model="datePickers.worker_end" :close-on-content-click="false"
                      :return-value.sync="addWorker.end_date"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="addWorker.end_date" placeholder="Окончание работ" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="addWorker.end_date" no-title scrollable color="primary">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="datePickers.worker_end = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.worker_end.save(addWorker.end_date)">OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-row>
            <v-textarea placeholder="Комментарий" v-model="addWorker.comment" outlined></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="putObjectUser">Сохранить</v-btn>
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
    <v-dialog v-model="confirmDeleteWorkerDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление работника с объекта
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить работника с объекта? Отменить это действие будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteWorkerDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteObjectUser">Подтвердить</v-btn>
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
          <v-btn color="primary" text @click="editObject">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import $ from 'jquery';
// import AddPhotoIcon from "../components/icons/addPhotoIcon";
import BackIcon from "../components/icons/backIcon";
import WasteIcon from "../components/icons/wasteIcon";
import EditIcon from "../components/icons/editIcon";

export default {
  name: "Objects",
  components: {EditIcon, WasteIcon, BackIcon, /*AddPhotoIcon*/},
  data() {
    return {
      page: 'objects',
      objects: [],
      objectWorkers: [],
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
        client_id: '',
        contact_id: '',
        work_description: null,
        habitation: null,
        accident_insurance: null,
        health_insurance: null,
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
        contact_id: {
          email: ''
        },
        work_description: null,
        habitation: null,
        accident_insurance: null,
        health_insurance: null,
      },
      addWorker: {
        id: 0,
        user_profile_id: 0,
        object_id: 0,
        start_date: null,
        end_date: null,
        comment: null,
      },
      newComment: {
        text: "",
        object_comments_id: null,
        objects_id: null
      },
      photos: "",
      comments: [],
      clients: [],
      contacts: [],
      workers: [],
      selects: ["Все", "ООО \"Праздник\"", "ООО \"Цветы\""],
      filter: {
        address: "",
        client: "Все",
        dates: []
      },
      datePickers: {
        menu_filter: false,
        menu_start: false,
        menu_end: false,
        worker_start: false,
        worker_end: false,
      },
      formTitle: "Добавление объекта",
      formBtnText: "Добавить объект",
      addForm: false,
      addWorkerForm: false,
      confirmArchiveDialog: false,
      confirmDeleteDialog: false,
      confirmDeleteWorkerDialog: false,
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
      editorConfig: {
        printLog: false,
        uploadImgUrl: 'http://localhost:8000/time-tracking/images/upload',
        menus: [
          'source',
          '|',
          'bold',
          'underline',
          'italic',
          'strikethrough',
          'eraser',
          'forecolor',
          'bgcolor',
          '|',
          'quote',
          'fontfamily',
          'fontsize',
          'head',
          'unorderlist',
          'orderlist',
          'alignleft',
          'aligncenter',
          'alignright',
          '|',
          'link',
          'unlink',
          'table',
          // 'emotion',
          '|',
          // 'img',
          // 'video',
          'insertcode',
          '|',
          'undo',
          'redo',
          'fullscreen'
        ],
        useLang: 'en',
        pasteText: true,
      },
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
  },
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
    loadContacts(client_id) {
      this.newObject.contact_id = null
      this.contacts = []
      $.ajax({
        url: this.$hostname + "time-tracking/clients-employees/" + client_id,
        type: "GET",
        success: (response) => {
          this.contacts = response.data.data
          this.contacts.forEach(contact => {
            contact.label = contact.lastname + ' ' + contact.name + ', ' + contact.position
            console.log(contact.label)
          })
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    addObject() {
      if (this.$refs.form.validate()) {
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
              client_id: this.newObject.client_id,
              contact_id: this.newObject.contact_id,
              work_description: this.newObject.work_description,
              habitation: this.newObject.habitation,
              accident_insurance: this.newObject.accident_insurance,
              health_insurance: this.newObject.health_insurance,
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
      }
    },
    editObject() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "PUT",
        data: this.currentObject,
        // data: this.newObject,
        success: () => {
          console.log("Объект изменен ")
          if (this.addForm) {
            this.loadData()
            this.closeForm()
          } else {
            this.confirmArchiveDialog = false
          }
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
      this.loadPhoto(item.id)
      this.all = false
      this.loadWorkers()
      this.loadComments()
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
    loadWorkers() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees/" + this.currentObject.id,
        type: "GET",
        success: (response) => {
          this.objectWorkers = response.data.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees",
        type: "GET",
        success: (response) => {
          this.workers = response.data.data
          this.workers.forEach(worker => {
            worker.label = worker.lastname + ' ' + worker.name + ', ' + worker.position
          })
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    loadComments() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/comments/" + this.currentObject.id,
        type: "GET",
        success: (response) => {
          this.comments = response.data.data
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    putObjectUser() {
      if (this.$refs.workerForm.validate()) {
        this.addWorker.object_id = this.currentObject.id
        $.ajax({
          url: this.$hostname + "time-tracking/objects/employees",
          type: "PUT",
          data: {
            id: this.addWorker.id,
            user_profile_id: this.addWorker.user_profile_id,
            objects_id: this.addWorker.object_id,
            start_date: this.addWorker.start_date,
            end_date: this.addWorker.end_date,
            comment: this.addWorker.comment,
          },
          success: (response) => {
            console.log(response)
            this.loadWorkers()
            this.addWorkerForm = false
          },
          error: (response) => {
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            console.log(response.data)
          },
        })
      }
    },
    deleteObjectUser() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees",
        type: "DELETE",
        data: {
          id: this.addWorker.id,
        },
        success: (response) => {
          console.log(response)
          this.loadWorkers()
          this.confirmDeleteWorkerDialog = false
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    openWorker(worker) {
      console.log(worker)
    },
    addComment() {
      this.newComment.objects_id = this.currentObject.id
      $.ajax({
        url: this.$hostname + "time-tracking/objects/comments",
        type: "POST",
        data: this.newComment,
        success: (response) => {
          console.log(response)
          this.loadComments()
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
    openAddWorkerForm() {
      this.formTitle = "Добавление работника на объект"
      this.addWorkerForm = true
    },
    openEditWorkerForm(worker) {
      this.addWorker = worker
      this.formTitle = "Редактирование работника на объекте"
      this.addWorkerForm = true
    },
    openConfirmArchiveDialog() {
      if ((this.currentObject.active && !this.all) || (!this.currentObject.active && this.all)) {
        this.currentObject.active = true
        this.confirmArchiveDialog = true
      } else {
        this.editObject()
      }
    },
    cancelConfirmArchiveDialog() {
      this.currentObject.active = false
      this.confirmArchiveDialog = false
    },
    openConfirmDeleteDialog(item) {
      this.currentObject = item
      if (this.archive || !this.all) {
        this.confirmDeleteDialog = true
      } else
        this.openConfirmArchiveDialog()
    },
    openConfirmDeleteWorkerDialog(item) {
      this.addWorker = item
      this.confirmDeleteWorkerDialog = true
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
        client_id: '',
        contact_id: '',
        work_description: null,
        habitation: null,
        accident_insurance: null,
        health_insurance: null,
      }
      this.addWorker = {
        id: 0,
        user_profile_id: 0,
        object_id: 0,
        start_date: null,
        end_date: null,
        comment: null,
      }
      this.addWorkerForm = false
    },
    openFilters() {
      console.log("open filters")
      $('.content-list__filters').addClass('open')
      $('.content-list__btns').addClass('hidden')
    },
    closeFilters() {
      console.log("open filters")
      $('.content-list__filters').removeClass('open')
      $('.content-list__btns').removeClass('hidden')
    },
  }
}
</script>

<style scoped>

</style>