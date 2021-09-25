<template>
  <div class="flex-main">
    <Menu class="flex-sidebar"/>
    <div class="news flex-content">
      <div class="summary-box">
        <template v-for="item in news">
          <v-card class="news-single" :key="item.id" color="primary">
            <div class="news-single__actions">
              <waste-icon @click="deleteNew(item.id)"/>
              <v-icon @click="openEditForm">$edit</v-icon>
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
    </div>
    <v-dialog v-model="addForm" persistent>
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
          <v-textarea placeholder="Текст новости" v-model="newNew.text" outlined></v-textarea>
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
</template>

<script>
import $ from "jquery";
import Menu from "../components/Menu";
import AddPhotoIcon from "../components/icons/addPhotoIcon";
import AddNewIcon from "../components/icons/addNewIcon";
import WasteIcon from "../components/icons/wasteIcon";

export default {
  name: "News",
  components: {WasteIcon, AddNewIcon, AddPhotoIcon, Menu},
  data() {
    return {
      page: 'news',
      news: '',
      newNew: {
        title: '',
        text: ''
      },
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
      $.ajax({
        url: this.$hostname + "time-tracking/news",
        type: "POST",
        data: this.newNew,
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
    editNew(id) {
      $.ajax({
        url: this.$hostname + "time-tracking/news",
        type: "PUT",
        data: {
          id: id,
          title: this.newNew.title,
          text: this.newNew.text
        },
        success: () => {
          this.alertMsg = "Новость изменена"
          this.loadData()
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
    openEditForm() {
      this.formTitle = "Редактирование новости"
      this.addForm = true
    },
    closeForm() {
      this.addForm = false
      this.newNew = {
        title: "",
        text: "",
      }
    },
  }
}
</script>

<style scoped>

</style>