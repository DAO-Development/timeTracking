<template>
  <div class="objects flex-content">
    <div class="summary-box">
      <div class="summary-box__title">
        <h3>Объекты</h3>
        <div class="addition-btn" @click="all = true" v-if="!all">
          <span>К списку объектов</span>
          <back-icon/>
        </div>
        <div class=" addition-btn content-list__filters-mobile" v-if="all"
             @click="openFilters">Фильтры
        </div>
      </div>
      <div class="objects-all all" v-if="all">
        <div class="content-list__filters">
          <v-icon color="grey lighten-1" @click="closeFilters">
            $deleteIcon
          </v-icon>
          <v-text-field placeholder="Адрес" v-model="filter.address" outlined></v-text-field>
          <v-select v-model="filter.client" :items="[{name: 'Все', id: 'Все'}].concat(clients)" item-text="name"
                    item-value="id" outlined></v-select>
          <v-menu ref="menu_filter" v-model="datePickers.menu_filter" :close-on-content-click="false"
                  :return-value.sync="filter.dates"
                  transition="scale-transition" offset-y min-width="auto">
            <template v-slot:activator="{ on, attrs }">
              <v-text-field v-model="filter.dates" placeholder="Начало работ" readonly v-bind="attrs"
                            v-on="on" outlined></v-text-field>
            </template>
            <v-date-picker v-model="filter.dates" no-title scrollable range color="primary">
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="datePickers.menu_filter = false"> Cancel</v-btn>
              <v-btn text color="primary" @click="$refs.menu_filter.save(filter.dates)">OK</v-btn>
            </v-date-picker>
          </v-menu>
        </div>
        <v-list three-line class="objects__list content-list">
          <template v-for="object in objects">
            <v-list-item :key="object.id"
                         v-if="object.active === archive && (object.city + ' ' + object.street + ' ' + object.house).includes(filter.address) && (filter.client==='Все' || object.client_id.id===filter.client) && ((typeof(filter.dates[0]) === 'undefined' || object.date_start >= filter.dates[0]) && (object.date_start <= filter.dates[1] || typeof(filter.dates[1]) === 'undefined'))">
              <v-list-item-content @click="openObject(object)">
                <v-list-item-title>{{ object.city }} {{ object.street }} {{ object.house }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span>{{ object.date_start }} - {{ object.date_end }}</span><br>
                  <span>{{ object.client_id.name }}</span>
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action v-if="$parent.$parent.edit.indexOf('Объекты') !== -1">
                <v-icon color="grey lighten-1" @click="openConfirmDeleteDialog(object)">$deleteIcon</v-icon>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
        <v-list class="content-list__btns">
          <v-list-item v-if="!archive && $parent.$parent.edit.indexOf('Объекты') !== -1" class="content-list__btns-add"
                       @click="openAddForm">
            <v-list-item-icon>
              <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Добавить объект</v-list-item-title>
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
      <div class="objects-open" v-else>
        <div class="profile__image">
          <v-img v-if="currentObject.photo_path != null && currentObject.photo_path != undefined"
                 :lazy-src="$hostname+'media'+currentObject.photo_path"
                 :src="$hostname+'media'+currentObject.photo_path"></v-img>
          <v-img v-else :lazy-src="$hostname+'media/objects/preview.jpg'"
                 :src="$hostname+'media/objects/preview.jpg'"></v-img>
          <v-btn class="action-btn" color="primary" v-if="$parent.$parent.edit.indexOf('Объекты') !== -1"
                 @click="photoDialog = true">
            Сменить фото
          </v-btn>
        </div>
        <div class="objects-open__info profile__info">
          <h3>Информация об объекте</h3>
          <div class="news-open__actions open__actions" v-if="$parent.$parent.edit.indexOf('Объекты') !== -1">
            <div class="addition-btn" @click="openEditForm(currentObject)">
              <edit-icon/>
              Редактировать объект
            </div>
            <div class="addition-btn" @click="deleteObject(currentObject.id)">
              <waste-icon/>
              Удалить объект
            </div>
          </div>
          <v-btn color="primary" @click="addTimingForm=true; newTiming.objects_id=currentObject.id; loadPositions()">
            Добавить часовой отчет
          </v-btn>
          <ul>
            <li>
              <span class="profile__info-title">Объект сдан</span>
              <v-checkbox v-model="currentObject.active" :disabled="$parent.$parent.edit.indexOf('Объекты') === -1"
                          @change="openConfirmArchiveDialog"></v-checkbox>
            </li>
            <li>
              <span class="profile__info-title">Клиент</span>
              <span class="profile__info-content">{{ currentObject.client_id.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Начало работ</span>
              <span class="profile__info-content">{{ currentObject.date_start }}</span>
            </li>
            <li>
              <span class="profile__info-title">Окончание работ</span>
              <span class="profile__info-content">{{ currentObject.date_end }}</span>
            </li>
            <li>
              <span class="profile__info-title">Описание работ</span>
              <span class="profile__info-content">{{ currentObject.work_description }}</span>
            </li>
          </ul>
          <h3>Адрес</h3>
          <ul>
            <li>
              <span class="profile__info-title">Улица</span>
              <span class="profile__info-content">{{ currentObject.street }}</span>
            </li>
            <li>
              <span class="profile__info-title">Дом</span>
              <span class="profile__info-content">{{ currentObject.house }}</span>
            </li>
            <li>
              <span class="profile__info-title">Подъезд</span>
              <span class="profile__info-content">{{ currentObject.entrance }}</span>
            </li>
            <li>
              <span class="profile__info-title">Квартира</span>
              <span class="profile__info-content">{{ currentObject.flat }}</span>
            </li>
            <li>
              <span class="profile__info-title">Город</span>
              <span class="profile__info-content">{{ currentObject.city }}</span>
            </li>
            <li>
              <span class="profile__info-title">Индекс</span>
              <span class="profile__info-content">{{ currentObject.index }}</span>
            </li>
          </ul>
          <h3>Контактное лицо</h3>
          <ul>
            <li>
              <span class="profile__info-title">Фамилия</span>
              <span class="profile__info-content">{{ currentObject.contact_id.lastname }}</span>
            </li>
            <li>
              <span class="profile__info-title">Имя</span>
              <span class="profile__info-content">{{ currentObject.contact_id.name }}</span>
            </li>
            <li>
              <span class="profile__info-title">Телефон</span>
              <span class="profile__info-content">{{ currentObject.contact_id.work_phone }}</span>
            </li>
            <li>
              <span class="profile__info-title">E-mail</span>
              <span class="profile__info-content">{{ currentObject.contact_id.work_email }}</span>
            </li>
          </ul>
          <h3>Дополнительная информация</h3>
          <ul>
            <li>
              <span class="profile__info-title">Жилье</span>
              <span class="profile__info-content">{{ currentObject.habitation }}</span>
            </li>
            <li>
              <span class="profile__info-title">Страховка от несчастных случаев</span>
              <span class="profile__info-content">{{ currentObject.accident_insurance }}</span>
            </li>
            <li>
              <span class="profile__info-title">Страховка здоровья</span>
              <span class="profile__info-content">{{ currentObject.health_insurance }}</span>
            </li>
          </ul>
          <h3>Работники</h3>
          <v-list three-line class="workers__list content-list">
            <template v-for="worker in objectWorkers">
              <v-list-item :key="worker.id">
                <v-list-item-content @click="openWorker(worker)">
                  <v-list-item-title>{{ worker.user_profile_id.lastname }} {{ worker.user_profile_id.name }}
                    ({{ worker.user_profile_id.phone }})
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <span>{{ worker.start_date }} - {{ worker.end_date }}</span><br>
                    <span>{{ worker.comment }}</span>
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action v-if="$parent.$parent.edit.indexOf('Объекты') !== -1">
                  <v-icon color="grey lighten-1" @click="openEditWorkerForm(worker)">
                    $edit
                  </v-icon>
                  <v-icon color="grey lighten-1" @click="openConfirmDeleteWorkerDialog(worker)">
                    $waste
                  </v-icon>
                </v-list-item-action>
              </v-list-item>
            </template>
          </v-list>
          <v-list class="content-list__btns" v-if="$parent.$parent.edit.indexOf('Объекты') !== -1">
            <v-list-item class="content-list__btns-add" @click="openAddWorkerForm">
              <v-list-item-icon>
                <v-icon>mdi-plus</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Добавить работника</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <!--          <h3>Фото объекта</h3>-->
          <!--          <v-slide-group class="pa-4 objects-open__slider" v-model="photos" active-class="slide-active" show-arrows>-->
          <!--            <v-slide-item v-for="ph in photos" :key="ph.id">-->
          <!--              <v-card class="ma-4" height="250" width="300">-->
          <!--                <v-row class="fill-height" align="center" justify="center">-->
          <!--                  <v-scale-transition>-->
          <!--                    <v-img :src="require('../../../media'+ph.photo_path)"></v-img>-->
          <!--                  </v-scale-transition>-->
          <!--                </v-row>-->
          <!--              </v-card>-->
          <!--            </v-slide-item>-->
          <!--          </v-slide-group>-->
          <h3>Комментарии</h3>
          <div class="objects-open__comments">
            <div class="objects-open__comments-single" v-for="com in comments.comments" :key="com.id">
              <h4> {{ com.user_profile_id.lastname }} {{ com.user_profile_id.name }}
                ({{ com.user_profile_id.position.name }})</h4>
              <div v-html="com.text"></div>
              <div class="open__actions">
                <div class="addition-btn" @click="answer=com.text; newComment.object_comments_id=com.id">
                  Ответить
                </div>
                <div class="addition-btn" @click="deleteComment(com.id)"
                     v-if="com.user_profile_id.id === comments.profile">
                  Удалить
                </div>
              </div>
              <v-divider></v-divider>
              <div class="objects-open__comments-answers" v-for="ans in comments.data[com.id]" :key="ans.id">
                <h4> {{ ans.user_profile_id.lastname }} {{ ans.user_profile_id.name }}
                  ({{ ans.user_profile_id.position.name }})</h4>
                <div v-html="ans.text"></div>
                <div class="open__actions">
                  <div class="addition-btn" @click="deleteComment(ans.id)"
                       v-if="ans.user_profile_id.id === comments.profile">
                    Удалить
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="objects-open__comments-add">
            <editor v-model="newComment.text"
                    api-key="660vq0feuhjyub7s7o01nh9an48e4eq55ucbneldw55cr22l"
                    :init="editorInit"
            />
            <div class="objects-open__comments-add-actions">
              <div class="objects-open__comments-add-answerfor" v-if="newComment.object_comments_id != null">
                <div>Ответ на:
                  <div class="comments__answer" v-html="answer"></div>
                </div>
                <v-icon @click="newComment.object_comments_id=null" style="width: 16px">$deleteIcon</v-icon>
              </div>
              <v-btn class="action-btn" color="secondary" @click="addComment">
                Добавить
              </v-btn>
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
          <v-form ref="form">
            <v-text-field placeholder="Индекс*" v-model="newObject.index" :rules="reqRules" required
                          outlined></v-text-field>
            <v-row>
              <v-text-field placeholder="Город*" v-model="newObject.city" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Улица*" v-model="newObject.street" :rules="reqRules" required
                            outlined></v-text-field>
            </v-row>
            <v-row>
              <v-text-field placeholder="Дом*" v-model="newObject.house" :rules="reqRules"
                            required outlined></v-text-field>
              <v-text-field placeholder="Подъезд" v-model="newObject.entrance" outlined></v-text-field>
              <v-text-field placeholder="Квартира" v-model="newObject.flat" outlined></v-text-field>
            </v-row>
            <v-row>
              <v-menu ref="menu_start" v-model="datePickers.menu_start" :close-on-content-click="false"
                      :return-value.sync="newObject.date_start"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newObject.date_start" placeholder="Начало работ*" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="newObject.date_start" no-title scrollable color="primary">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="datePickers.menu_start = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu_start.save(newObject.date_start)">OK</v-btn>
                </v-date-picker>
              </v-menu>
              <v-menu ref="menu_end" v-model="datePickers.menu_end" :close-on-content-click="false"
                      :return-value.sync="newObject.date_end"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newObject.date_end" placeholder="Окончание работ" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="newObject.date_end" no-title scrollable color="primary">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="datePickers.menu_end = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu_end.save(newObject.date_end)">OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-row>
            <v-row>
              <v-select v-model="newObject.client_id" :items="clients" item-text="name" item-value="id"
                        :rules="reqRules" placeholder="Клиент*" outlined dense
                        @change="loadContacts(newObject.client_id)"></v-select>
              <v-select v-model="newObject.contact_id" :items="contacts" item-value="id" item-text="label"
                        no-data-text="Выберите клиента" placeholder="Контактное лицо*" :rules="reqRules" outlined
                        dense></v-select>
            </v-row>
            <v-text-field placeholder="Жилье" v-model="newObject.habitation" outlined></v-text-field>
            <v-row>
              <v-text-field placeholder="Страховка от несчастных случаев" v-model="newObject.accident_insurance"
                            outlined></v-text-field>
              <v-text-field placeholder="Страховка здоровья" v-model="newObject.health_insurance"
                            outlined></v-text-field>
            </v-row>
            <v-textarea placeholder="Описание работ" v-model="newObject.work_description" outlined></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="addObject">{{ formBtnText }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="addTimingForm">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="addTimingForm = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>Добавление часов</h3>
        <v-card-text>
          <v-form ref="form" :model="newTiming">
            <v-row>
              <v-menu ref="dateMenu" v-model="menus.dateMenu"
                      :close-on-content-click="false"
                      :nudge-right="40" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newTiming.date" label="Дата" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="newTiming.date" @input="menus.dateMenu = false"
                               :allowed-dates="allowedDates"></v-date-picker>
              </v-menu>
            </v-row>
            <v-autocomplete label="Объект" v-model="newTiming.objects_id" :items="objects" item-text="label"
                            item-value="id" :rules="reqRules" disabled></v-autocomplete>
            <v-combobox label="Профиль работ" v-model="newTiming.position" :items="positions"
                        :rules="reqRules"></v-combobox>
            <v-row>
              <v-menu ref="menuStartTime" v-model="menus.timeStartMenu"
                      :close-on-content-click="false" :nudge-right="40" :return-value.sync="newTiming.time_start"
                      transition="scale-transition" offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newTiming.time_start" label="Время начала" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules" required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeStartMenu" v-model="newTiming.time_start" full-width format="24hr"
                               @click:minute="$refs.menuStartTime.save(newTiming.time_start)"></v-time-picker>
              </v-menu>
              <v-menu ref="menuEndTime" v-model="menus.timeEndMenu" :close-on-content-click="false"
                      :nudge-right="40" :return-value.sync="newTiming.time_end" transition="scale-transition"
                      offset-y max-width="290px" min-width="290px">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="newTiming.time_end" label="Время окончания" readonly v-bind="attrs"
                                v-on="on" outlined required></v-text-field>
                </template>
                <v-time-picker v-if="menus.timeEndMenu" v-model="newTiming.time_end" full-width format="24hr"
                               :min="newTiming.time_start"
                               @click:minute="$refs.menuEndTime.save(newTiming.time_end)"></v-time-picker>
              </v-menu>
            </v-row>
            <v-textarea label="Описание" v-model="newTiming.comment"></v-textarea>
          </v-form>
          <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
            {{ alertMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="openConfirmAdd">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="addWorkerForm" max-width="500">
      <v-card>
        <v-toolbar flat>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeForm">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <h3>{{ formTitle }}</h3>
        <v-card-text>
          <v-form ref="workerForm">
            <v-select v-model="addWorker.user_profile_id" :items="workers" item-value="id" item-text="label"
                      no-data-text="Нет свободных работников" placeholder="Выберите работника*" :rules="reqRules"
                      outlined dense></v-select>
            <v-row>
              <v-menu ref="worker_start" v-model="datePickers.worker_start" :close-on-content-click="false"
                      :return-value.sync="addWorker.start_date"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="addWorker.start_date" placeholder="Начало работ*" readonly v-bind="attrs"
                                v-on="on" outlined :rules="reqRules"></v-text-field>
                </template>
                <v-date-picker v-model="addWorker.start_date" no-title scrollable color="primary">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="datePickers.worker_start = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.worker_start.save(addWorker.start_date)">OK</v-btn>
                </v-date-picker>
              </v-menu>
              <v-menu ref="worker_end" v-model="datePickers.worker_end" :close-on-content-click="false"
                      :return-value.sync="addWorker.end_date"
                      transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field v-model="addWorker.end_date" placeholder="Окончание работ" readonly v-bind="attrs"
                                v-on="on" outlined></v-text-field>
                </template>
                <v-date-picker v-model="addWorker.end_date" no-title scrollable color="primary">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="datePickers.worker_end = false"> Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.worker_end.save(addWorker.end_date)">OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-row>
            <v-textarea placeholder="Комментарий" v-model="addWorker.comment" outlined></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="action-btn" color="primary" @click="putObjectUser">Сохранить</v-btn>
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
    <v-dialog v-model="confirmAddDialog" max-width="500">
      <v-card>
        <v-card-title>
          Подтверждение
        </v-card-title>
        <v-card-text>Проверьте корректность всех данных. Внести изменения сможет только администратор</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmAddDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="addTiming">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление объекта
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить объект? Отменить это действие будет невозможно</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteObject">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteWorkerDialog" max-width="500">
      <v-card>
        <v-card-title>
          Удаление работника с объекта
        </v-card-title>
        <v-card-text>Вы действительно хотите удалить работника с объекта? Отменить это действие будет невозможно
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="confirmDeleteWorkerDialog = false">Отменить</v-btn>
          <v-btn color="primary" text @click="deleteObjectUser">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmArchiveDialog" max-width="500">
      <v-card>
        <v-card-title>
          Сдача объекта
        </v-card-title>
        <v-card-text>
          Вы действительно хотите сдать объект? После подтверждения объект будет перемещен в архив
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" text @click="cancelConfirmArchiveDialog">
            Отменить
          </v-btn>
          <v-btn color="primary" text @click="editObject">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import $ from 'jquery';
// import AddPhotoIcon from "../components/icons/addPhotoIcon";
import BackIcon from "../components/icons/backIcon";
import WasteIcon from "../components/icons/wasteIcon";
import EditIcon from "../components/icons/editIcon";
import Editor from '@tinymce/tinymce-vue'


export default {
  name: "Objects",
  components: {EditIcon, WasteIcon, BackIcon, 'editor': Editor, /*AddPhotoIcon*/},
  props: {
    idClient: [String, Number, null]
  },
  data() {
    return {
      page: 'objects',
      objects: [],
      objectWorkers: [],
      all: true,
      archive: false,
      newObject: {
        id: 0,
        index: '',
        city: '',
        street: '',
        house: '',
        entrance: '',
        flat: '',
        date_start: '',
        date_end: '',
        active: false,
        client_id: '',
        contact_id: '',
        work_description: null,
        habitation: null,
        accident_insurance: null,
        health_insurance: null,
      },
      currentObject: {
        id: 0,
        index: '',
        city: '',
        street: '',
        house: '',
        entrance: '',
        flat: '',
        date_start: '',
        date_end: '',
        active: false,
        client_id: '',
        contact_id: {
          email: ''
        },
        work_description: null,
        habitation: null,
        accident_insurance: null,
        health_insurance: null,
      },
      addWorker: {
        id: 0,
        user_profile_id: 0,
        object_id: 0,
        start_date: null,
        end_date: null,
        comment: null,
      },
      newComment: {
        text: "",
        object_comments_id: null,
        objects_id: null
      },
      answer: "",
      photos: "",
      comments: {
        comments: [],
        data: {}
      },
      clients: [],
      contacts: [],
      workers: [],
      positions: [],
      newTiming: {
        id: 0,
        date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        time_start: '',
        time_end: '',
        position: '',
        objects_id: '',
        user_profile_id: null,
        comment: ''
      },
      colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1', 'yellow', 'pink', 'lime'],
      filter: {
        address: "",
        client: "Все",
        dates: []
      },
      datePickers: {
        menu_filter: false,
        menu_start: false,
        menu_end: false,
        worker_start: false,
        worker_end: false,
      },
      menus: {
        dateMenu: false,
        timeStartMenu: false,
        timeEndMenu: false,
      },
      formTitle: "Добавление объекта",
      formBtnText: "Добавить объект",
      photoField: null,
      addForm: false,
      addTimingForm: false,
      addWorkerForm: false,
      photoDialog: false,
      confirmArchiveDialog: false,
      confirmAddDialog: false,
      confirmDeleteDialog: false,
      confirmDeleteWorkerDialog: false,
      reqRules: [
        v => !!v || 'Необходимо заполнить поле'
      ],
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
      editorInit: {
        height: 500,
        menubar: false,
        plugins: [
          'advlist autolink lists link image charmap print preview anchor',
          'searchreplace visualblocks code fullscreen',
          'insertdatetime media table paste code help wordcount'
        ],
        toolbar:
            'undo redo | formatselect | bold italic backcolor | \
            alignleft aligncenter alignright alignjustify | \
            bullist numlist outdent indent | image | removeformat | help',
        file_picker_types: 'image',
        relative_urls: false,
        image_prepend_url: this.$hostname,
        images_upload_base_path: this.$hostname,
        image_description: false,
        // image_dimensions: false,
        file_picker_callback: function (callback, value, meta) {
          $(".tox-lock.tox-button").click()
          console.log(callback)
          console.log(value)
          console.log(meta)
          var input = document.createElement('input');
          input.setAttribute('type', 'file');
          input.setAttribute('accept', 'image/*');
          input.onchange = function () {
            var file = this.files[0];
            console.log(file)
            var reader = new FileReader();
            reader.onload = function () {
              const axios = require('axios')
              // чтение файла в formData
              let fd = new FormData();
              if (file !== null) {
                fd.append('file', file)
              }
              axios({
                method: 'post',
                // url: "http://127.0.0.1:8000/time-tracking/images/upload",
                url: "https://shielded-plateau-96200.herokuapp.com/time-tracking/images/upload",
                headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
                data: fd
              })
                  .then(response => {
                    console.log(response.data.data)
                    $('.tox-control-wrap .tox-textfield').val(response.data.data)
                  });
              /*
                Note: Now we need to register the blob in TinyMCEs image blob
                registry. In the next release this part hopefully won't be
                necessary, as we are looking to handle it internally.
              */
              // var id = 'blobid' + (new Date()).getTime();
              // var blobCache = tinymce.activeEditor.editorUpload.blobCache;
              // var base64 = reader.result.split(',')[1];
              // var blobInfo = blobCache.create(id, file, base64);
              // blobCache.add(blobInfo);
              //
              // /* call the callback and populate the Title field with the file name */
              // cb(blobInfo.blobUri(), {title: file.name});
            };
            reader.readAsDataURL(file);
          };

          input.click();
        }
      },
    }
  },
  created() {
    console.log("init Objects")
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      if (this.$parent.$parent.read.indexOf('Объекты') === -1)
        this.$router.push({name: "Index"})
      this.$emit('set-auth')
      this.$emit('load-functions')
      $.ajaxSetup({
        headers: {"Authorization": "Token " + (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token'))}
      })
      this.loadData()
      this.loadClients()
    } else {
      this.$emit('set-not-auth')
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    allowedDates: val => val <= new Date().toISOString(),
    // initSocket() {
    // socket.onmessage = function (e) {
    //   const data = JSON.parse(e.data);
    //   console.log(data.message);
    // };
    //
    // socket.onclose = function () {
    //   console.error('Chat socket closed unexpectedly');
    // };
    // },
    loadData() {
      let url = ""
      if (this.idClient !== null && this.idClient !== undefined) {
        url = "time-tracking/objects/" + this.idClient
        this.filter.client = Number(this.idClient)
      } else
        url = "time-tracking/objects"
      $.ajax({
        url: this.$hostname + url,
        type: "GET",
        success: (response) => {
          this.objects = response.data.data
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
    loadContacts(client_id) {
      this.newObject.contact_id = null
      this.contacts = []
      $.ajax({
        url: this.$hostname + "time-tracking/clients/employees/" + client_id,
        type: "GET",
        success: (response) => {
          this.contacts = response.data.data
          this.contacts.forEach(contact => {
            contact.label = contact.lastname + ' ' + contact.name + ', ' + contact.position.name
            console.log(contact.label)
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
    },
    loadPositions() {
      $.ajax({
        url: this.$hostname + "time-tracking/time-reports-positions",
        type: "GET",
        success: (response) => {
          this.positions = response.data.positions
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
        }
      })
    },
    addObject() {
      if (this.$refs.form.validate()) {
        if (this.newObject.id === 0)
          $.ajax({
            url: this.$hostname + "time-tracking/objects",
            type: "POST",
            data: {
              index: this.newObject.index,
              city: this.newObject.city,
              street: this.newObject.street,
              house: this.newObject.house,
              entrance: this.newObject.entrance,
              flat: this.newObject.flat,
              date_start: this.newObject.date_start,
              date_end: this.newObject.date_end,
              active: this.newObject.active,
              client_id: this.newObject.client_id,
              contact_id: this.newObject.contact_id,
              work_description: this.newObject.work_description,
              habitation: this.newObject.habitation,
              accident_insurance: this.newObject.accident_insurance,
              health_insurance: this.newObject.health_insurance,
            },
            success: () => {
              console.log("Объект добавлен ")
              this.loadData()
              this.closeForm()
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
        else
          this.editObject()
      }
    },
    editObject() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "PUT",
        data: this.currentObject,
        // data: this.newObject,
        success: () => {
          console.log("Объект изменен ")
          if (this.addForm) {
            this.loadData()
            this.closeForm()
          } else {
            this.confirmArchiveDialog = false
          }
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
    deleteObject() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects",
        type: "DELETE",
        data: {
          id: this.currentObject.id
        },
        success: () => {
          console.log("Объект удален")
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
    openObject(item) {
      this.currentObject = item
      this.currentObject.label = this.currentObject.city + ' ' + this.currentObject.street + ' ' + this.currentObject.house
      // this.loadPhoto(item.id)
      this.all = false
      this.loadWorkers()
      this.loadComments(false)
      // setInterval(() => {
      //   this.loadComments(true)
      // }, 25000)
    },
    // loadPhoto(id) {
    //   $.ajax({
    //     url: this.$hostname + "time-tracking/objects/photos/" + id,
    //     type: "GET",
    //     success: (response) => {
    //       this.photos = response.data.data
    //     },
    //     error: (response) => {
    //       if (response.status === 500) {
    //         this.alertMsg = "Ошибка соединения с сервером"
    //       } else if (response.status === 401) {
    //         this.$refresh()
    //       } else {
    //         this.alertMsg = "Непредвиденная ошибка"
    //       }
    //       this.alertError = true
    //     },
    //   })
    // },
    loadWorkers() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees/" + this.currentObject.id,
        type: "GET",
        success: (response) => {
          this.objectWorkers = response.data.data
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
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees",
        type: "GET",
        success: (response) => {
          this.workers = response.data.data
          this.workers.forEach(worker => {
            worker.label = worker.lastname + ' ' + worker.name + ', ' + worker.position
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
    },
    loadComments(check) {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/comments/" + this.currentObject.id,
        type: "GET",
        success: (response) => {
          // console.log(this.comments)
          // console.log(response.data)
          // console.log(this.comments.comments.length < response.data.comments.length)
          if (!check)
            this.comments = response.data
          // else if (this.comments !== undefined && check) {
          //   let k = false
          //   if (this.comments.comments.length < response.data.comments.length
          //       || this.comments.data.length < response.data.data.length)
          //     k = true
          //   else
          //     for (let i = 0; i !== this.comments.data.length; i++) {
          //       if (this.comments.data[i].length < this.response.data.data[i].length)
          //         k = true
          //     }
          //   if (k) {
          //     this.comments = response.data
          //     alert("Новый комментарий!")
          //   }
          // }
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
    putObjectUser() {
      if (this.$refs.workerForm.validate()) {
        this.addWorker.object_id = this.currentObject.id
        $.ajax({
          url: this.$hostname + "time-tracking/objects/employees",
          type: "PUT",
          data: {
            id: this.addWorker.id,
            user_profile_id: this.addWorker.user_profile_id,
            objects_id: this.addWorker.object_id,
            start_date: this.addWorker.start_date,
            end_date: this.addWorker.end_date,
            comment: this.addWorker.comment,
          },
          success: (response) => {
            console.log(response)
            this.loadWorkers()
            this.addWorkerForm = false
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
    },
    deleteObjectUser() {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/employees",
        type: "DELETE",
        data: {
          id: this.addWorker.id,
        },
        success: (response) => {
          console.log(response)
          this.loadWorkers()
          this.confirmDeleteWorkerDialog = false
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
    openWorker(worker) {
      console.log(worker)
    },
    addComment() {
      this.newComment.objects_id = this.currentObject.id
      $.ajax({
        url: this.$hostname + "time-tracking/objects/comments",
        type: "POST",
        data: this.newComment,
        success: () => {
          // console.log(socket.readyState)
          // console.log(socket.OPEN)
          // socket.onopen = () =>
          //     socket.send(JSON.stringify({
          //   'message': this.newComment.text
          // }));
          // console.log(socket.readyState)
          this.loadComments(false)
          this.newComment = {
            text: "",
            object_comments_id: null,
            objects_id: null
          }
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
    deleteComment(id) {
      $.ajax({
        url: this.$hostname + "time-tracking/objects/comments/" + id,
        type: "DELETE",
        data: this.newComment,
        success: () => {
          this.loadComments(false)
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
    addTiming() {
      $.ajax({
        url: this.$hostname + "time-tracking/time-reports",
        type: "POST",
        data: this.newTiming,
        success: () => {
          this.loadData()
          this.loadPositions()
          this.addTimingForm = false
          this.confirmAddDialog = false
          this.newTiming = {
            date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
            time_start: '',
            time_end: '',
            position: '',
            objects_id: '',
            user_profile_id: '',
            comment: ''
          }
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
    savePhoto() {
      const axios = require('axios')
      // чтение файла в formData
      let fd = new FormData();
      let avatar = this.photoField;
      if (avatar !== undefined) {
        fd.append('image', avatar)
      } else {
        console.log("ERROR")
        return
      }
      axios({
        method: 'put',
        url: this.$hostname + "time-tracking/objects/" + this.currentObject.id,
        headers: {"Authorization": "Token " + (sessionStorage.getItem("auth_token") || localStorage.getItem("auth_token"))},
        data: fd
      })
          .then(response => {
            console.log(response.data.data)
            this.photoDialog = false
            this.photoField = null
            this.currentObject.photo_path = response.data.data.name
            this.loadData()
          });
    },
    openAddForm() {
      this.formTitle = "Добавление объекта"
      this.formBtnText = "Добавить объект"
      this.addForm = true
    },
    openEditForm(item) {
      this.formTitle = "Редактирование объекта"
      this.formBtnText = "Сохранить объект"
      this.newObject = item
      this.addForm = true
    },
    openAddWorkerForm() {
      this.formTitle = "Добавление работника на объект"
      this.addWorkerForm = true
    },
    openEditWorkerForm(worker) {
      this.addWorker = worker
      this.formTitle = "Редактирование работника на объекте"
      this.addWorkerForm = true
    },
    openConfirmAdd() {
      if (this.$refs.form.validate()) {
        this.confirmAddDialog = true
      } else {
        this.alertMsg = "Заполните все необходимые поля"
        this.alertError = true
      }
    },
    openConfirmArchiveDialog() {
      if ((this.currentObject.active && !this.all) || (!this.currentObject.active && this.all)) {
        this.currentObject.active = true
        this.confirmArchiveDialog = true
      } else {
        this.editObject()
      }
    },
    cancelConfirmArchiveDialog() {
      this.currentObject.active = false
      this.confirmArchiveDialog = false
    },
    openConfirmDeleteDialog(item) {
      this.currentObject = item
      if (this.archive || !this.all) {
        this.confirmDeleteDialog = true
      } else
        this.openConfirmArchiveDialog()
    },
    openConfirmDeleteWorkerDialog(item) {
      this.addWorker = item
      this.confirmDeleteWorkerDialog = true
    },
    closeForm() {
      this.addForm = false
      this.newObject = {
        id: 0,
        index: '',
        city: '',
        street: '',
        house: '',
        entrance: '',
        flat: '',
        date_start: '',
        date_end: '',
        active: false,
        client_id: '',
        contact_id: '',
        work_description: null,
        habitation: null,
        accident_insurance: null,
        health_insurance: null,
      }
      this.addWorker = {
        id: 0,
        user_profile_id: 0,
        object_id: 0,
        start_date: null,
        end_date: null,
        comment: null,
      }
      this.addWorkerForm = false
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
.profile__image {
  max-width: 200px;
}
</style>