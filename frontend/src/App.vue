<template>
 <v-app id="inspire" style="background: #fff">
    <v-toolbar color="blue" dark fixed app>
      <v-toolbar-title><router-link to="/" class="router-link">pathoLogic</router-link></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn
            :href="$store.state.logout_url"
            icon
        >
            <v-icon>exit_to_app</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <router-view></router-view>
      </v-container>
    </v-content>
    <v-btn
      fab
      bottom
      right
      color="pink"
      dark
      fixed
      to="createSamples"
      v-if="$route.name === 'samples'"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-app>
</template>

<style scoped>
.router-link {
    text-decoration: none;
    color: #fff;
}
</style>
