<template>
  <div class="login">
    <div class="logo">logo</div>
    <v-form ref="form" :model="authForm" class="mu-demo-form">
      <h1>Авторизация</h1>
      <v-text-field placeholder="Логин" v-model="authForm.login" :rules="usernameRules" required
                    append-icon="$login" outlined></v-text-field>
      <v-text-field placeholder="Пароль" type="password" v-model="authForm.password" :rules="passwordRules"
                    required append-icon="$password" outlined></v-text-field>
      <v-checkbox v-model="checkbox" :label="`Запомнить меня`"></v-checkbox>
      <v-btn color="primary" @click="setLogin">Войти</v-btn>
    </v-form>
<!--    <button class="login__recover-btn" @click="goRecover">Забыли пароль?</button>-->
    <v-alert v-model="alertError" close-text="Закрыть" color="error" dismissible>
      {{ alertMsg }}
    </v-alert>
    <v-alert v-model="alertSuccess" close-text="Закрыть" color="success" dismissible>
      {{ alertMsg }}
    </v-alert>
  </div>
</template>

<script>
import $ from 'jquery'

export default {
  name: "Login",
  data() {
    return {
      authForm: {
        login: '',
        password: ''
      },
      checkbox: false,
      usernameRules: [
        v => !!v || 'Необходимо заполнить почту пользователя',
        v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'Некорректный E-mail',
      ],
      passwordRules: [
        v => !!v || 'Необходимо заполнить пароль',
      ],
      alertError: false,
      alertSuccess: false,
      alertMsg: '',
    }
  },
  created() {
    if (localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')) {
      this.$router.push({name: "Index"})
    }
  },
  methods: {
    setLogin() {
      if (this.$refs.form.validate()) {
        var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        $.ajax({
          url: this.$hostname + "auth/token/login",
          type: "POST",
          headers: {
            "X-CSRFToken": $crf_token
          },
          // contentType: "application/json; charset=utf-8",
          data: {
            email: this.authForm.login,
            password: this.authForm.password,
          },
          success: (response) => {
            if (this.checkbox)
              localStorage.setItem("auth_token", response.data.attributes.auth_token)
            else
              sessionStorage.setItem("auth_token", response.data.attributes.auth_token)
            this.$emit('set-auth')
            this.$emit('load-functions')
            this.$router.push({name: "Index"})
          },
          error: (response) => {
            console.log(response)
            this.alertError = true
            this.alertMsg = "Непредвиденная ошибка"
            switch (response.status) {
              case 400:
                this.alertMsg = "Пользователя с такой почтой не существует"
                break
              case 403:
                this.alertMsg = "Неверный пароль"
                break
              case 404:
                this.alertMsg = "Страница не найдена"
                break
            }
          }
        })
      }
    },
    goRecover() {
      this.$router.push({name: "RecoverPassword"})
    }
  }
}
</script>

<style scoped>

</style>