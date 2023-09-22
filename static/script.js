// Date selection
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; // January is 0!
var yyyy = today.getFullYear();

if (dd < 10) {
   dd = '0' + dd; // Days less than 10 shown as 01,02,... rather than 1,2,...
}

if (mm < 10) {
   mm = '0' + mm; // Months less than 10 shown as 01,02,... rather than 1,2,...
} 
    
today = yyyy + '-' + mm + '-' + dd;
document.getElementById("dateId").setAttribute("max", today); // Set the HTML input type='date' maximum to today.

// Text field for price input

// Restricts input for the given textbox to the given inputFilter function.
function setInputFilter(textbox, inputFilter, errMsg) {
   [ "input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop", "focusout" ].forEach(function(event) {
     textbox.addEventListener(event, function(e) {
       if (inputFilter(this.value)) {
         // Accepted value.
         if ([ "keydown", "mousedown", "focusout" ].indexOf(e.type) >= 0){
           this.classList.remove("input-error");
           this.setCustomValidity("");
         }
 
         this.oldValue = this.value;
         this.oldSelectionStart = this.selectionStart;
         this.oldSelectionEnd = this.selectionEnd;
       }
       else if (this.hasOwnProperty("oldValue")) {
         // Rejected value: restore the previous one.
         this.classList.add("input-error");
         this.setCustomValidity(errMsg);
         this.reportValidity();
         this.value = this.oldValue;
         this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
       }
       else {
         // Rejected value: nothing to restore.
         this.value = "";
       }
     });
   });
 }

// Adds the restriction to our price field.
setInputFilter(document.getElementById("priceId"), function(value) {
   return /^\d*\.?\d*$/.test(value); // Allow digits and '.' only, using a RegExp.
 }, "Käytä vain numeroita ja pistettä.");