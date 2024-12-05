<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
     <main class="container" id="main_container">
        <nav>
            <div class="logo">
            <!--                     <img src="static/logo/gistechnic_logo.png" id="gistechnic_logo">-->
                <h4>GEO-TECHNICS</h4>
            </div>
            <ul class="nav-links" id="navigation">
                <li><a href="/">HOME</a></li>
                <li><a href="/pygis">PYTHON</a></li>
                <li><a href="/maps">CARTOGRAPHY</a></li>
                <li><a href="/parks3d">ADVENTURE-3D</a></li>
            </ul>
            <div class = "boerie">
                <div class = 'line1'></div>
                <div class = 'line2'></div>
                <div class = 'line3'></div>
            </div>
        </nav>
        <div class="row">
            <div class="col">
            {% block content %}
            {% endblock %}
            </div>
        </div>
    </main>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
