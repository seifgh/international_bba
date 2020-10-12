"use strict";

Vue.component("news-letter", {
  data: function data() {
    return {
      email: "",
      emailAlreadyExists: false,
      invalid: false,
      isLoading: false,
      unexpectedError: false,
      success: false
    };
  },
  methods: {
    validateNewsLetterEmail: function validateNewsLetterEmail() {
      this.invalid = !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(this.email);
    },
    newsLetterSubmit: function newsLetterSubmit(_ref) {
      var _this = this;

      var target = _ref.target;
      this.validateNewsLetterEmail();

      if (!this.invalid) {
        this.isLoading = true;
        grecaptcha.ready(function () {
          grecaptcha.execute(reCaptchaSiteKey, {
            action: "submit"
          }).then(function _callee(token) {
            var formData, res, data;
            return regeneratorRuntime.async(function _callee$(_context) {
              while (1) {
                switch (_context.prev = _context.next) {
                  case 0:
                    formData = new FormData(target);
                    formData.append("token", token);
                    _context.prev = 2;
                    _context.next = 5;
                    return regeneratorRuntime.awrap(axios.post("/subscribe", formData));

                  case 5:
                    res = _context.sent;
                    _this.success = true;
                    _context.next = 14;
                    break;

                  case 9:
                    _context.prev = 9;
                    _context.t0 = _context["catch"](2);
                    console.log(_context.t0);
                    console.log(_context.t0.response);

                    if (_context.t0.response && _context.t0.response.status === 400) {
                      data = _context.t0.response.data;

                      if (data && data.email) {
                        _this.emailAlreadyExists = true;
                      } else {
                        _this.unexpectedError = true;
                      }
                    } else {
                      _this.unexpectedError = true;
                    }

                  case 14:
                    _this.isLoading = false;

                  case 15:
                  case "end":
                    return _context.stop();
                }
              }
            }, null, null, [[2, 9]]);
          })["catch"](function (err) {
            _this.isLoading = false;
            _this.unexpectedError = true;
          });
        });
      }
    }
  },
  template: "<div class=\"block content-center md:w-160 w-full bg-white rounded-md shadow-lg p-5\">\n                <h3 v-if=\"success\" class=\"md:text-lg sm:text-md text-sm font-semibold text-left text-center text-suc\">\n                    Merci pour votre inscription !<br />\n                    Votre souscription sera trait\xE9e.\n                </h3>\n                <div v-else>\n                    <h3 class=\"md:text-lg sm:text-md text-sm font-semibold text-left mb-3\">\n                        Inscrivez-vous \xE0 notre newsletter\n                    </h3>\n                    <form @submit.prevent=\"newsLetterSubmit\" method=\"post\" class=\"relative flex items-stretch w-full\">\n                        <input :class=\"{ 'border-dg anim-shake': invalid || emailAlreadyExists }\" @blur=\"validateNewsLetterEmail\" v-model.trim=\"email\" type=\"text\" name=\"email\" placeholder=\"Mettre votre adresse e-mail\" class=\"w-full pl-4 pr-32 h-12 rounded-lg bg-white shadow-sm border border-gray focus:shadow-outline focus:outline-none\" />\n                        <button class=\"absolute right-0 h-full font-semibold bg-pri text-white text-sm rounded-tr-md rounded-br-md px-3 py-2 focus:outline-none\">\n                            <span v-if=\"isLoading\">En traitement ...</span>\n                            <span v-else>S'inscrire</span>\n                        </button>\n                    </form>\n                    <small v-show=\"invalid\" class=\"text-dg\">Ce champ est invalide.</small>\n                    <small v-show=\"emailAlreadyExists\" class=\"text-dg\">Cet email existe d\xE9j\xE0 dans notre liste.</small>\n                    <small v-show=\"unexpectedError\" class=\"text-dg\">Une erreur inattendue s'est produite, veuillez v\xE9rifier\n                    votre connexion ou recommencer plus tard.</small>\n                </div>\n            </div>"
});