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
      <div class="news-all" v-if="all">
        <div class="news-all__grid">
          <template v-for="item in news">
            <v-card class="news-single" :key="item.id" color="primary" @click="openNew(item)">
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
          <v-list-item class="content-list__btns-add" @click="openAddForm">
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
        <div class="news-open__text" v-html="currentNew.text"></div>
        <div class="news-open__actions">
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
    <v-dialog class="news__dialog" v-model="addForm" persistent>
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeForm">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-text-field placeholder="Заголовок" v-model="newNew.title" :rules="titleRules" required
                        outlined></v-text-field>
          <v-editor v-model="newNew.text" :config="editorConfig"></v-editor>
        </v-card-text>
        <v-card-actions>
          <!--            <div class="addition-btn">-->
          <!--              <add-photo-icon/>-->
          <!--              Загрузить обложку-->
          <!--            </div>-->
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addNew">{{ formBtnText }}</v-btn>
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

export default {
  name: "News",
  components: {
    BackIcon, EditIcon, WasteIcon, /*AddPhotoIcon,*/
  },
  data() {
    return {
      page: 'news',
      all: true,
      news: '',
      newNew: {
        id: 0,
        title: '',
        text: '',
        plainText: '',
      },
      currentNew: {
        id: 0,
        title: '',
        text: ''
      },
      titleRules: [
        v => !!v || 'Необходимо ввести заголовок'
      ],
      formTitle: "Добавление новости",
      formBtnText: "Добавить новость",
      addForm: false,
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
          'img',
          'video',
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
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
    },
    addNew() {
      console.log(this.newNew.id + " " + this.newNew.title)
      console.log(this.newNew.text)
      if (this.newNew.id > 0)
        this.editNew()
      else
        $.ajax({
          url: this.$hostname + "time-tracking/news",
          type: "POST",
          data: {
            title: this.newNew.title,
            text: this.newNew.text,
          },
          success: () => {
            this.alertMsg = "Новость добавлена"
            this.loadData()
            this.addForm = false
          },
          error: (response) => {
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            console.log(response.data)
          },
        })
    },
    editNew() {
      $.ajax({
        url: this.$hostname + "time-tracking/news",
        type: "PUT",
        data: {
          id: this.newNew.id,
          title: this.newNew.title,
          text: this.newNew.text
        },
        success: () => {
          this.alertMsg = "Новость изменена"
          this.loadData()
          this.currentNew = {
            id: this.newNew.id,
            title: this.newNew.title,
            text: this.newNew.text
          }
          this.closeForm()
        },
        error: (response) => {
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
        },
      })
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
          this.alertError = true
          this.alertMsg = "Непредвиденная ошибка"
          console.log(response.data)
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
        title: "",
        text: "",
      }
    },
    openNew(item) {
      this.currentNew = item
      this.currentNew.text = this.currentNew.text.replaceAll('&lt;', '<').replaceAll('&gt;', '>')
      console.log(this.currentNew.text.replaceAll('&lt;', '<').replaceAll('&gt;', '>'))
      // this.currentNew.text = innerHtml(this.currentNew.text)
      // document.getElementById('div').innerHtml(this.currentNew.text)
      this.all = false
    }
  }
}
</script>

<style scoped>

</style>