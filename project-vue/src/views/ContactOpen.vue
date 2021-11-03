<template>
  <div class="contacts flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Клиенты</h3>
        <div class="addition-btn" @click="$router.go(-1)">
          <span>К списку контактов</span>
          <back-icon/>
        </div>
      </div>
      <div class="clients-open workers-open">
        <div class="profile__image clients-open__image">
          <v-img
              v-if="currentClient.logo_path" :lazy-src="require('../../../media'+currentClient.logo_path)"
              :src="require('../../../media'+currentClient.logo_path)"></v-img>
          <div class="profile__change-photo" @click="photoDialog = true">Сменить фото</div>
        </div>
        <div class="profile__info">
          <h3>Общая информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Название</span>
              <span class="profile__info-content">{{ currentClient.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Краткое название</span>
              <span class="profile__info-content">{{ currentClient.short_name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Отрасль</span>
              <span class="profile__info-content">{{ currentClient.branch }}</span>
            </li>
            <li>
              <span class="profile__info-title">ОГРН</span>
              <span class="profile__info-content">{{ currentClient.ogrn }}</span>
            </li>
          </ul>
          <h3>Контакты</h3>
          <ul>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentClient.phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentClient.email }}</span>
            </li>
            <li>
              <span class="profile__info-title">Сайт</span>
              <span class="profile__info-content">{{ currentClient.site }}</span>
            </li>
          </ul>

          <div class="profile__info profile__info-full" v-if="full">
            <h3>Адреса</h3>
            <ul>
              <li>
                <span class="profile__info-title">Юридический адрес</span>
                <span class="profile__info-content"
                      v-if="currentClient.business_address !== null || currentClient.business_address.city !== ''">{{
                    currentClient.business_address.index
                  }} {{ currentClient.business_address.country }}, г.{{
                    currentClient.business_address.city
                  }}, {{ currentClient.business_address.street }}, д.{{
                    currentClient.business_address.house
                  }}, {{ currentClient.business_address.entrance }}, кв.{{ currentClient.business_address.flat }}</span>
              </li>
              <li>
                <span class="profile__info-title">Адрес доставки</span>
                <span class="profile__info-content"
                      v-if="currentClient.warehouse_address.city !== ''">{{
                    currentClient.warehouse_address.index
                  }} {{ currentClient.warehouse_address.country }}, г.{{
                    currentClient.warehouse_address.city
                  }}, {{ currentClient.warehouse_address.street }}, д.{{
                    currentClient.warehouse_address.house
                  }}, {{ currentClient.warehouse_address.entrance }}, кв.{{
                    currentClient.warehouse_address.flat
                  }}</span>
              </li>
            </ul>
            <h3>Банковская информация</h3>
            <ul>
              <li>
                <span class="profile__info-title">Банковский счет</span>
                <span class="profile__info-content">{{ currentClient.bank_account }}</span>
              </li>
              <li>
                <span class="profile__info-title">Банк</span>
                <span class="profile__info-content">{{ currentClient.bank }}</span>
              </li>
              <li>
                <span class="profile__info-title">BIC/SWIFT</span>
                <span class="profile__info-content">{{ currentClient.bic }}</span>
              </li>
              <li>
                <span class="profile__info-title">НДС</span>
                <span class="profile__info-content">{{ currentClient.vat }}%</span>
              </li>
            </ul>
            <h3>Электронные счета</h3>
            <ul>
              <li>
                <span class="profile__info-title">Оператор электронных счетов</span>
                <span class="profile__info-content">{{ currentClient.account_operator }}</span>
              </li>
              <li>
                <span class="profile__info-title">Индекс посредника</span>
                <span class="profile__info-content">{{ currentClient.index_operator }}</span>
              </li>
              <li>
                <span class="profile__info-title">Номер электронных счетов</span>
                <span class="profile__info-content">{{ currentClient.electronic_number }}</span>
              </li>
              <li>
                <span class="profile__info-title">Email для счетов</span>
                <span class="profile__info-content">{{ currentClient.account_email }}</span>
              </li>
            </ul>
          </div>
          <div class="open__actions">
            <div class="addition-btn" @click="full = !full">
              <span v-if="full">Скрыть полную информацию</span>
              <span v-if="!full">Показать полную информацию</span>
            </div>
          </div>
          <div class="news-open__actions open__actions">
            <div class="addition-btn" @click="openEditForm">
              <edit-icon/>
              Редактировать клиента
            </div>
            <div class="addition-btn" @click="confirmDeleteDialog = true">
              <waste-icon/>
              Удалить клиента
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
          <v-form ref="addForm" :model="newContact">
            <v-row>
              <v-text-field placeholder="Фамилия*" v-model="newContact.lastname" :rules="reqRules" required
                            outlined></v-text-field>
              <v-text-field placeholder="Имя*" v-model="newContact.name" :rules="reqRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-combobox placeholder="Фирма*" v-model="newContact.client" :items="selectsClient" item-text="name"
                          item-value="id" :rules="reqRules" required outlined></v-combobox>
              <v-combobox placeholder="Должность*" v-model="newContact.position" :items="selectsPosition"
                          :rules="reqRules" required outlined></v-combobox>
            </v-row>
            <h4>Контакты</h4>
            <v-row>
              <v-text-field placeholder="Телефон" v-model="newContact.phone" outlined></v-text-field>
              <v-text-field placeholder="Рабочий телефон*" v-model="newContact.work_phone" :rules="phoneRules"
                            required outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Почта" v-model="newContact.email" required outlined></v-text-field>
              <v-text-field placeholder="Рабочая почта*" v-model="newContact.work_email" :rules="emailRules" required
                            outlined></v-text-field>
            </v-row>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addContact">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление контакта
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить контакт и все зависящие от него объекты? Отменить это действие
          будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteClient">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="photoDialog" max-width="500">
      <v-card>
        <v-card-title>
          Сменить фото
        </v-card-title>
        <v-card-text>
          <v-file-input v-model="photoField" placeholder="Логотип организации" accept="image"
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
import BackIcon from "../components/icons/backIcon";

export default {
  name: "ContactOpen",
  components: {BackIcon},
  props: {
    id: [String, Number]
  },
}
</script>

<style scoped>

</style>