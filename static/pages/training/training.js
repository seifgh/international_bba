




$("body").ready(function(){

  const navMenuElements = $(".nav-selector > .menu-bar > *");
  const navPages = $(".nav-selector > .pages > *");
  navMenuElements.click(function(){
    const PageId = this.id.replace("selector-","");
    navMenuElements.removeClass("active");
    navPages.removeClass("show");
    let i = 0;
    for ( i = 0; i < navMenuElements.length; i++ ){
      if ( navMenuElements[i].id === "selector-"+PageId ){
        navMenuElements[i].className = "active";
        break;
      }
    }
    for ( i = 0; i < navPages.length; i++ ){
      if ( navPages[i].id === PageId ){
        navPages[i].className = "show";
        break;
      }
    }
  })


    $("#training-form").submit( function(e){
      e.preventDefault();
      //check all fields
      const elements = this.elements;
       first_name = cleanWords(elements[1].value) ,
       last_name = cleanWords(elements[2].value) ,
       email = cleanWords(elements[3].value) ,
       phone_number = replaceAll(elements[4].value," ",""),
       subject = cleanWords(elements[5].value);

      //check name and last name
      let message = "", check=true;
      if ( first_name  ){
        if ( first_name.length < 2 ){
          check=false;
          message = formErrors.lengthError( min_length = 2 );
        }
      }else{
        check=false;
        message = formErrors.required;
      }
      $("#first_name_error").text(message);


      message ="";
      if ( last_name  ){
        if ( last_name.length < 2 ){
          check=false;
          message = formErrors.lengthError( min_length = 2 );
        }
      }else{
        check=false
        message = formErrors.required;
      }
      $("#last_name_error").text(message);

      // check  email
      message = "";
      if ( email ){
        if ( ! validateEmail(email) ){
          check = false;
          message = formErrors.email;
        }
      }else{
        check = false;
        message =formErrors.required;
      }
      $("#email_error").text(message);

      //check phone number using regx
      message = "";
      if ( phone_number ){

        if ( !(/^[0-9]{7,14}$/.test(phone_number.slice(1) ) ) ){
          check = false;
          message = formErrors.phone;
        }
      }else{
        check = false;
        message = formErrors.required;
      }

      $("#phone_number_error").text(message);

      //sujet
      message ="";
      if ( subject  ){
        if ( subject.length < 2 ){
          check = false;
          message = formErrors.lengthError( min_length = 2 );
         }
      }else{
        check = false;
        message = formErrors.required;
      }
      $("#subject_error").text(message);


      if ( check ){
        const thisForm = this;

        $("#training-form  button").text("Chargement ...");
         grecaptcha.execute(reCAPTCHA_site_key).then(function(token) {

            const form = new FormData($("#training-form")[0]);
            form.set('phone',phone_number);
            form.append('token_key',token);
            $.ajax({
              url: '/registration/create',
              method : 'post',
              data : form,
              contentType: false,
              processData: false,
            }).done(function(data){
              notify( formErrors.emailVerify( email ) , true, false );
              $("#training-form  button").text("Envoyer");
              $(".modal-container").click();
              emptyForm( thisForm, 0 );
            }).fail(function(err){
              message = "";
              if ( err.responseJSON ){
                const errors = err.responseJSON;
                if ( errors["__all__"] ){
                  errors['__all__'].map( err =>{
                      message += " " + err + ","
                  })
                  message = message.slice(0, message.length - 1);
                }
              }
              if ( ! message ){
                if ( err.status === 403  )
                  message = formErrors.rate_limit;
                else
                  message = formErrors.error;
              }
              notify( message, false, true );
              $("#training-form  button").text("Envoyer");
            })
          })
        }
      return check;
    })
})
