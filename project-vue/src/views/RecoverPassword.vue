<template>
  <div class="login">
    <div class="logo">logo</div>
    <v-form ref="form" :model="authForm" class="mu-demo-form">
      <h1>Восстановление пароля</h1>
      <v-text-field placeholder="Логин" v-model="authForm.login" :rules="usernameRules" required
                    append-icon="$login" outlined></v-text-field>
      <v-btn color="primary" @click="sendMessage">Восстановить пароль</v-btn>
    </v-form>
    <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
      {{ alertMsg }}
    </v-alert>

    <v-alert v-model="alertSuccess" close-text="Закрыть" color="success" dismissible>
      {{ alertMsg }}
    </v-alert>
  </div>
</template>

<script>
export default {
  name: "RecoverPassword",
  data() {
    return {
      authForm: {
        login: ''
      },
      usernameRules: [
        v => !!v || 'Необходимо заполнить имя пользователя'
      ],
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
    }
  },
}
</script>

<style scoped>

</style>