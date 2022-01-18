<template>
  <div class="accounting flex-content">
    <Header/>
    <section class="summary-box">
      <div class="summary-box__title">
        <h1>{{ title }}</h1>
        <div class="addition-btn" @click="$router.push({name: 'Accounting', params: {type: type}})">
          <span>К списку документов</span>
          <back-icon/>
        </div>
      </div>
      <div class="document">
        <h3>{{ currentDocument.name }}</h3>
        <div class="document_date">Дата создания: {{ currentDocument.create_date }}</div>
        <div class="document_client" v-if="type === 'contracts' || type === 'property'">
          Клиент: {{ currentDocument.client.name }}
        </div>
        <strong>Документы:</strong>
        <ul class="document_path">
          <template v-for="item in currentDocument.path.split(';')">
            <li @click="downloadFile(item)" :key="item">{{ item.substr(item.lastIndexOf('/') + 1) }}</li>
          </template>
        </ul>
        <v-btn class="action-btn" color="primary" @click="downloadAll">Скачать все файлы</v-btn>
      </div>
    </section>
  </div>
</template>

<script>
import Header from "../../components/Header";
import $ from "jquery";
import BackIcon from "../../components/icons/backIcon";

export default {
  name: "AccountingOpen",
  components: {BackIcon, Header},
  props: {
    type: String,
    id: [String, Number]
  },
  data() {
    return {
      title: '',
      url: '',
      mode: 0,
      clients: [],
      currentDocument: {
        id: 0,
        name: '',
        create_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        path: '',
        client: '',
      },
      menu: false,
      addForm: false,
      confirmDeleteDialog: false,
      alertError: false,
      alertMsg: "",
      reqRules: [
        v => !!v || 'Необходимо заполнить поле',
      ],
    }
  },
  created() {
    console.log("init Accounting " + this.type)
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      switch (this.type) {
        case 'reports':
          this.title = "Бухгалтерские отчеты"
          this.url = "time-tracking/accounting/documents"
          this.mode = 1
          break
        case 'extracts':
          this.title = "Бухгалтерские выписки"
          this.url = "time-tracking/accounting/documents"
          this.mode = 2
          break
        case 'documents':
          this.title = "Бухгалтерские документы"
          this.url = "time-tracking/accounting/documents"
          this.mode = 3
          break
        case 'contracts':
          this.title = "Договора с клиентами"
          this.url = "time-tracking/accounting/documents-client"
          this.mode = 4
          this.loadClients()
          break
        case 'property':
          this.title = "Документы на собственность"
          this.url = "time-tracking/accounting/documents-client"
          this.mode = 5
          this.loadClients()
          break
      }
      this.loadData()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    loadData() {
      $.ajax({
        url: this.$hostname + this.url + "/" + this.mode + "/" + this.id,
        type: "GET",
        success: (response) => {
          this.currentDocument = response.data.data[0]
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
    loadClients() {
      $.ajax({
        url: this.$hostname + "time-tracking/clients",
        type: "GET",
        success: (response) => {
          this.clients = response.data.data
        },
        error: (response) => {
          console.log(response)
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
    downloadFile(item) {
      console.log(this.$hostname + 'media' + item)
      const axios = require('axios')
      axios({
        url: this.$hostname + 'media' + item,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement('a');

        fileLink.href = fileURL;
        fileLink.setAttribute('download', item);
        document.body.appendChild(fileLink);

        fileLink.click();
      });
    },
    downloadAll() {
      const axios = require('axios')
      $.ajax({
        url: this.$hostname + 'time-tracking/to-zip',
        type: "POST",
        data: {
          name: this.currentDocument.name,
          path: this.currentDocument.path
        },
        success: (response) => {
          console.log(response.data.name)
          let item = response.data.name
          axios({
            url: this.$hostname + item,
            method: 'GET',
            responseType: 'blob',
          }).then((response) => {
            var fileURL = window.URL.createObjectURL(new Blob([response.data]));
            var fileLink = document.createElement('a');

            fileLink.href = fileURL;
            fileLink.setAttribute('download', item.substr(item.lastIndexOf('/') + 1));
            document.body.appendChild(fileLink);

            fileLink.click();
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
    }
  }
}
</script>

<style scoped>

</style>