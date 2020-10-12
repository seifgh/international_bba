"use strict";

var app = new Vue({
  el: "#app",
  delimiters: ["$[", "]"],
  data: {
    showNav: window.innerWidth >= 768,
    selectedId: 1
  }
});