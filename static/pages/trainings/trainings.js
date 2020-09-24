
// $('body').ready(function () {
// $("#formations_search_input").click(function () {
//   $(this).parent().toggleClass("focused");
// })
// $("#formations_search_input").blur(function () {
//   $(this).parent().toggleClass("focused")
// })
// $(".form-container #toggler").click(function () {
//   $(this).parent().children(".form-filter").toggleClass("show");
// })

window.addEventListener("DOMContentLoaded", function () {

  document.getElementById("flf-toggler").addEventListener('blur', function () {
    this.parentElement.querySelector("form").classList.toggle("show");
  })


  // scroller-swiper-1
  let left = 0;
  const scroller = $("#scroller");
  scroller.css("transform", 'translateX(0px)');
  const parentScroller = $("#parent-scroller"),
    leftScroller = $("#scroll-left");
  $("#scroll-left").click(function () {
    left = scroller[0].style.transform.replace("translateX(", "").replace("px)", "");
    left = Number(left) + parentScroller[0].clientWidth;

    left = left >= 0 ? 0 : left;

    scroller.css("transform", `translateX(${left}px)`);
  })
  $("#scroll-right").click(function () {
    left = scroller[0].style.transform.replace("translateX(", "").replace("px)", "");
    left = Number(left) - parentScroller[0].clientWidth;
    if (-left > (scroller[0].clientWidth - parentScroller[0].clientWidth))
      left = ((scroller[0].clientWidth - parentScroller[0].clientWidth) * -1)

    scroller.css("transform", `translateX(${left}px)`);

  })
})
