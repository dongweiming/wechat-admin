<template>
<div class="nav">
  <div v-for="item in items">
	  <div class="item">
      <h2>{{ item.title }}</h2>
      <ul>
        <li v-for="sub_item in item.sub_items">
          <router-link :to="{ path: sub_item.path }">{{ sub_item.name }}</router-link>
        </li>
      </ul>
    </div>
    </div>
  </div>
</template>

<script>
	export default {
    data() {
        return {
          items: []
        }
    },
    mounted() {
      this.$router.options.routes.forEach(route => {
        if (!route.hidden && !route.leaf) {
          let sub_items = [];
          route.children.forEach(sub_route => {
            sub_items.push({
              name: sub_route.name,
              path: sub_route.path
            });
          });
          this.items.push({
            title: route.name,
            sub_items: sub_items
          });
        }
      })
    }
	}

</script>

<style lang="scss" scoped>
* {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}
h2 {
    width: 140px;
    padding: 11px 15px;
    margin: 0;
    font-size: 18px;
    font-weight: normal;
    color: #fff;
    background-color: #20a0ff;
}
.nav {
  background-color: #f6f6f6;
  padding: 20px;
}
.item {
    overflow: hidden;
    margin: 20px 0 30px;
    ul {
      margin-right: -1%;
      padding: 0;
    }
    li {
    float: left;
    width: 19%;
    margin-right: 1%;
    margin-top: 1%;
    padding: 15px;
    font-size: 12px;
    height: 89px;
    overflow: hidden;
    background-color: #fff;
    border-bottom: 15px solid #fff;
    a {
      margin-bottom: 5px;
      display: inline-block;
      font-size: 14px;
      font-weight: bold;
      color: #45B6F7;
      border-bottom: 2px solid transparent;
      text-decoration: inherit;
      cursor: pointer;
      &:hover, &:active {
        color: #FD8C84;
        border-bottom-color: #FD8C84;
      }
    }
  }
}
</style>