


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
  $("#open-modal-1").click(function(){
    $("#modal-1").show();
  })
  $(".modal-container").click(function(e){
    if ( e.target.className === this.className )
      $(this).hide();
  })
  $("#file-input-open").click( function(e){
      $("#file-input").click()
  })

    $("#trainer-form").submit( function(e){
      e.preventDefault();
      // $("#trainer-form  .notf-success").addClass("hide");
      //check all fields
      const elements = this.elements;
      const first_name = cleanWords(elements[0].value) ,
       last_name = cleanWords(elements[1].value) ,
       email = cleanWords(elements[2].value) ,
       phone_number = replaceAll(elements[3].value," ",""),
       profession = cleanWords(elements[5].value),
       files = elements[4].files;

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
        if ( !(/^[0-9]{7,14}$/.test(phone_number.slice(1) ) )      ){
          check = false;
          message = formErrors.phone;
        }
      }else{
        check = false;
        message = formErrors.required;
      }

      $("#phone_number_error").text(message);

      //profession
      message ="";
      if ( profession  ){
        if ( profession.length < 2 ){
          check = false;
          message = formErrors.lengthError( min_length = 2 );
        }
      }else{
        check = false;
        message = formErrors.required;
      }
      $("#profession_error").text(message);

      message = "";

      if ( files.length >= 1 ){
        const ext = files[0].name.slice(files[0].name.length - 3) ;
        if ( ext !== 'pdf' && ext !== 'png'  ){
          check = false;
          message = formErrors.type_error;
        }
        if ( files[0].size > 5242880 ){
          check = false;
          message += form.fileSizeError( max_size = '5 Mo' );
        }
      }else{
        check = false;
        message = formErrors.required;
      }
      $("#file_error").text(message);

      if ( check ){
        const thisForm = this;
        $("#trainer-form  button").text("Chargement ...");
         grecaptcha.execute(reCAPTCHA_site_key).then(function(token) {
            const form = new FormData($("#trainer-form")[0]);
            form.set('phone',phone_number);
            form.append('token_key',token);
            $.ajax({
              url: '/trainer',
              method : 'post',
              cache: false,
              data : form,
              contentType: false,
              processData: false,
            }).done(function(data){
              notify(  formErrors.emailVerify( email ), true, false );
              $("#trainer-form  button").text("Envoyer");
              emptyForm( thisForm,0 );
            }).fail(function(err){
              if ( err.status === 403  )
                message = formErrors.rate_limit;
              else
                message = formErrors.error;
              notify( message, false, true )
              $("#trainer-form  button").text("Envoyer");
            })
          })
        }

      return check;
    })
})
