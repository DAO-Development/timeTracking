<template>
  <div class="news flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Новости</h3>
        <div class="addition-btn" @click="all = true" v-if="!all">
          <span>К списку новостей</span>
          <back-icon/>
        </div>
      </div>
      <div class="news-all all" v-if="all">
        <div class="news-all__grid">
          <template v-for="item in news">
            <v-card class="news-single" :key="item.id" color="primary" @click="openNew(item)" v-if="item.photo_path"
                    v-bind:style="{'background-image': 'url('+$hostname+'media'+item.photo_path+ ')', 'background-size': 'cover', 'background-position': 'center'}">
              <div class="news-single__actions">
                <v-icon @click="deleteNew(item.id)">$waste</v-icon>
                <v-icon @click="openEditForm(item.id, item.title, item.text)">$edit</v-icon>
              </div>
              <div class="news-single__title">{{ item.title }}</div>
              <div class="news-single__text" v-html="item.text"></div>
            </v-card>
            <v-card class="news-single" :key="item.id" color="primary" @click="openNew(item)" v-else>
              <div class="news-single__actions">
                <v-icon @click="deleteNew(item.id)">$waste</v-icon>
                <v-icon @click="openEditForm(item.id, item.title, item.text)">$edit</v-icon>
              </div>
              <div class="news-single__title">{{ item.title }}</div>
              <div class="news-single__text" v-html="item.text"></div>
            </v-card>
          </template>
        </div>
        <v-list>
          <v-list-item class="content-list__btns-add" @click="openAddForm" v-if="$parent.$parent.admin">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить новость</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
      <div class="news-open" v-else>
        <h4>{{ currentNew.title }}</h4>
        <div class="news-open__image">
          <v-img v-if="currentNew.photo_path" :src="$hostname+'media'+currentNew.photo_path"></v-img>
        </div>
        <div class="news-open__text" v-html="currentNew.text"></div>
        <div class="news-open__actions open__actions" v-if="$parent.$parent.admin">
          <div class="addition-btn" @click="openEditForm(currentNew.id, currentNew.title, currentNew.text)">
            <edit-icon/>
            Редактировать новость
          </div>
          <div class="addition-btn" @click="deleteNew(currentNew.id)">
            <waste-icon/>
            Удалить новость
          </div>
        </div>
      </div>
    </div>
    <v-dialog class="news__dialog" v-model="addForm">
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
            <v-text-field placeholder="Заголовок" v-model="newNew.title" :rules="titleRules" required
                          outlined></v-text-field>
            <v-editor v-model="newNew.text" :config="editorConfig"></v-editor>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <div class="addition-btn" @click="photoDialog=true">
            <add-photo-icon/>
            <span v-if="photoField == null">Загрузить обложку</span>
            <span v-if="photoField != null">Сменить обложку</span>
          </div>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addNew">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="photoDialog" max-width="500">
      <v-card>
        <v-card-title>
          Сменить фото
        </v-card-title>
        <v-card-text>
          <v-file-input v-model="photoField" placeholder="Обложка новости" accept="image/*"
                        prepend-icon="" outlined></v-file-input>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closePhotoForm">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import $ from "jquery";
import WasteIcon from "../components/icons/wasteIcon";
import EditIcon from "../components/icons/editIcon";
import BackIcon from "../components/icons/backIcon";
import AddPhotoIcon from "../components/icons/addPhotoIcon"

//todo добавить loader на процессы добавления и редактирования (картинка тормозит)

export default {
  name: "News",
  components: {BackIcon, EditIcon, WasteIcon, AddPhotoIcon},
  data() {
    return {
      page: 'news',
      all: true,
      news: '',
      newNew: {
        id: 0,
        title: '',
        text: '',
        photo_path: null,
      },
      photoField: null,
      currentNew: {
        id: 0,
        title: '',
        text: '',
        photo_path: null
      },
      titleRules: [
        v => !!v || 'Необходимо ввести заголовок'
      ],
      formTitle: "Добавление новости",
      formBtnText: "Добавить новость",
      addForm: false,
      photoDialog: false,
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
      options: {},
      editorConfig: {
        printLog: false,
        uploadImgUrl: 'http://localhost:2233/api/upload',
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
      disableEditor: {
        printLog: false,
        disable: true
      }
    }
  },
  created() {
    console.log("init News")
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
  methods: {
    onChange() {
      console.log(this.newNew.text.text())
    },
    uploadCallback(url) {
      console.log("uploaded url", url)
    },
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/news",
        type: "GET",
        success: (response) => {
          this.news = response.data.data
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
    addNew() {
      if (this.$refs.form.validate()) {
        if (this.newNew.id > 0)
          this.editNew()
        else {
          const axios = require('axios')
          // чтение файла в formData
          let fd = new FormData();
          let photo = this.photoField;
          if (this.photoField !== undefined) {
            fd.append('image', photo)
          }
          fd.append('title', this.newNew.title)
          fd.append('text', this.newNew.text)
          axios({
            method: 'post',
            url: this.$hostname + "time-tracking/news",
            headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
            data: fd
          })
              .then(response => {
                console.log(response.data.data)
                this.photoDialog = false
                this.closeForm()
                this.loadData()
              });
        }
      } else {
        this.alertError = true
        this.alertMsg = "Заполните обязательные поля"
      }
    },
    editNew() {
      const axios = require('axios')
      // чтение файла в formData
      let fd = new FormData();
      let photo = this.photoField;
      console.log(this.currentNew.photo_path)
      if (this.photoField !== null) {
        fd.append('image', photo)
      }
      fd.append('title', this.newNew.title)
      fd.append('text', this.newNew.text)
      fd.append('id', this.newNew.id)
      axios({
        method: 'put',
        url: this.$hostname + "time-tracking/news",
        headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
        data: fd
      })
          .then(response => {
            console.log(response.data.data)
            this.photoDialog = false
            this.closeForm()
            this.loadData()
            if (this.photoField !== null) {
              this.currentNew.photo_path = "/news/" + this.photoField.name
              this.photoField = null
            }
          });
    },
    deleteNew(id) {
      $.ajax({
        url: this.$hostname + "time-tracking/news",
        type: "DELETE",
        data: {
          id: id,
        },
        success: () => {
          this.alertMsg = "Новость удалена"
          this.loadData()
          this.all = true
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
    openAddForm() {
      this.formTitle = "Добавление новости"
      this.formBtnText = "Добавить новость"
      this.addForm = true
    },
    openEditForm(id, title, text) {
      this.formTitle = "Редактирование новости"
      this.formBtnText = "Сохранить новость"
      this.newNew = {
        id: id,
        title: title,
        text: text
      }
      this.addForm = true
    },
    closeForm() {
      this.addForm = false
      this.newNew = {
        id: 0,
        title: "",
        text: "",
        photo: null
      }
    },
    closePhotoForm() {
      // if (this.newNew.photo_path !== null)
      //   this.currentNew.photo_path = '/news/' + this.newNew.photo_path.name
      this.photoDialog = false
    },
    openNew(item) {
      this.currentNew = item
      // this.currentNew.text = this.currentNew.text.replaceAll('&lt;', '<').replaceAll('&gt;', '>')
      this.all = false
    }
  }
}
</script>

<style scoped>

</style>