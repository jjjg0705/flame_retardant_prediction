<template>
  <div id="app">
    <nav>
      <div class="logo">
        <img alt="logo" src="./assets/logodaizi2.png" style="width: 120px; height: auto;">
      </div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/about">关于</router-link>
        <router-link to="/predict">预测</router-link>
      </div>
    </nav>
    <router-view/>
  </div>
</template>



<style>
#app {
  text-align: center;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  background: url("./assets/图片1.png") no-repeat center;
  background-size: cover;
}

.nav-links {
  flex-grow: 1;
  text-align: right;
}

nav a {
  font-weight: bold;
  color: #ffffff;
  margin-right: 100px;
}

nav a.router-link-exact-active {
  color: #000000;
}

.logo {
  flex-grow: 1;
  max-width: 20%;
}

.logo img {
  width: 100%;
  height: auto;
}

</style>
