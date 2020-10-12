const app = new Vue({
  el: "#app",
  delimiters: ["$[", "]"],
  data: {
    showNav: window.innerWidth >= 768,
    searchKey: "",
  },
});
