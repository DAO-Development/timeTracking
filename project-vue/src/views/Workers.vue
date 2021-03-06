<template>
  <div class="workers flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Работники</h3>
        <div class="addition-btn" @click="all = true" v-if="!all">
          <span>К списку работников</span>
          <back-icon />
        </div>
        <div
          class="addition-btn content-list__filters-mobile"
          v-if="all"
          @click="openFilters"
        >
          Фильтры
        </div>
      </div>
      <div class="workers-all all" v-if="all">
        <div class="content-list__filters">
          <v-icon color="grey lighten-1" @click="closeFilters">
            $deleteIcon
          </v-icon>
          <v-text-field
            placeholder="Фамилия Имя"
            v-model="filter.name"
            outlined
          ></v-text-field>
          <v-select
            v-model="filter.position"
            :items="[{ id: 0, name: 'Все' }].concat(positions)"
            item-text="name"
            item-value="name"
            placeholder="Должность"
            outlined
          ></v-select>
          <v-text-field
            placeholder="Почта"
            v-model="filter.email"
            outlined
          ></v-text-field>
        </div>
        <v-list three-line class="workers__list content-list">
          <template v-for="profile in profiles">
            <v-list-item
              :key="profile.id"
              v-if="
                profile.active !== archive &&
                profile.auth_user_id.email.includes(filter.email) &&
                (profile.name + ' ' + profile.lastname).includes(filter.name) &&
                (profile.position.name === filter.position ||
                  filter.position === 'Все')
              "
            >
              <v-list-item-avatar class="content-list__image">
                <v-img
                  v-if="profile.photo_path"
                  :src="$hostname + 'media' + profile.photo_path"
                ></v-img>
              </v-list-item-avatar>
              <v-list-item-content
                @click="
                  $router.push({
                    name: 'WorkerOpen',
                    params: { id: profile.id },
                  })
                "
              >
                <v-list-item-title
                  >{{ profile.lastname }} {{ profile.name }}</v-list-item-title
                >
                <v-list-item-subtitle>
                  <span v-if="profile.position.name !== null">{{
                    profile.position.name
                  }}</span
                  ><br />
                  <span>{{ profile.auth_user_id.email }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action
                v-if="$parent.$parent.edit.indexOf('Работники') !== -1"
              >
                <v-icon
                  color="grey lighten-1"
                  @click="openConfirmDeleteDialog(profile)"
                >
                  $deleteIcon
                </v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
        <v-list class="content-list__btns">
          <v-list-item
            v-if="!archive && $parent.$parent.edit.indexOf('Работники') !== -1"
            class="content-list__btns-add"
            @click="openAddForm"
          >
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить работника</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-if="!archive"
            class="content-list__btns-add"
            @click="archive = !archive"
          >
            <v-list-item-icon>
              <v-icon>$archive</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Архив</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-else
            class="content-list__btns-add"
            @click="archive = !archive"
          >
            <v-list-item-icon>
              <v-icon>$archive</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Выйти из архива</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
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
          <v-form ref="addForm" :model="newProfile">
            <v-row>
              <v-text-field
                placeholder="Фамилия*"
                v-model="newProfile.lastname"
                :rules="reqRules"
                required
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Имя*"
                v-model="newProfile.name"
                :rules="reqRules"
                required
                outlined
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                placeholder="Гражданство*"
                v-model="newProfile.citizenship"
                :rules="reqRules"
                required
                outlined
              ></v-text-field>
              <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                :return-value.sync="newProfile.birthdate"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="newProfile.birthdate"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    placeholder="Дата рождения*"
                    :rules="reqRules"
                    outlined
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="newProfile.birthdate"
                  no-title
                  scrollable
                >
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="menu = false">
                    Cancel</v-btn
                  >
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.menu.save(newProfile.birthdate)"
                  >
                    OK</v-btn
                  >
                </v-date-picker>
              </v-menu>
            </v-row>
            <v-row>
              <v-text-field
                placeholder="Номер социального страхования"
                v-model="newProfile.social_code_own"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Номер соц. страхования в Финляндии*"
                v-model="newProfile.social_code_fin"
                :rules="reqRules"
                required
                outlined
              ></v-text-field>
            </v-row>
            <h4>Адрес в своей стране</h4>
            <v-row>
              <v-text-field
                placeholder="Страна"
                v-model="newProfile.address_own.country"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Город"
                v-model="newProfile.address_own.city"
                outlined
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                placeholder="Улица"
                v-model="newProfile.address_own.street"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Индекс"
                v-model="newProfile.address_own.index"
                outlined
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                placeholder="Дом"
                v-model="newProfile.address_own.house"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Подъезд"
                v-model="newProfile.address_own.entrance"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Квартира"
                v-model="newProfile.address_own.flat"
                outlined
              ></v-text-field>
            </v-row>
            <h4>Адрес в Финляндии</h4>
            <v-row>
              <v-text-field
                placeholder="Страна"
                v-model="newProfile.address_fin.country"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Город"
                v-model="newProfile.address_fin.city"
                outlined
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                placeholder="Улица"
                v-model="newProfile.address_fin.street"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Индекс"
                v-model="newProfile.address_fin.index"
                outlined
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                placeholder="Дом"
                v-model="newProfile.address_fin.house"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Подъезд"
                v-model="newProfile.address_fin.entrance"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Квартира"
                v-model="newProfile.address_fin.flat"
                outlined
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                placeholder="Телефон"
                v-model="newProfile.phone"
                :rules="phoneRules"
                required
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Телефон в Финляндии*"
                v-model="newProfile.phone_fin"
                :rules="phoneFinRules"
                required
                outlined
              ></v-text-field>
            </v-row>
            <v-text-field
              placeholder="Почта*"
              v-model="newProfile.email"
              :rules="emailRules"
              required
              outlined
            ></v-text-field>
            <v-text-field
              placeholder="Номер счета в банке*"
              v-model="newProfile.bank_account"
              :rules="reqRules"
              required
              outlined
            ></v-text-field>
            <v-text-field
              placeholder="Налоговый номер*"
              v-model="newProfile.tax_number"
              :rules="reqRules"
              required
              outlined
            ></v-text-field>
            <v-row>
              <v-checkbox
                label="Свой автомобиль"
                v-model="newProfile.auto"
              ></v-checkbox>
              <v-checkbox
                label="Свой инструмент"
                v-model="newProfile.tool"
              ></v-checkbox>
            </v-row>
            <v-row>
              Категория прав
              <v-radio-group v-model="newProfile.auto_category">
                <v-radio value="A" label="A"></v-radio>
                <v-radio value="B" label="B"></v-radio>
                <v-radio value="C" label="C"></v-radio>
                <v-radio value="D" label="D"></v-radio>
                <v-radio value="BE" label="BE"></v-radio>
                <v-radio value="CE" label="CE"></v-radio>
                <v-radio value="DE" label="DE"></v-radio>
              </v-radio-group>
            </v-row>
            <h4>Языки</h4>
            <v-row>
              <v-checkbox
                label="Английский"
                v-model="newProfile.english"
              ></v-checkbox>
              <v-checkbox
                label="Финский"
                v-model="newProfile.finnish"
              ></v-checkbox>
              <v-checkbox
                label="Русский"
                v-model="newProfile.russian"
              ></v-checkbox>
              <v-checkbox
                label="Эстонский"
                v-model="newProfile.estonian"
              ></v-checkbox>
            </v-row>
            <v-text-field
              placeholder="Другие языки"
              v-model="newProfile.other_language"
              outlined
            ></v-text-field>
            <v-combobox
              ref="positionCombobox"
              v-model="newProfile.position"
              :items="positions"
              item-value="id"
              item-text="name"
              placeholder="Должность*"
              outlined
              dense
              :rules="reqRules"
            ></v-combobox>
            <v-textarea
              placeholder="Что умеете делать?"
              v-model="newProfile.skills"
              outlined
            ></v-textarea>
            <h4>Одежда</h4>
            <v-row>
              <v-text-field
                placeholder="Ботинки"
                v-model="newProfile.boots"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Куртка"
                v-model="newProfile.jacket"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Штаны"
                v-model="newProfile.pants"
                outlined
              ></v-text-field>
              <v-text-field
                placeholder="Футболка"
                v-model="newProfile.shirt"
                outlined
              ></v-text-field>
            </v-row>
            <h3>Карточки</h3>
            <v-row>
              <v-btn @click="addProfileCard">Добавить карточку</v-btn>
            </v-row>
            <template v-for="i in cardsQuantity">
              <div :key="i">
                <v-row>
                  <v-autocomplete
                    :items="cards"
                    item-value="id"
                    item-text="name"
                    v-model="newProfile.cards[i - 1].card"
                    :rules="reqRules"
                    outlined
                  ></v-autocomplete>
                </v-row>
                <v-row>
                  <v-text-field
                    v-model="newProfile.cards[i - 1].number"
                    :rules="reqRules"
                    outlined
                  ></v-text-field>
                  <v-menu
                    ref="menuCard"
                    v-model="menuCard"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="newProfile.cards[i - 1].due_date"
                        label="Срок действия"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                        outlined
                      ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="newProfile.cards[i - 1].due_date"
                      @input="menuCard = false"
                      type="month"
                      :min="new Date(Date.now()).toISOString().substr(0, 7)"
                    ></v-date-picker>
                  </v-menu>
                </v-row>
              </div>
            </template>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addUser">{{
            formBtnText
          }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title> Удаление работника </v-card-title>
        <v-card-text
          >Вы действительно хотите удалить профиль? Отменить это действие будет
          невозможно</v-card-text
        >
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false"
            >Отменить</v-btn
          >
          <v-btn color="primary" text @click="deleteUser(null)"
            >Подтвердить</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmArchiveDialog" max-width="500">
      <v-card>
        <v-card-title> Увольнение работника </v-card-title>
        <v-card-text>
          Вы действительно хотите уволить работника? После подтверждения профиль
          будет перемещен в архив
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
        <v-card-title> Сменить фото </v-card-title>
        <v-card-text>
          <v-file-input
            v-model="photoField"
            placeholder="Фото профиля"
            accept="image/*"
            prepend-icon=""
            outlined
          ></v-file-input>
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
// import PdfIcon from "../components/icons/pdfIcon";
import BackIcon from "../components/icons/backIcon";
// import EditIcon from "../components/icons/editIcon";
// import WasteIcon from "../components/icons/wasteIcon";

export default {
  name: "Workers",
  components: { /*WasteIcon, EditIcon,*/ BackIcon /*PdfIcon*/ },
  data() {
    return {
      page: "home",
      all: true,
      full: false,
      archive: false,
      profiles: {},
      positions: [],
      cards: [],
      // selects: ["Все", "Администратор", "Маляр", "Строитель"],
      newProfile: {
        id: 0,
        lastname: "",
        name: "",
        citizenship: "",
        birthdate: "",
        social_code_own: "",
        social_code_fin: "",
        address_own: {
          index: "",
          country: "",
          city: "",
          street: "",
          house: "",
          entrance: "",
          flat: "",
        },
        address_fin: {
          index: "",
          country: "",
          city: "",
          street: "",
          house: "",
          entrance: "",
          flat: "",
        },
        phone: "",
        phone_fin: "",
        email: "",
        bank_account: "",
        tax_number: "",
        auto: false,
        auto_category: null,
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
        is_staff: false,
        photo_path: null,
        cards: [],
      },
      cardsQuantity: 0,
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
        email: "",
      },
      formTitle: "Добавление работника",
      formBtnText: "Добавить работника",
      addForm: false,
      confirmArchiveDialog: false,
      confirmDeleteDialog: false,
      photoField: null,
      photoDialog: false,
      menu: false,
      menuCard: false,
      alertError: false,
      alertMsg: "",
      reqRules: [(v) => !!v || "Необходимо заполнить поле"],
      emailRules: [
        (v) => !!v || "Необходимо заполнить поле",
        (v) =>
          /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
            v
          ) || "Некорректный E-mail",
      ],
      phoneRules: [
        // v => !!v || '',
        (v) =>
          /^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$/.test(
            v
          ) || "Некорректный номер телефона",
      ],
      phoneFinRules: [
        (v) => !!v || "Необходимо заполнить поле",
        (v) =>
          /^((([+][\s]{0,1})|([0]{2}[\s-]{0,1}))([358]{3})([\s-]{0,1})|([0]{1}))(([1-9]{1}[0-9]{0,1})([\s-]{0,1})([0-9]{2,4})([\s-]{0,1})([0-9]{2,4})([\s-]{0,1}))([0-9]{0,3}){1}$/.test(
            v
          ) || "Некорректный номер телефона",
      ],
    };
  },
  mounted() {
    console.log("init Workers");
    if (
      localStorage.getItem("auth_token") ||
      sessionStorage.getItem("auth_token")
    ) {
      this.$emit("set-auth");
      this.$emit("load-functions");
      if (this.$parent.$parent.read.indexOf("Работники") === -1)
        this.$router.push({ name: "Index" });
      $.ajaxSetup({
        headers: {
          Authorization:
            "Token " +
            (localStorage.getItem("auth_token") ||
              sessionStorage.getItem("auth_token")),
        },
      });
      this.loadData();
      this.loadPositions();
      this.loadCards();
    } else {
      this.$emit("set-not-auth");
      this.$router.push({ name: "Index" });
    }
  },
  methods: {
    allowedMonths: (val) => val >= Date.now(),
    loadData() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "GET",
        success: (response) => {
          this.profiles = response.data.data;
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером";
          } else if (response.status === 401) {
            this.$refresh();
          } else {
            this.alertMsg = "Непредвиденная ошибка";
          }
          this.alertError = true;
        },
      });
    },
    loadPositions() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles/positions",
        type: "GET",
        success: (response) => {
          this.positions = response.data.data;
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером";
          } else if (response.status === 401) {
            this.$refresh();
          } else {
            this.alertMsg = "Непредвиденная ошибка";
          }
          this.alertError = true;
        },
      });
    },
    loadCards() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles/cards",
        type: "GET",
        success: (response) => {
          this.cards = response.data.data;
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером";
          } else if (response.status === 401) {
            this.$refresh();
          } else {
            this.alertMsg = "Непредвиденная ошибка";
          }
          this.alertError = true;
        },
      });
    },
    addUser() {
      if (this.$refs.addForm.validate()) {
        if (this.newProfile.id !== 0) {
          this.editProfile();
        } else {
          $.ajax({
            url: this.$hostname + "time-tracking/user",
            type: "POST",
            data: {
              username: this.newProfile.email,
              email: this.newProfile.email,
              is_staff: this.newProfile.is_staff,
              password: "12345678",
            },
            success: (response) => {
              this.addProfile(response.data.data.id);
            },
            error: (response) => {
              if (response.status === 500) {
                this.alertMsg = "Ошибка соединения с сервером";
              } else if (response.status === 401) {
                this.$refresh();
              } else {
                this.alertMsg = "Непредвиденная ошибка";
              }
              this.alertError = true;
            },
          });
        }
      } else {
        this.alertError = true;
        this.alertMsg = "Заполните все обязательные поля";
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
          citizenship: this.newProfile.citizenship,
          birthdate: this.newProfile.birthdate,
          social_code_own: this.newProfile.social_code_own,
          social_code_fin: this.newProfile.social_code_fin,
          address_own: JSON.stringify(this.newProfile.address_own),
          address_fin: JSON.stringify(this.newProfile.address_fin),
          phone: this.newProfile.phone,
          phone_fin: this.newProfile.phone_fin,
          bank_account: this.newProfile.bank_account,
          tax_number: this.newProfile.tax_number,
          auto: this.newProfile.auto,
          auto_category: this.newProfile.auto_category,
          tool: this.newProfile.tool,
          english: this.newProfile.english,
          estonian: this.newProfile.estonian,
          finnish: this.newProfile.finnish,
          russian: this.newProfile.russian,
          other_language: this.newProfile.other_language,
          position: this.newProfile.position.id,
          skills: this.newProfile.skills,
          boots: this.newProfile.boots,
          jacket: this.newProfile.jacket,
          pants: this.newProfile.pants,
          shirt: this.newProfile.shirt,
          photo_path: this.currentProfile.photo_path,
          active: true,
          cards: JSON.stringify(this.newProfile.cards),
        },
        success: () => {
          this.alertMsg = "Пользователь добавлен";
          this.closeForm();
          this.loadData();
        },
        error: (response) => {
          this.alertError = true;
          this.alertMsg = "Непредвиденная ошибка";
          console.log(response);
        },
      });
    },
    addProfileCard() {
      this.cardsQuantity += 1;
      this.newProfile.cards.push({ card: 0, number: "", due_date: "" });
    },
    editProfile() {
      $.ajax({
        url: this.$hostname + "time-tracking/profiles",
        type: "PUT",
        data: this.currentProfile,
        success: () => {
          console.log("Профиль изменен");
          if (this.addForm) {
            this.editUser();
          } else {
            this.confirmArchiveDialog = false;
            this.loadData();
          }
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером";
          } else if (response.status === 401) {
            this.$refresh();
          } else {
            this.alertMsg = "Непредвиденная ошибка";
          }
          this.alertError = true;
        },
      });
    },
    editUser() {
      this.currentProfile.auth_user_id.email = this.newProfile.email;
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "PUT",
        data: {
          id: this.newProfile.auth_user_id.id,
          username: this.newProfile.email,
          email: this.newProfile.email,
        },
        success: () => {
          console.log("Пользователь изменен");
          this.loadData();
          this.closeForm();
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером";
          } else if (response.status === 401) {
            this.$refresh();
          } else {
            this.alertMsg = "Непредвиденная ошибка";
          }
          this.alertError = true;
        },
      });
    },
    savePhoto() {
      const axios = require("axios");
      // чтение файла в formData
      let fd = new FormData();
      let avatar = this.photoField;
      if (avatar !== undefined) {
        fd.append("image", avatar);
      } else {
        console.log("ERROR");
        return;
      }
      axios({
        method: "put",
        url:
          this.$hostname + "time-tracking/profiles/" + this.currentProfile.id,
        headers: {
          Authorization:
            "Token " +
            (localStorage.getItem("auth_token") ||
              sessionStorage.getItem("auth_token")),
          "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').attr("value"),
        },
        data: fd,
      }).then((response) => {
        console.log(response.data);
        this.photoDialog = false;
        this.photoField = null;
        this.currentProfile.photo_path = response.data.name;
        this.loadData();
      });
    },
    deleteUser(email) {
      if (email == null) {
        email = this.currentProfile.email;
      }
      console.log(email);
      $.ajax({
        url: this.$hostname + "time-tracking/user",
        type: "DELETE",
        data: {
          email: email,
        },
        success: () => {
          this.alertMsg = "Пользователь удален";
          this.loadData();
          this.confirmDeleteDialog = false;
        },
        error: (response) => {
          if (response.status === 500) {
            this.alertMsg = "Ошибка соединения с сервером";
          } else if (response.status === 401) {
            this.$refresh();
          } else {
            this.alertMsg = "Непредвиденная ошибка";
          }
          this.alertError = true;
        },
      });
    },
    openProfile(profile) {
      this.currentProfile = profile;
      this.all = false;
    },
    closeForm() {
      this.addForm = false;
      this.newProfile = {
        id: 0,
        lastname: "",
        name: "",
        citizenship: "",
        birthdate: "",
        social_code_own: "",
        social_code_fin: "",
        address_own: {
          index: "",
          country: "",
          city: "",
          street: "",
          house: "",
          entrance: "",
          flat: "",
        },
        address_fin: {
          index: "",
          country: "",
          city: "",
          street: "",
          house: "",
          entrance: "",
          flat: "",
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
        is_staff: false,
      };
    },
    openAddForm() {
      this.formTitle = "Добавление работника";
      this.formBtnText = "Добавить работника";
      this.addForm = true;
    },
    openEditForm(item) {
      this.formTitle = "Редактирование работника";
      this.formBtnText = "Сохранить работника";
      this.newProfile = item;
      this.newProfile.email = item.auth_user_id.email;
      this.addForm = true;
    },
    openConfirmArchiveDialog() {
      console.log(this.currentProfile.id);
      if (
        (!this.currentProfile.active && !this.all) ||
        (this.currentProfile.active && this.all)
      ) {
        this.currentProfile.active = false;
        this.confirmArchiveDialog = true;
      } else {
        this.editProfile();
      }
    },
    cancelConfirmArchiveDialog() {
      this.currentProfile.active = true;
      this.confirmArchiveDialog = false;
    },
    openConfirmDeleteDialog(item) {
      this.currentProfile = item;
      this.currentProfile.email = item.auth_user_id.email;
      if (this.archive || !this.all) {
        this.confirmDeleteDialog = true;
      } else {
        this.openConfirmArchiveDialog();
      }
    },
    openFilters() {
      console.log("open filters");
      $(".content-list__filters").addClass("open");
      $(".content-list__btns").addClass("hidden");
    },
    closeFilters() {
      console.log("open filters");
      $(".content-list__filters").removeClass("open");
      $(".content-list__btns").removeClass("hidden");
    },
  },
};
</script>

<style scoped></style>
