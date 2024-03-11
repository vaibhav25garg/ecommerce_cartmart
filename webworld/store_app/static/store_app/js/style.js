function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }
  
  /* Set the width of the side navigation to 0 */
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }

function openCart() {
   document.getElementById("mySidecart").style.width = "350px";
}
  
/* Set the width of the side navigation to 0 */
function closeCart() {
  document.getElementById("mySidecart").style.width = "0";
}

function openFilter() {
  document.getElementById("mySidefilter").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeFilter() {
 document.getElementById("mySidefilter").style.width = "0";
}

var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  // x[slideIndex-1].style.display = "block";  
}

$(document).ready(function() {
  $('#autoWidth').lightSlider({
      autoWidth:true,
      loop:true,
      onSliderLoad: function() {
          $('#autoWidth').removeClass('cS-hidden');
      } 
  });  
});

