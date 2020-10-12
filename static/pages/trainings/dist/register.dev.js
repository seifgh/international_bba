"use strict";

var app = new Vue({
  el: "#app",
  delimiters: ["$[", "]"],
  data: {
    showNav: window.innerWidth < 768 ? false : true,
    form: {
      firstName: {
        value: "",
        required: false,
        invalid: false,
        hasError: false
      },
      lastName: {
        value: "",
        required: false,
        invalid: false,
        hasError: false
      },
      email: {
        value: "",
        required: false,
        invalid: false,
        alreadyExists: false,
        hasError: false
      },
      phone: {
        value: "",
        required: false,
        invalid: false,
        hasError: false
      },
      address: {
        value: "",
        required: false,
        invalid: false,
        hasError: false
      },
      message: {
        value: "",
        invalid: false,
        hasError: false
      },
      priceDemanded: {
        value: false
      },
      isValid: false,
      isLoading: false,
      unexpectedError: false,
      success: false
    }
  },
  methods: {
    validate: function validate(propertyName, validator) {
      var value = this.form[propertyName].value;
      this.form[propertyName].hasError = false;

      if (value) {
        this.form[propertyName].required = false;
        var isInvalid = validator(value);
        this.form[propertyName].invalid = isInvalid;
        this.form[propertyName].hasError = isInvalid;
        this.form.isValid = !isInvalid;
      } else if ("required" in this.form[propertyName]) {
        this.form[propertyName].invalid = false;
        this.form[propertyName].required = true;
        this.form[propertyName].hasError = true;
        this.form.isValid = false;
      }
    },
    validateFirstName: function validateFirstName() {
      this.validate("firstName", function (v) {
        return v.length < 2 || v.length > 50;
      });
    },
    validateLastName: function validateLastName() {
      this.validate("lastName", function (v) {
        return v.length < 2 || v.length > 50;
      });
    },
    validateEmail: function validateEmail() {
      this.validate("email", function (v) {
        return !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(v);
      });
    },
    validatePhone: function validatePhone() {
      this.validate("phone", function (v) {
        return !/^\+?([0-9]{2,3})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{4})$/.test(v);
      });
    },
    validateAddress: function validateAddress() {
      this.validate("address", function (v) {
        return v.length < 2 || v.length > 95;
      });
    },
    validateMessage: function validateMessage() {
      this.validate("message", function (v) {
        return v.length > 250;
      });
    },
    validateAll: function validateAll() {
      this.form.unexpectedError = false;
      this.form.isValid = true;
      this.validateFirstName();
      this.validateLastName();
      this.validateEmail();
      this.validatePhone();
      this.validateAddress();
      this.validateMessage();
    },
    submit: function submit(_ref) {
      var _this = this;

      var target = _ref.target;
      this.validateAll();

      if (this.form.isValid) {
        this.form.isLoading = true;
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
                    return regeneratorRuntime.awrap(axios.post("/training/register", formData));

                  case 5:
                    res = _context.sent;
                    _this.form.success = true;
                    _context.next = 13;
                    break;

                  case 9:
                    _context.prev = 9;
                    _context.t0 = _context["catch"](2);
                    console.log(_context.t0.response);

                    if (_context.t0.response && _context.t0.response.status === 400) {
                      data = _context.t0.response.data;

                      if (data && data.__all__) {
                        _this.form.email.alreadyExists = true;
                        _this.form.email.hasError = true;
                      } else {
                        _this.form.unexpectedError = true;
                      }
                    } else {
                      _this.form.unexpectedError = true;
                    }

                  case 13:
                    _this.form.isLoading = false;

                  case 14:
                  case "end":
                    return _context.stop();
                }
              }
            }, null, null, [[2, 9]]);
          })["catch"](function (err) {
            _this.form.isLoading = false;
            _this.form.unexpectedError = true;
          });
        });
      }
    }
  }
});