// Bus Registrtation Number validation


var busRegistrationNumber= document.getElementById("busRegistrationNumber");
var busRegistrationNumberValidation=function(){

   busRegistrationNumberValue=busRegistrationNumber.value.trim();
   validbusRegistrationNumber=/^[A-Z]{2} \d{2} [A-Z]{2} \d{4}$/;
   busRegistrationNumberErr=document.getElementById('bus-Registration-Number-err');

   if(busRegistrationNumberValue=="" )
   {
    busRegistrationNumberErr.innerHTML="Bus Registration Number is required";
    busRegistrationNumberErr.style.color ="red";


   }
   else if(!validbusRegistrationNumber.test(busRegistrationNumberValue)){
     busRegistrationNumberErr.innerHTML="Please enter a valid vehicle registration number (e.g., AB 12 CD 1234).";
        busRegistrationNumberErr.style.color ="red";

   }
   else{
     busRegistrationNumberErr.innerHTML="";
     return true;

   }
}

busRegistrationNumber.oninput=function(){
   busRegistrationNumberValidation();
}

// bus type
var busType= document.getElementById("busType");
var busTypeValidation=function(){

   busTypeValue=busType.value.trim();
   busTypeErr=document.getElementById('bus-type-err');

   if(TypeValue==="" )
   {
    busTypeErr.innerHTML="Please select a valid bus type";
    busTypeErr.style.color ="red";
   }
   else{
     busTypeErr.innerHTML="";
     return true;
   }
}
busType.oninput=function(){
   busTypeValidation();
}


// total seats
var totalSeats= document.getElementById("totalSeats");

var totalSeatsValidation=function(){

   // totalSeatsValue=totalSeats.value.trim();
   totalSeatsValue = parseInt(totalSeats.value, 10);
   totalSeatsErr=document.getElementById('total-seats-err');

   if(totalSeatsValue=="" )
   {
    totalSeatsErr.innerHTML="Total Seats is required";
    totalSeatsErr.style.color ="red";
   }
   else if(totalSeatsValue < 1 || totalSeatsValue > 198)
   {
    totalSeatsErr.innerHTML="Seats Overflow!";
    totalSeatsErr.style.color ="red";
   }
   else{
     totalSeatsErr.innerHTML="";
     return true;

   }
}

totalSeats.oninput=function(){

   totalSeatsValidation();
}

// drivers name
  var driversfullname= document.getElementById("driversfullname");

  var driversfullnameValidation= function(){

   driversfullnameValue=driversfullname.value.trim();
   validdriversfullname=/^[A-Za-z]\s[^\s]+[A-Za-z]\s[^\s]+[A-Za-z]+$/;
   driversfullnameErr=document.getElementById('driver-fullname-err');

   if(driversfullnameValue=="")
   {
    driversfullnameErr.innerHTML="FullName is required";
driversfullnameErr.style.color ="red";
   }else if(!validdriversfullname.test(driversfullnameValue)){
     driversfullnameErr.innerHTML="Please enter a valid FullName (e.g., ABC abc Cdd).";
    driversfullnameErr.style.color ="red";
   }else{
     driversfullnameErr.innerHTML="";
     return true;
   }
  }

driversfullname.oninput=function(){

   driversfullnameValidation();
}

 var driversMobile= document.getElementById("driversMobile");;
 var driversMobileValidation= function(){

  driversMobileValue=driversMobile.value.trim();
   validdriversMobile=/^\d{10}$/;
   driversMobileErr=document.getElementById('driver-mobile-err');

   if(driversMobileValue=="")
   {
    driversMobileErr.innerHTML="Mobile Number is required";
driversMobileErr.style.color ="red";
   }
   else if(!validdriversMobile.test(driversMobileValue)){
     driversMobileErr.innerHTML="Please enter a valid 10-digit mobile number.";
     driversMobileErr.style.color ="red";
   }else{
     driversMobileErr.innerHTML="";
     return true;
   }

 }

driversMobile.oninput=function(){

   driversMobileValidation();
}

document.getElementById("addbusform").onsubmit=function e(){
  busRegistrationNumberValidation();
  busTypeValidation();
  totalSeatsValidation();
  driversfullnameValidation();
  driversMobileValidation();

  if(busRegistrationNumberValidation()==true &&
    busTypeValidation()==true &&
    totalSeatsValidation() == true &&
    driversfullnameValidation() == true &&
    driversMobileValidation() == true
  ){
	return true;
  }else{
    return false;
  }
}
if(error == false){
    btn.disabled = false;
}