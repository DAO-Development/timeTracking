<template>
  <div class="clients flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Клиенты</h3>
        <div class="addition-btn" @click="all = true" v-if="!all">
          <span>К списку клиентов</span>
          <back-icon/>
        </div>
      </div>
      <div class="clients-open">
        <div class="profile__image">
          <v-img
              v-if="currentProfile.photo_path" :lazy-src="require('../../../media'+currentProfile.photo_path)"
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
              <span class="profile__info-title">Дата рождения</span>
              <span class="profile__info-content">{{ currentProfile.birthdate }}</span>
            </li>
            <li>
              <span class="profile__info-title">Гражданство</span>
              <span class="profile__info-content">{{ currentProfile.citizenship }}</span>
            </li>
            <li>
              <span class="profile__info-title">Должность</span>
              <span class="profile__info-content">{{ currentProfile.position }}</span>
            </li>
            <li>
              <span class="profile__info-title">Номер соц. страхования</span>
              <span class="profile__info-content">{{ currentProfile.social_code_own }}</span>
            </li>
            <li>
              <span class="profile__info-title">Финский номер соц. страхования</span>
              <span class="profile__info-content">{{ currentProfile.social_code_fin }}</span>
            </li>
            <li>
              <span class="profile__info-title">Работает</span>
              <v-checkbox v-model="currentProfile.active" @change="openConfirmArchiveDialog"></v-checkbox>
            </li>
          </ul>
          <h3>Контакты</h3>
          <ul>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentProfile.phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">Телефон в Финляндии</span>
              <span class="profile__info-content">{{ currentProfile.phone_fin }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentProfile.auth_user_id.email }}</span>
            </li>
          </ul>
          <h3>Банковская информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Налоговый номер</span>
              <span class="profile__info-content">{{ currentProfile.tax_number }}</span>
            </li>
            <li>
              <span class="profile__info-title">Счет в банке</span>
              <span class="profile__info-content">{{ currentProfile.bank_account }}</span>
            </li>
          </ul>
          <div class="profile__info profile__info-full" v-if="full">
            <h3>Адреса</h3>
            <ul>
              <li>
                <span class="profile__info-title">Адрес в своей стране</span>
                <span class="profile__info-content" v-if="currentProfile.address_own !== null">{{
                    currentProfile.address_own.index
                  }} {{ currentProfile.address_own.country }}, г.{{
                    currentProfile.address_own.city
                  }}, {{ currentProfile.address_own.street }}, д.{{
                    currentProfile.address_own.house
                  }}, {{ currentProfile.address_own.entrance }}, кв.{{ currentProfile.address_own.flat }}</span>
              </li>
              <li>
                <span class="profile__info-title">Адрес в Финляндии</span>
                <span class="profile__info-content" v-if="currentProfile.address_fin !== null">{{
                    currentProfile.address_fin.index
                  }} {{ currentProfile.address_fin.country }}, г.{{
                    currentProfile.address_fin.city
                  }}, {{ currentProfile.address_fin.street }}, д.{{
                    currentProfile.address_fin.house
                  }}, {{ currentProfile.address_fin.entrance }}, кв.{{ currentProfile.address_fin.flat }}</span>
              </li>
            </ul>
            <h3>Одежда (размеры)</h3>
            <ul>
              <li>
                <span class="profile__info-title">Ботинки</span>
                <span class="profile__info-content">{{ currentProfile.boots }}</span>
              </li>
              <li>
                <span class="profile__info-title">Куртка</span>
                <span class="profile__info-content">{{ currentProfile.jacket }}</span>
              </li>
              <li>
                <span class="profile__info-title">Штаны</span>
                <span class="profile__info-content">{{ currentProfile.pants }}</span>
              </li>
              <li>
                <span class="profile__info-title">Футболка</span>
                <span class="profile__info-content">{{ currentProfile.shirt }}</span>
              </li>
            </ul>
            <h3>Языки</h3>
            <ul>
              <li>
                <span class="profile__info-title">Русский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.russian" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Английский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.english" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Эстонский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.estonian" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Финский</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.finnish" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Другие</span>
                <span class="profile__info-content">{{ currentProfile.other_language }}</span>
              </li>
            </ul>
            <h3>Другое</h3>
            <ul>
              <li>
                <span class="profile__info-title">Свой автомобиль</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.auto" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Свой инструмент</span>
                <v-checkbox class="profile__info-content" v-model="currentProfile.tool" disabled></v-checkbox>
              </li>
              <li>
                <span class="profile__info-title">Навыки</span>
                <span class="profile__info-content">{{ currentProfile.skills }}</span>
              </li>
            </ul>
          </div>
          <div class="open__actions">
            <div class="addition-btn" @click="full = !full">
              <span v-if="full">Скрыть полную информацию</span>
              <span v-if="!full">Показать полную информацию</span>
            </div>
            <div class="addition-btn"
                 @click="$router.push({name: 'Documents', params: {type: 'worker', id: currentProfile.id}})">
              Документы
            </div>
          </div>
          <div class="news-open__actions open__actions">
            <div class="addition-btn" @click="openEditForm(currentProfile)">
              <edit-icon/>
              Редактировать работника
            </div>
            <div class="addition-btn" @click="openConfirmDeleteDialog(currentProfile)">
              <waste-icon/>
              Удалить работника
            </div>
          </div>
        </div>
      </div>
    </div>
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
import BackIcon from "../components/icons/backIcon";

export default {
  name: "ClientOpen",
  components: {BackIcon},
  created() {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth-token')) {
      this.$emit('set-auth')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth-token'))}
      })
      this.loadData()
    } else {
      this.$router.push({name: "Index"})
    }
  }
}
</script>

<style scoped>

</style>