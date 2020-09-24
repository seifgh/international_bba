window.addEventListener("DOMContentLoaded", function () {});

//   $('body').ready(function(){

//     $("#open-modal-1").click(function(){
//       $("#modal-1").show();
//     })
//     $(".modal-container").click(function(e){
//       if ( e.target.className === this.className )
//         $(this).hide();
//     })

//   $("#catalogue_form").submit( function(e){
//     e.preventDefault();
//     //check all fields
//     $("#catalogue_form  .notf-success").addClass("hide");
//     const email = cleanWords(this.elements[0].value)
//     // check  email
//     let message = "", check = true;
//     if ( email ){
//       if ( ! validateEmail(email) ){
//         check = false;
//         message =formErrors.email;
//       }
//     }else{
//       check = false;
//       message =formErrors.required;
//     }
//     $("#email_error").text(message);
//     if ( check ){
//         const thisForm = this;
//         $("#catalogue_form  button").text("Chargement ...");
//         grecaptcha.execute(reCAPTCHA_site_key).then( function(token) {
//         $.ajax({
//           url: '/',
//           method : 'post',
//           data : {'email':email,'token_key':token}
//         }).done(function(data){
//           notify( formErrors.catalog, true, false );
//           $("#catalogue_form  button").text("Envoyer");
//           $(".modal-container").click();
//           emptyForm( thisForm, 0 );
//         }).fail(function(err){
//           notify( formErrors.error, false, true );
//           $("#catalogue_form  button").text("Envoyer");
//         })
//       })
//     }

//     return check;
//   })
// })
