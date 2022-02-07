<template>
  <div class="documents flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Документы</h3>
        <div class="addition-btn" @click="$router.go(-1)">
          <span>Назад</span>
          <back-icon/>
        </div>
      </div>
      <div class="documents-all all">
        <v-data-table :headers="headers" :items="documents" item-key="id" @click:row="downloadFile">
          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="openEditForm(item)"
                    v-if="id === undefined || $parent.$parent.edit.indexOf('Работники') !== -1">
              mdi-pencil
            </v-icon>
            <v-icon small @click="openConfirmDeleteDialog(item)"
                    v-if="id === undefined || $parent.$parent.edit.indexOf('Работники') !== -1">
              mdi-delete
            </v-icon>
          </template>
          <template v-slot:no-data>
            Документы не загружены
          </template>
        </v-data-table>
        <v-list class="content-list__btns">
          <v-list-item class="content-list__btns-add"
                       v-if="id === undefined || $parent.$parent.edit.indexOf('Работники') !== -1"
                       @click="openAddForm">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить документ</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
    </div>
    <v-dialog v-model="addForm" max-width="500">
      <v-card>
        <v-card-title>
          {{ formTitle }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" :model="currentDocument">
            <v-text-field v-model="currentDocument.name" placeholder="Название документа*" outlined
                          :rules="reqRules" required></v-text-field>
            <v-btn v-if="!editFile" text @click="editFile=true">Изменить файл</v-btn>
            <v-file-input v-if="editFile" v-model="currentDocument.path" placeholder="Выберите документ*" accept="*"
                          prepend-icon="" outlined @change="showDoc" :rules="reqRules"></v-file-input>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="putDocument">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление документа
        </v-card-title>
        <v-card-text>
          Вы действительно хотите удалить выбранный документ? Отменить это действие будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteDocument">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import BackIcon from "../components/icons/backIcon";
import $ from "jquery";

export default {
  name: "Documents",
  components: {BackIcon},
  props: {
    type: String,
    id: [String, Number, undefined],
  },
  data() {
    return {
      profile: {},
      documents: [],
      currentDocument: {
        id: 0,
        name: null,
        create_date: null,
        path: null,
      },
      headers: [
        {text: 'Название', align: 'start', sortable: true, value: 'name',},
        {text: 'Дата создания', value: 'create_date'},
        {text: '', value: 'actions', sortable: false},
      ],
      formTitle: "Добавить документ",
      editFile: false,
      addForm: false,
      confirmDeleteDialog: false,
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
    }
  },
  created() {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      if (this.$parent.$parent.read.indexOf('Работники') === -1)
        this.$router.push({name: "Index"})
      this.$emit('set-auth')
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
    showDoc() {
      console.log(this.currentDocument.path.type)
    },
    loadData() {
      let url = ''
      if (this.id !== undefined)
        url = "time-tracking/documents/" + this.type + "/" + this.id
      else
        url = "time-tracking/documents/" + this.type
      $.ajax({
        url: this.$hostname + url,
        type: "GET",
        success: (response) => {
          this.documents = response.data.documents
          this.profile = response.data.profile
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
    putDocument() {
      if (this.$refs.form.validate()) {
        const axios = require('axios')
        // чтение файла в formData
        let fd = new FormData();
        if (this.editFile) {
          let document = this.currentDocument.path;
          if (document !== undefined) {
            fd.append('document', document)
          } else {
            console.log("ERROR")
            return
          }
        } else
          fd.append('path', this.currentDocument.path)
        fd.append('id', this.currentDocument.id)
        fd.append('create_date', this.currentDocument.create_date)
        fd.append('name', this.currentDocument.name)
        fd.append('user_profile_id', this.id)
        axios({
          method: 'put',
          url: this.$hostname + "time-tracking/documents/" + this.type,
          headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
          data: fd
        })
            .then(response => {
              console.log(response.data.data)
              this.addForm = false
              this.loadData()
            });
      }
    },
    deleteDocument() {
      $.ajax({
        url: this.$hostname + "time-tracking/documents/" + this.type,
        type: "DELETE",
        data: {
          "id": this.currentDocument.id
        },
        success: () => {
          console.log("Документ удален")
          this.confirmDeleteDialog = false
          this.loadData()
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
    downloadFile(item) {
      const axios = require('axios')
      axios({
        url: this.$hostname + 'media' + item.path,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement('a');

        fileLink.href = fileURL;
        fileLink.setAttribute('download', item.path);
        document.body.appendChild(fileLink);

        fileLink.click();
      });
    },
    openAddForm() {
      this.editFile = true
      this.formTitle = "Добавить документ"
      this.currentDocument = {
        id: 0,
        name: null,
        create_date: null,
        path: null,
      }
      this.addForm = true
    },
    openEditForm(item) {
      this.editFile = false
      this.formTitle = "Редактировать документ"
      this.currentDocument = item
      this.addForm = true
    },
    openConfirmDeleteDialog(item) {
      this.currentDocument = item
      this.confirmDeleteDialog = true
    }
  }
}
</script>

<style scoped>

</style>