<template>
  <FormCard ref="loginForm" :schema="loginSchema" :data="ctx" :logo="osLogo" @keydown.enter.prevent="login">
    <template #title v-if="showHeader">
      <h3 class="header">Welcome to LIIMS<br><span style="font-size: 18px; font-weight: 400;">(Longevity India Information Management System)</span></h3>
    </template>

    <template #primary-action>
      <os-button primary label="Sign In" @click="login" />
    </template>
  
    <template #secondary-actions v-if="ctx.forgotPasswordEnabled || ctx.otpAuthEnabled">
      <os-button text label="Forgot Password?" @click="gotoForgotPassword" v-if="ctx.forgotPasswordEnabled" />

      <os-button text label="Reset OTP Secret Code?" @click="gotoResetOtpSecret" v-if="ctx.otpAuthEnabled" />
    </template>
  </FormCard>
</template>

<script>
import loginSvc    from '@/common/services/Login.js';
import loginSchema from '@/users/schemas/login.js';
import osLogo      from '@/assets/images/os_dna_logo.png';
import routerSvc   from '@/common/services/Router.js';

import FormCard    from './FormCard.vue';

export default {
  props: ['show-header'],

  inject: ['ui'],

  components: {
    FormCard
  },

  data() {
    const {global: {appProps}} = this.ui;
    return {
      osLogo,

      loginSchema: loginSchema.layout,

      ctx: {
        loginDetail: {
          domainName: 'openspecimen'
        },

        otpAuthEnabled: false,

        forgotPasswordEnabled: appProps.forgot_password,

        samlDomainSelected: false
      }
    };
  },

  mounted() {
    if (this.$osSvc.userOtpSvc) {
      this.$osSvc.userOtpSvc.isFeatureEnabled().then(status => this.ctx.otpAuthEnabled = status);
    }
  },

  computed: {
  },

  watch: {
  },

  methods: {
    login: function() {
      if (!this.$refs.loginForm.validate()) {
        return;
      }

      const {loginDetail} = this.ctx;
      loginSvc.login(loginDetail).then(
        (resp) => {
          if (resp.resetPasswordToken && !resp.token) {
            routerSvc.goto('UserResetPassword', {}, {resetToken: resp.resetPasswordToken});
          } else {
            routerSvc.goto('HomePage');
          }
        }
      );
    },

    gotoForgotPassword: function() {
      routerSvc.goto('UserForgotPassword');
    },

    gotoResetOtpSecret: function() {
      routerSvc.goto('UserResetOtpSecretCode');
    }
  }
}
</script>
