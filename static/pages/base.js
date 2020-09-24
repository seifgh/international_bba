// handle form errors
const formErrors = {
  error: "Quelque chose a mal tourné.",
  required: "Ce champ est obligatoire.",
  catalog: "Merci, vérifiez votre email, nous vous avons envoyé le catalogue.",
  email: "Adresse email invalide.",
  phone: "Numéro de téléphone invalide.",
  email_exist: "Ce courriel existe déjà.",
  registration_success: "Merci pour votre inscription",
  type_error: "Type invalide.",
  rate_limit:
    "Vous avez dépassé le nombre maximal de demandes, veuillez essayer demain.",
  thanks_contact: "Merci, nous vous contacterons dès que possible.",
  emailVerify: function (email = null) {
    if (email)
      return `Merci, Nous vous contacterons dès que possible.<br>Veuillez vérifier votre email (${email}) pour confirmer vos données.`;
    return "";
  },
  fileSizeError: function (max_size = null) {
    if (max_size)
      return `Veuillez conserver la taille de fichier inférieure à ${max_size}.`;
    return "";
  },
  lengthError: function (min_length = null, max_length = null) {
    if (min_length)
      return `Le champ doit contenir au moins ${min_length} lettres.`;
    else if (max_length)
      return `Le champ doit contenir au maximum ${max_length} caractères.`;
    return "";
  },
};

window.mobileCheck = function () {
  var check = false;
  (function (a) {
    if (
      /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(
        a
      ) ||
      /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(
        a.substr(0, 4)
      )
    )
      check = true;
  })(navigator.userAgent || navigator.vendor || window.opera);
  return check;
};

function cleanWords(words) {
  return words.strim().replace("  ", " ");
}
function validateEmail(email) {
  var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function replaceAll(words, replaced, replaced_by) {
  let p = words.indexOf(replaced);
  while (p !== -1) {
    words = words.replace(replaced, replaced_by);
    p = words.indexOf(replaced);
  }
  return words;
}

function notify(htmlMessage, success = null, fail = null) {
  const notfDom = document.querySelector("#notf");
  notfDom.classList.remove("success", "fail");

  notfDom.innerHTML = htmlMessage;

  if (fail) notfDom.classList.add("fail", "show");
  else if (success) notfDom.classList.add("success", "show");
  setTimeout(function () {
    notfDom.classList.remove("show");
  }, 6000);
}

function emptyForm(form, startsFrom) {
  for (var i = startsFrom; i < form.elements.length; i++) {
    form.elements[i].value = "";
  }
}

window.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector("header"),
    header_menu = header.querySelector("#menu"),
    links = header.querySelector("#links"),
    header_close = header.querySelector("#close"),
    search_show = header.querySelector("#search-show"),
    search_hide = header.querySelector("#search-hide"),
    subscribe_form = document.querySelector("#subscribe-form");

  // toggle header menu ( responsive )
  header_menu.addEventListener(
    "click",
    () => {
      links.classList.add("show");
    },
    false
  );
  header_close.addEventListener(
    "click",
    () => {
      links.classList.remove("show");
    },
    false
  );

  // toggle search bar
  search_show.addEventListener(
    "click",
    () => {
      header.classList.add("show-search");
    },
    false
  );
  search_hide.addEventListener(
    "click",
    () => {
      header.classList.remove("show-search");
    },
    false
  );

  subscribe_form.addEventListener(
    "submit",
    (e) => {
      e.preventDefault();
      handleSubscribeForm();
    },
    false
  );

  function handleSubscribeForm() {
    // clean all fields
    let elements = subscribe_form.elements, message, check = true;
    const email = cleanWords(elements[0].value);
    // check email
    message = "";
    if (email) {
      if (!validateEmail(email)) {
        check = false;
        message = formErrors.email;
      }
    } else {
      check = false;
      message = formErrors.required;
    }
    if (message) notify(message, false, true);
    // subscribe_form.querySelector("#email_error").textContent = message;

    if (check && grecaptcha) {
      const button = subscribe_form.querySelector("button");

      button.textContent = "Chargement ...";

      //google captcha check
      grecaptcha
        .execute(reCAPTCHA_site_key)
        .then(function (token) {
          const data = new FormData(subscribe_form);
          data.append("token_key", token); // for captcha checking

          // post data
          axios({
            method: "post",
            url: "/subscribe",
            data: data,
            headers: { "Content-Type": "multipart/form-data" },
          })
            .then(function (res) {
              notify(formErrors.registration_success, true, false);
              button.textContent = "Envoyer";
            })
            .catch(function (err) {
              button.textContent = "Envoyer";
              // console.log(response);

              message = "";
              if (err.response.data) {
                const errors = err.response.data;
                if (errors["email"]) message = formErrors.email_exist;
              }
              if (!message) message = formErrors.error;
              notify(message, false, true);
            });
        })
        .catch(function (err) {
          notify(formErrors.error, false, true);
        });
    }
  }

  // swipers
  const swipers = document.querySelectorAll("[swiper]");

  swipers.forEach((swiper) => {
    const el = swiper.querySelector("[scroll]"),
      leftBtn = swiper.querySelector("[left]"),
      rightBtn = swiper.querySelector("[right]");

    if (el.scrollWidth === el.clientWidth) {
      leftBtn.style.display = "none";
      rightBtn.style.display = "none";
    }

    // handle left click
    rightBtn.onclick = () => {
      rightBtn.disabled = true;
      el.scrollTo({ left: el.scrollLeft + el.clientWidth, behavior: "smooth" });
      setTimeout(() => (rightBtn.disabled = false), 500);
    };
    // handle right click
    leftBtn.onclick = () => {
      leftBtn.disabled = true;
      el.scrollTo({ left: el.scrollLeft - el.clientWidth, behavior: "smooth" });
      setTimeout(() => (leftBtn.disabled = false), 500);
    };

    // handle touch swiping
    if ("mouse-scroll" in el.attributes && !"scroll-by-one" in el.attributes) {
      el.onmousedown = (e) => {
        el.querySelectorAll("*").forEach((el) => { });
        let prevX = e.clientX;
        el.onmousemove = (e) => {
          const currentX = e.clientX;
          const scrollTo = el.scrollLeft - (currentX - prevX) * 1.5; //1.5 for fasting swiping
          el.scrollTo(scrollTo, 0);
          prevX = currentX;
        };
        document.onmouseup = (e) => {
          e.preventDefault();
          el.onmousemove = null;
        };
      };
    }

    if ("mouse-scroll" in el.attributes && "scroll-by-one" in el.attributes) {
      el.onmousedown = (e) => {
        el.querySelectorAll("*").forEach((el) => { });
        let prevX = e.clientX;
        let leftOrRight = 1; // 1 is right, 0 is left
        const scrollNext = el.scrollLeft; // when mouse up scroll to it
        el.onmousemove = (e) => {
          const currentX = e.clientX;
          const scrollTo = el.scrollLeft - (currentX - prevX) * 1.5; // 1.5 for fasting swiping
          el.scrollTo(scrollTo, 0);
          leftOrRight = currentX > prevX ? 0 : 1;
          prevX = currentX;
        };
        document.onmouseup = (e) => {
          e.preventDefault();
          el.onmousemove = null;

          if (leftOrRight)
            el.scrollTo({
              left: scrollNext + el.clientWidth,
              behavior: "smooth",
            });
          else
            el.scrollTo({
              left: scrollNext - el.clientWidth,
              behavior: "smooth",
            });
        };
      };
    }
  });

  // modals
  const modalOpeners = document.querySelectorAll("[data-modal-id]");

  modalOpeners.forEach((modalOpener) => {
    const modal = document.querySelector(`#${modalOpener.dataset.modalId}`);

    modalOpener.addEventListener(
      "click",
      () => {
        modal.classList.add("show");
      },
      false
    );

    modal.addEventListener(
      "click",
      (e) => {
        if (e.target.id === modal.id) modal.classList.remove("show");
      },
      false
    );
  });
});

// $("#subscribe-form").submit( function(e){
//   e.preventDefault();

//   //check all fields
//   let elements = subscribe_form.elements;
//   const email = cleanWords(elements[0].value) ;
//   let message, check=true;

//   // check  email
//   message = "";
//   if ( email ){
//     if ( ! validateEmail(email) ){
//       check = false;
//       message = formErrors.email;
//     }
//   }else{
//     check = false;
//     message = formErrors.required;
//   }
//   $("#subscribe-form #email_error").text(message);
//   if ( check ){
//     const thisForm = subscrib_form;
//     $("#subscribe-form  button").text("Chargement ...");
//      grecaptcha.execute(reCAPTCHA_site_key).then(function(token) {
//         const form = new FormData($("#subscribe-form")[0]);
//         form.append('token_key',token);
//         $.ajax({
//           url: '/subscribe',
//           method : 'post',
//           data : form,
//           contentType: false,
//           processData: false,
//         }).done(function(data){
//           notify( formErrors.registration_success, true, false );
//           $("#subscribe-form  button").text("Envoyer");
//           emptyForm( thisForm,0 );
//         }).fail(function(err){
//           message = "";

//           if ( err.responseJSON ){

//             const errors = err.responseJSON;
//             if ( errors["email"] ) message = formErrors.email_exist;
//           }
//           if ( ! message ) message = formErrors.error;
//           notify( message, false, true );
//           $("#subscribe-form  button").text("Envoyer");
//         })
//       })
//     }else{
//       notify( message, false, true );
//     }

//   return check;
// })

// $("#open-modal-trainer").click(function(){
//   $("#modal-trainer").show();
// })
// $(".modal-container").click(function(e){
//   if ( e.target.className === this.className )
//     $(this).hide();
// })
