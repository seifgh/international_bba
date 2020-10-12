const app = new Vue({
  el: "#app",
  delimiters: ["$[", "]"],
  data: {
    showNav: window.innerWidth < 768 ? false : true,
    form: {
      firstName: {
        value: "",
        required: false,
        invalid: false,
        hasError: false,
      },
      lastName: {
        value: "",
        required: false,
        invalid: false,
        hasError: false,
      },
      email: {
        value: "",
        required: false,
        invalid: false,
        alreadyExists: false,
        hasError: false,
      },
      phone: {
        value: "",
        required: false,
        invalid: false,
        hasError: false,
      },
      subject: {
        value: document.querySelector("input[name=subject]").value,
        required: false,
        invalid: false,
        hasError: false,
      },
      message: {
        value: "",
        required: false,
        invalid: false,
        hasError: false,
      },
      isValid: false,
      isLoading: false,
      unexpectedError: false,
      success: false,
    },
  },
  methods: {
    validate(propertyName, validator) {
      const { value } = this.form[propertyName];
      this.form[propertyName].hasError = false;

      if (value) {
        this.form[propertyName].required = false;
        const isInvalid = validator(value);
        this.form[propertyName].invalid = isInvalid;
        this.form[propertyName].hasError = isInvalid;
        this.form.isValid = !isInvalid;
      } else {
        this.form[propertyName].invalid = false;
        this.form[propertyName].required = true;
        this.form[propertyName].hasError = true;
        this.form.isValid = false;
      }
    },
    validateFirstName() {
      this.validate("firstName", (v) => v.length < 2 || v.length > 50);
    },
    validateLastName() {
      this.validate("lastName", (v) => v.length < 2 || v.length > 50);
    },
    validateEmail() {
      this.validate(
        "email",
        (v) =>
          !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(
            v
          )
      );
    },
    validatePhone() {
      this.validate(
        "phone",
        (v) => !/^\+?([0-9]{2,3})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{4})$/.test(v)
      );
    },
    validateSubject() {
      this.validate("subject", (v) => v.length < 2 || v.length > 100);
    },
    validateMessage() {
      this.validate("message", (v) => v.length < 10 || v.length > 250);
    },
    validateAll() {
      this.form.unexpectedError = false;
      this.form.isValid = true;
      this.validateFirstName();
      this.validateLastName();
      this.validateEmail();
      this.validatePhone();
      this.validateSubject();
      this.validateMessage();
    },
    submit({ target }) {
      this.validateAll();
      if (this.form.isValid) {
        this.form.isLoading = true;
        grecaptcha.ready(() => {
          grecaptcha
            .execute(reCaptchaSiteKey, {
              action: "submit",
            })
            .then(async (token) => {
              const formData = new FormData(target);
              formData.append("token", token);
              try {
                const res = await axios.post("/contact", formData);
                this.form.success = true;
              } catch (err) {
                console.log(err.response);
                if (err.response && err.response.status === 400) {
                  const { data } = err.response;
                  if (data && data.email) {
                    this.form.email.alreadyExists = true;
                    this.form.email.hasError = true;
                  } else {
                    this.form.unexpectedError = true;
                  }
                } else {
                  this.form.unexpectedError = true;
                }
              }
              this.form.isLoading = false;
            })
            .catch((err) => {
              this.form.isLoading = false;
              this.form.unexpectedError = true;
            });
        });
      }
    },
  },
});
