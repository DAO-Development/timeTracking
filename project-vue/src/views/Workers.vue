<template>
  <div class="workers flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Работники</h3>
        <div class="addition-btn" @click="all = true" v-if="!all">
          <span>К списку работников</span>
          <back-icon/>
        </div>
        <div class=" addition-btn content-list__filters-mobile" v-if="all"
             @click="openFilters">Фильтры
        </div>
      </div>
      <div class="workers-all" v-if="all">
        <div class="content-list__filters">
          <v-icon color="grey lighten-1" @click="closeFilters">
            $deleteIcon
          </v-icon>
          <v-text-field placeholder="Фамилия Имя" v-model="filter.name" outlined></v-text-field>
          <v-select v-model="filter.position" :items="selects" placeholder="Должность" outlined></v-select>
          <v-text-field placeholder="Почта" v-model="filter.email" outlined></v-text-field>
        </div>
        <v-list three-line class="workers__list content-list">
          <template v-for="profile in profiles">
            <v-list-item :key="profile.id"
                         v-if="profile.active !== archive && profile.auth_user_id.email.includes(filter.email) && (profile.name + ' ' + profile.lastname).includes(filter.name)  && (profile.position===filter.position || filter.position === 'Все')">
              <v-list-item-avatar class="content-list__image">
                <v-img v-if="profile.photo_path != null" :src="require('../../../media'+profile.photo_path)"></v-img>
              </v-list-item-avatar>
              <v-list-item-content @click="openProfile(profile)">
                <v-list-item-title>{{ profile.name }} {{ profile.lastname }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span>{{ profile.position }}</span><br>
                  <span>{{ profile.auth_user_id.email }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon color="grey lighten-1" @click="openConfirmDeleteDialog(profile)">
                  $deleteIcon
                </v-icon>
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
              <v-list-item-title>Добавить работника</v-list-item-title>
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
      <div class="workers-open" v-if="!all">
        <div class="profile__image">
          <v-img v-if="currentProfile.photo_path != null"
                 :lazy-src="require('../../../media'+currentProfile.photo_path)"
                 :src="require('../../../media'+currentProfile.photo_path)"></v-img>
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
              <span class="profile__info-title">Должность</span>
              <span class="profile__info-content">{{ currentProfile.position }}</span></li>
          </ul>
          <h3>Контакты</h3>
          <ul>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentProfile.phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentProfile.auth_user_id.email }}</span>
            </li>
          </ul>
          <ul>
            <li>
              <span class="profile__info-title">Работает</span>
              <v-checkbox v-model="currentProfile.active" @change="openConfirmArchiveDialog"></v-checkbox>
            </li>
          </ul>
          <div class="news-open__actions open__actions">
            <div class="addition-btn" @click="openEditForm(currentProfile)">
              <edit-icon/>
              Редактировать объект
            </div>
            <div class="addition-btn" @click="openConfirmDeleteDialog(currentProfile)">
              <waste-icon/>
              Удалить объект
            </div>
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
          <v-text-field placeholder="Фамилия*" v-model="newProfile.lastname" :rules="reqRules" required
                        outlined></v-text-field>
          <v-text-field placeholder="Имя*" v-model="newProfile.name" :rules="reqRules"
                        required outlined></v-text-field>
          <v-combobox ref="positionCombobox" v-model="newProfile.position" :items="positions" placeholder="Должность*"
                      outlined dense></v-combobox>
          <v-text-field placeholder="Почта*" v-model="newProfile.email" :rules="emailRules" required
                        outlined></v-text-field>
          <v-text-field placeholder="Телефон*" v-model="newProfile.phone" :rules="phoneRules"
                        required outlined></v-text-field>
        </v-card-text>
        <v-card-actions>
          <div class="addition-btn">
            <pdf-icon/>
            Конвертировать в .pdf
          </div>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addUser">{{ formBtnText }}</v-btn>
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
          <v-btn color="primary" text @click="deleteUser(null)">Подтвердить</v-btn>
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
  </div>
</template>

<script>
import $ from "jquery";
import PdfIcon from "../components/icons/pdfIcon";
import BackIcon from "../components/icons/backIcon";
import EditIcon from "../components/icons/editIcon";
import WasteIcon from "../components/icons/wasteIcon";

export default {
  name: "Workers",
  components: {WasteIcon, EditIcon, BackIcon, PdfIcon},
  data() {
    return {
      page: 'home',
      all: true,
      archive: false,
      profiles: {},
      positions: ["Администратор", "Маляр", "Строитель"],
      selects: ["Все", "Администратор", "Маляр", "Строитель"],
      newProfile: {
        id: 0,
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
      },
      currentProfile: {
        id: 0,
        auth_user_id: "",
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
        active: true,
        photo_path: null,
      },
      filter: {
        name: "",
        position: "Все",
        email: ""
      },
      formTitle: "Добавление работника",
      formBtnText: "Добавить работника",
      addForm: false,
      confirmArchiveDialog: false,
      confirmDeleteDialog: false,
      photoField: null,
      photoDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      emailRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      phoneRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
    }
  },
  created() {
    if (localStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + localStorage.getItem("auth_token")}
      })
      this.loadData()
    } else if (sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + sessionStorage.getItem("auth_token")}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "GET",
        success: (response) => {
          this.profiles = response.data.data
        },
        error: (response) => {
          console.log(response)
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером"
          } else {
            this.alertMsg = "Непредвиденная ошибка"
          }
          this.alertError = true
        }
      })
    },
    addUser() {
      if (this.newProfile.id !== 0) {
        this.editProfile()
      } else {
        if (this.newProfile.position === "Администратор") {
          this.newProfile.is_staff = true
        }
        $.ajax({
          url: this.$hostname + "time-tracking/user",
          type: "POST",
          data: {
            username: this.newProfile.email,
            email: this.newProfile.email,
            is_staff: this.newProfile.is_staff,
            password: "12345678"
          },
          success: (response) => {
            this.addProfile(response.data.data.id)
          },
          error: (response) => {
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            console.log(response.data)
          },
        })
      }
    },
    addProfile(id) {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "POST",
        data: {
          auth_user_id: id,
          name: this.newProfile.name,
          lastname: this.newProfile.lastname,
          position: this.newProfile.position,
          phone: this.newProfile.phone,
          active: true
        },
        success: () => {
          this.alertMsg = "Пользователь добавлен"
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
    editProfile() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "PUT",
        data: {
          id: this.currentProfile.id,
          auth_user_id: this.currentProfile.auth_user_id,
          name: this.currentProfile.name,
          lastname: this.currentProfile.lastname,
          position: this.currentProfile.position,
          phone: this.currentProfile.phone,
          active: this.currentProfile.active,
          // photo_path: this.currentProfile.photo_path
        },
        success: () => {
          console.log("Профиль изменен")
          this.confirmArchiveDialog = false
          if (this.addForm) {
            this.editUser()
          } else {
            this.loadData()
          }
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    editUser() {
      this.currentProfile.auth_user_id.email = this.newProfile.email
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "PUT",
        data: {
          id: this.newProfile.auth_user_id.id,
          username: this.newProfile.email,
          email: this.newProfile.email,
        },
        success: () => {
          console.log("Пользователь изменен")
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
    makeblob(dataURL) {
      var BASE64_MARKER = ';base64,';
      // var parts, contentType, raw, rawLength
      if (dataURL.indexOf(BASE64_MARKER) === -1) {
        let parts = dataURL.split(',');
        let contentType = parts[0].split(':')[1];
        let raw = decodeURIComponent(parts[1]);
        return new Blob([raw], {type: contentType});
      }
      let parts = dataURL.split(BASE64_MARKER);
      let contentType = parts[0].split(':')[1];
      let raw = window.atob(parts[1]);
      let rawLength = raw.length;

      var uInt8Array = new Uint8Array(rawLength);

      for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
      }

      return new Blob([uInt8Array], {type: contentType});
    },
    savePhoto() {
      const file = document.querySelector('input[type=file]').files[0]
      console.log(this.photoField.name)
      this.currentProfile.photo_path = "/users/" + this.photoField.name

      const reader = new FileReader()

      reader.onload = readerOnLoad;

      let rawImg;

      function readerOnLoad(e) {
        rawImg = btoa(e.target.result)
        console.log(rawImg);
      }

      reader.readAsBinaryString(file);
      console.log(file)


      $.ajax({
        url: this.$hostname + "time-tracking/profiles/" + this.currentProfile.id,
        type: "PUT",
        // contentType: "multipart/form-data; boundary=------WebKitFormBoundary",
        // contentType: "image/png",
        // contentType: 'application/octet-stream',
        processData: false,
        // data: fd,
        data: {
          photo: rawImg
        },
        // data: {
        //   photo: this.photoField,
        //   photo_path: this.currentProfile.photo_path
        // },
        success: () => {
          console.log("Профиль изменен")
          this.loadData()
          this.photoDialog = false
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
      console.log("done ajax")
      // чтение файла как base64
      // let reader = new FileReader();
      // // let str;
      // reader.readAsDataURL(this.photoField)
      // reader.onload = function () {
      //   console.log(reader.result);
      // };
      // reader.onerror = function (error) {
      //   console.log('Error: ', error);
      // };
      // console.log(reader.result)
      // console.log(this.reader.toString())
      //
      // var base64ImageContent = reader.toString().replace(/^data:image\/(png|jpg);base64,/, "");
      // var blob = base64ToBlob(base64ImageContent, 'image/png');
      // var formData = new FormData();
      // formData.append('picture', blob);

      // чтение файла в formData
      // let fd = new FormData();
      // let avatar = this.photoField;
      // if (avatar !== undefined) {
      //   fd.append('image', avatar)
      // } else {
      //   console.log("ERROR")
      //   return
      // }


      // $.ajax({
      //   url: this.$hostname + "time-tracking/profiles/" + this.currentProfile.id,
      //   type: "PUT",
      //   // contentType: "multipart/form-data; boundary=------WebKitFormBoundary",
      //   // contentType: "image/png",
      //   // contentType: 'application/octet-stream',
      //   processData: false,
      //   // data: fd,
      //   data: {
      //     photo: rawImg
      //   },
      //   // data: {
      //   //   photo: this.photoField,
      //   //   photo_path: this.currentProfile.photo_path
      //   // },
      //   success: () => {
      //     console.log("Профиль изменен")
      //     this.loadData()
      //     this.photoDialog = false
      //   },
      //   error: (response) => {
      //     this.alertError = true
      //     this.alertMsg = "Непредвиденная ошибка"
      //     console.log(response.data)
      //   },
      // })
    },
    deleteUser(email) {
      if (email == null) {
        email = this.currentProfile.email
      }
      console.log(email)
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "DELETE",
        data: {
          email: email,
        },
        success: () => {
          this.alertMsg = "Пользователь удален"
          this.loadData()
          this.confirmDeleteDialog = false
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    openProfile(profile) {
      this.currentProfile = profile
      this.all = false
    },
    closeForm() {
      this.addForm = false
      this.newProfile = {
        lastname: "",
        name: "",
        position: "",
        email: "",
        phone: "",
        is_staff: false,
      }
    },
    openAddForm() {
      this.formTitle = "Добавление работника"
      this.formBtnText = "Добавить работника"
      this.addForm = true
    },
    openEditForm(item) {
      this.formTitle = "Редактирование работника"
      this.formBtnText = "Сохранить работника"
      this.newProfile = item
      this.newProfile.email = item.auth_user_id.email
      this.addForm = true
    },
    openConfirmArchiveDialog() {
      console.log(this.currentProfile.id)
      if ((!this.currentProfile.active && !this.all) || (this.currentProfile.active && this.all)) {
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
    openConfirmDeleteDialog(item) {
      this.currentProfile = item
      this.currentProfile.email = item.auth_user_id.email
      if (this.archive || !this.all) {
        this.confirmDeleteDialog = true
      } else {
        this.openConfirmArchiveDialog()
      }
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