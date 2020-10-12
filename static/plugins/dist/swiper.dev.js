"use strict";

function scrollLeft() {
  var scroller = this.$refs.scroller;

  if (scroller.scrollLeft === 0) {
    scroller.scrollTo({
      left: scroller.scrollWidth,
      behavior: "smooth"
    });
  } else {
    scroller.scrollTo({
      left: scroller.scrollLeft - scroller.clientWidth,
      behavior: "smooth"
    });
  }
}

function scrollRight() {
  var scroller = this.$refs.scroller;

  if (scroller.scrollLeft >= scroller.scrollWidth - scroller.clientWidth) {
    scroller.scrollTo({
      left: 0,
      behavior: "smooth"
    });
  } else {
    scroller.scrollTo({
      left: scroller.scrollLeft + scroller.clientWidth,
      behavior: "smooth"
    });
  }
}

Vue.component("swiper", {
  props: {
    title: String
  },
  methods: {
    scrollLeft: scrollLeft,
    scrollRight: scrollRight
  },
  template: "\n  <div class=\"relative block\" >\n    <div class=\"flex justify-between items-center mb-5\">\n      <h3 class=\"font-bold text-3xl w-auto\">{{title}}</h3>\n      <div  class=\"flex mr-1\">\n        <button\n          title=\"Scroll to left\"\n          @click=\"scrollLeft\"\n          class=\"flex items-center justify-center w-12 h-12 mr-4 focus:outline-none rounded-md bg-pri-light text-pri shadow-sm hover:shadow-md\"\n        >\n        <svg class=\"h-5\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 20 20\" fill=\"currentColor\">\n            <path fill-rule=\"evenodd\" d=\"M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z\" clip-rule=\"evenodd\" />\n        </svg>\n        </button>\n        <button\n          title=\"Scroll to right\"\n          @click=\"scrollRight\"\n          class=\"flex items-center justify-center w-12 h-12 focus:outline-none rounded-md bg-pri-light text-pri shadow-sm hover:shadow-md\"\n        >\n        <svg class=\"h-5\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 20 20\" fill=\"currentColor\">\n            <path fill-rule=\"evenodd\" d=\"M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z\" clip-rule=\"evenodd\" />\n        </svg>\n        </button>\n      </div>\n    </div>\n\n    <div ref=\"scroller\" class=\"overflow-hidden flex flex-no-wrap scrolling-touch py-4\">\n      <slot />\n    </div>\n  </div>"
});