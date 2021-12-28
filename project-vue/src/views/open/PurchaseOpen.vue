<template>
  <div class="purchases flex-content">
    <Header/>
    <section class="summary-box">
      <h1>Покупки</h1>
      <v-btn class="action-btn" color="primary" @click="addForm = true">Добавить</v-btn>
      <div class="purchases__content">

      </div>
    </section>
<!--    <v-dialog v-model="addForm">-->
<!--      <v-card>-->
<!--        <v-toolbar flat>-->
<!--          <v-spacer></v-spacer>-->
<!--          <v-btn icon @click="addForm = false">-->
<!--            <v-icon>mdi-close</v-icon>-->
<!--          </v-btn>-->
<!--        </v-toolbar>-->
<!--        <h3>Добавление</h3>-->
<!--        <v-card-text>-->
<!--          <v-form ref="form" :model="newPurchase">-->
<!--            <v-autocomplete v-if="$parent.$parent.admin" v-model="newPurchase.user_profile"-->
<!--                            label="Ответственный" :items="users" item-text="label" item-value="id"></v-autocomplete>-->
<!--            <v-menu v-model="menus.dateReceiptMenu" :close-on-content-click="false" :nudge-right="40"-->
<!--                    transition="scale-transition" offset-y min-width="auto">-->
<!--              <template v-slot:activator="{ on, attrs }">-->
<!--                <v-text-field v-model="newPurchase.date_receipt" label="Дата покупки" readonly v-bind="attrs"-->
<!--                              v-on="on" outlined></v-text-field>-->
<!--              </template>-->
<!--              <v-date-picker v-model="newPurchase.date_receipt" @input="menus.dateReceiptMenu = false"></v-date-picker>-->
<!--            </v-menu>-->
<!--            <v-menu v-model="menus.dateMenu" :close-on-content-click="false" :nudge-right="40"-->
<!--                    transition="scale-transition" offset-y min-width="auto">-->
<!--              <template v-slot:activator="{ on, attrs }">-->
<!--                <v-text-field v-model="newPurchase.date" label="Дата покупки" readonly v-bind="attrs"-->
<!--                              v-on="on" outlined></v-text-field>-->
<!--              </template>-->
<!--              <v-date-picker v-model="newPurchase.date" @input="menus.dateMenu = false"></v-date-picker>-->
<!--            </v-menu>-->
<!--            <v-autocomplete v-model="newPurchase.category" :items="categories" item-text="name" item-value="id"-->
<!--                            label="Категория" :rules="reqRules" required outlined>-->
<!--              <template v-slot:no-data>-->
<!--                <v-list-item>-->
<!--                  <v-list-item-title>-->
<!--                    Категория не найдена-->
<!--                  </v-list-item-title>-->
<!--                </v-list-item>-->
<!--              </template>-->
<!--            </v-autocomplete>-->
<!--            <v-autocomplete v-model="newPurchase.tax" :items="taxes" item-text="tax" item-value="id"-->
<!--                            label="Налог" :rules="reqRules" required outlined>-->
<!--              <template v-slot:no-data>-->
<!--                <v-list-item>-->
<!--                  <v-list-item-title>-->
<!--                    Налог не найден-->
<!--                  </v-list-item-title>-->
<!--                </v-list-item>-->
<!--              </template>-->
<!--            </v-autocomplete>-->
<!--          </v-form>-->
<!--        </v-card-text>-->
<!--        <v-card-actions>-->
<!--          <v-spacer></v-spacer>-->
<!--          <v-btn class="action-btn" color="primary" @click="addWaybill">Сохранить</v-btn>-->
<!--        </v-card-actions>-->
<!--      </v-card>-->
<!--    </v-dialog>-->
<!--    <v-dialog v-model="confirmDeleteDialog" max-width="500">-->
<!--      <v-card>-->
<!--        <v-card-title>-->
<!--          Удаление чеков-->
<!--        </v-card-title>-->
<!--        <v-card-text>Вы действительно хотите удалить выбранные чеки? Отменить это действие будет невозможно-->
<!--        </v-card-text>-->
<!--        <v-card-actions>-->
<!--          <v-spacer></v-spacer>-->
<!--          <v-btn color="secondary" text @click="confirmDeleteDialog = false">Отменить</v-btn>-->
<!--          <v-btn color="primary" text @click="deletePurchase">Подтвердить</v-btn>-->
<!--        </v-card-actions>-->
<!--      </v-card>-->
<!--    </v-dialog>-->
  </div>
</template>

<script>
export default {
  name: "PurchaseOpen"
}
</script>

<style scoped>

</style>