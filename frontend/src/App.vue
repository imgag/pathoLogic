<template>
 <v-app id="inspire" style="background: #fff">
    <v-toolbar color="blue" dark fixed app>
      <v-toolbar-title>pathoLogic</v-toolbar-title>
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
      v-if="$route.name != 'createSamples'"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-app>
</template>
