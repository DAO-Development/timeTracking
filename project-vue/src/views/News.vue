<template>
  <div class="flex-main">
    <Menu class="flex-sidebar"/>
    <div class="news flex-content">
      <div class="summary-box">
        <h3>Новости</h3>
        <div class="news-all" v-if="all">
          <template v-for="item in news">
            <v-card class="news-single" :key="item.id" color="primary" @click="openNew(item)">
              <div class="news-single__actions">
                <v-icon @click="deleteNew(item.id)">$waste</v-icon>
                <v-icon @click="openEditForm(item.id, item.title, item.text)">$edit</v-icon>
              </div>
              <div class="news-single__title">{{ item.title }}</div>
              <div class="news-single__text">{{ item.text }}</div>
            </v-card>
          </template>
          <v-card class="news-single news-single-add" @click="openAddForm">
            <add-new-icon/>
            <div class="news-single-add__text">Добавить новость</div>
          </v-card>
        </div>
        <div class="news-open" v-else>
          <h4>{{ currentNew.title }}</h4>
          <div class="news-open__text">{{ currentNew.text }}</div>
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
            <v-textarea class="news__dialog--text" placeholder="Текст новости" v-model="newNew.text"
                        outlined></v-textarea>
          </v-card-text>
          <v-card-actions>
            <div class="addition-btn">
              <add-photo-icon/>
              Загрузить обложку
            </div>
            <v-spacer></v-spacer>
            <v-btn class="action-btn" color="primary" @click="addNew">Добавить новость</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
import Menu from "../components/Menu";
import AddPhotoIcon from "../components/icons/addPhotoIcon";
import AddNewIcon from "../components/icons/addNewIcon";
import WasteIcon from "../components/icons/wasteIcon";
import EditIcon from "../components/icons/editIcon";

export default {
  name: "News",
  components: {EditIcon, WasteIcon, AddNewIcon, AddPhotoIcon, Menu},
  data() {
    return {
      page: 'news',
      all: true,
      news: '',
      newNew: {
        id: 0,
        title: '',
        text: ''
      },
      currentNew: {},
      titleRules: [
        v => !!v || 'Необходимо ввести заголовок'
      ],
      formTitle: "Добавление новости",
      addForm: false,
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
    } else if (sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + sessionStorage.getItem("auth_token")}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Login"})
    }
  }
  ,
  methods: {
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
      this.addForm = true
    },
    openEditForm(id, title, text) {
      this.formTitle = "Редактирование новости"
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
      this.all = false
    }
  }
}
</script>

<style scoped>

</style>