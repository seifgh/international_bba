Vue.component("news-letter", {
  data() {
    return {
      email: "",
      emailAlreadyExists: false,
      invalid: false,
      isLoading: false,
      unexpectedError: false,
      success: false,
    };
  },
  methods: {
    validateNewsLetterEmail() {
      this.invalid = !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(
        this.email
      );
    },
    newsLetterSubmit({ target }) {
      this.validateNewsLetterEmail();
      if (!this.invalid) {
        this.isLoading = true;
        grecaptcha.ready(() => {
          grecaptcha
            .execute(reCaptchaSiteKey, {
              action: "submit",
            })
            .then(async (token) => {
              const formData = new FormData(target);
              formData.append("token", token);
              try {
                const res = await axios.post("/subscribe", formData);
                this.success = true;
              } catch (err) {
                console.log(err);
                console.log(err.response);
                if (err.response && err.response.status === 400) {
                  const { data } = err.response;
                  if (data && data.email) {
                    this.emailAlreadyExists = true;
                  } else {
                    this.unexpectedError = true;
                  }
                } else {
                  this.unexpectedError = true;
                }
              }
              this.isLoading = false;
            })
            .catch((err) => {
              this.isLoading = false;
              this.unexpectedError = true;
            });
        });
      }
    },
  },
  template: `<div class="block content-center md:w-160 w-full bg-white rounded-md shadow-lg p-5">
                <h3 v-if="success" class="md:text-lg sm:text-md text-sm font-semibold text-left text-center text-suc">
                    Merci pour votre inscription !<br />
                    Votre souscription sera traitée.
                </h3>
                <div v-else>
                    <h3 class="md:text-lg sm:text-md text-sm font-semibold text-left mb-3">
                        Inscrivez-vous à notre newsletter
                    </h3>
                    <form @submit.prevent="newsLetterSubmit" method="post" class="relative flex items-stretch w-full">
                        <input :class="{ 'border-dg anim-shake': invalid || emailAlreadyExists }" @blur="validateNewsLetterEmail" v-model.trim="email" type="text" name="email" placeholder="Mettre votre adresse e-mail" class="w-full pl-4 pr-32 h-12 rounded-lg bg-white shadow-sm border border-gray focus:shadow-outline focus:outline-none" />
                        <button class="absolute right-0 h-full font-semibold bg-pri text-white text-sm rounded-tr-md rounded-br-md px-3 py-2 focus:outline-none">
                            <span v-if="isLoading">En traitement ...</span>
                            <span v-else>S'inscrire</span>
                        </button>
                    </form>
                    <small v-show="invalid" class="text-dg">Ce champ est invalide.</small>
                    <small v-show="emailAlreadyExists" class="text-dg">Cet email existe déjà dans notre liste.</small>
                    <small v-show="unexpectedError" class="text-dg">Une erreur inattendue s'est produite, veuillez vérifier
                    votre connexion ou recommencer plus tard.</small>
                </div>
            </div>`,
});
