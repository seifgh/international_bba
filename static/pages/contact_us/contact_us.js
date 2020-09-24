
$("body").ready( function(){
  grecaptcha.ready(function(){
      $("#contact_us_form").submit( function(e){
        e.preventDefault();
        // $("#contact_us_form  .notf-success").addClass("hide");
        //check all fields

        let elements = this.elements;
         first_name = cleanWords(elements[0].value) ,
         last_name = cleanWords(elements[1].value) ,
         email = cleanWords(elements[2].value) ,
         phone_number = replaceAll(elements[3].value," ",""),
         subject = cleanWords(elements[4].value);

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
          if ( !(/^[0-9]{7,14}$/.test(phone_number.slice(1) ) )     ){
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

            $("#contact_us_form  button").text("Chargement ...");

              grecaptcha.execute(reCAPTCHA_site_key).then(function(token) {
                  $.ajax({
                    url: '/contact',
                    method : 'post',
                    data : {'first_name':first_name,'last_name':last_name,'subject':subject,'email':email,'phone':phone_number,'message':elements[5].value,'token_key':token}
                  }).done(function(data){
                    notify( formErrors.thanks_contact, true, false );
                    $("#contact_us_form  button").text("Envoyer");
                    emptyForm( thisForm, 0 );
                  }).fail(function(err){
                    if ( err.status === 403  )
                      message = formErrors.rate_limit;
                    else
                      message = formErrors.error;
                    notify( message, false, true );
                    $("#contact_us_form  button").text("Envoyer");
                  })

              })


          }
        return check;
      })
    })
})
