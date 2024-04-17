
//document.getElementById('myButton').addEventListener('click', function() {
//            var drawer = document.getElementById('myDrawer');
//            drawer.style.display = drawer.style.display === 'none' ? 'block' : 'none';
//        });
//
//        var closeButtons = document.getElementsById('closeButton');
//        for (var i = 0; i < closeButtons.length; i++) {
//                closeButtons[i].addEventListener('click', function() {
//                document.getElementById('myDrawer').style.display = 'none';
//            });
//        }
//
//
//function reveal() {
//          var reveals = document.querySelectorAll(".anim");
//
//          for (var i = 0; i < reveals.length; i++) {
//            var windowHeight = window.innerHeight;
//            var elementTop = reveals[i].getBoundingClientRect().top;
//            var elementVisible = 100;
//
//            if (elementTop < windowHeight - elementVisible) {
//              reveals[i].classList.add("active");
//            } else {
//              reveals[i].classList.remove("active");
//            }
//          }
//        }
//
//window.addEventListener("scroll", anim);


/*
//Old
var sections = document.querySelectorAll(".profile-sections");
var currentSectionIndex = 0;
var firstSection = sections[0];
var noSections = sections.length;
var progressCont = document.querySelectorAll(".progress-cont");
var progressCount = document.querySelectorAll(".progress-no");
let indexList = [];

//New
//Container
var infoGraph = document.querySelectorAll(".info-graph");
//Circle
var stepCircle = document.querySelectorAll(".steps-circle");

//Label; where the steps content goes
var labelGraphic = document.querySelector(".label-graphic");


var progressCountIncr = document.createElement("div");
*/


//Fixed Sticky
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var scrollingElement = document.getElementById("nav-div");
  // Distance from the top of the document to the top of the scrolling element
  var elementOffset = scrollingElement.offsetTop;
  // Viewport (window) top position
  var windowTop = window.pageYOffset || document.documentElement.scrollTop;

  if (windowTop > elementOffset) {
    scrollingElement.style.position = "fixed";
    scrollingElement.style.top = "0";
  } else {
    scrollingElement.style.position = "relative";
  }
}


//Navigation Dropdown
const navSlide = () => {
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav-links");
  const navLinks = document.querySelectorAll(".nav-links a");

if( nav && burger && navLinks.length > 0){
  burger.addEventListener("click", () => {
    nav.classList.toggle("nav-active");

    navLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = "";
      } else {
        link.style.animation = `navLinkFade 0.5s ease forwards ${
          index / 7 + 0.5
        }s `;
      }
    });
    burger.classList.toggle("toggle");
  });
  //
};
}
navSlide();




function calculateDays() {
    var adJob = document.querySelectorAll("#deadline-div");
    var adDeadline = document.querySelectorAll("#deadline");

    var date = new Date();
    var today = date.getTime(); // Get today's date in milliseconds to compare with deadlines

    for(var i = 0; i < adDeadline.length; i++) {
        // Get each ad's deadline
        var targetedAd = adDeadline[i];
        // Get the targeted ad's date tag and convert it to a Date object
        var deadline = new Date(targetedAd.innerText);
        console.log(deadline);

        // Calculate the days between today's date and the deadline
        var difference = (deadline.getTime() - today) / (1000 * 60 * 60 * 24); // Convert the time difference to days
        console.log("There are still plenty of time: ",difference);
        if (difference > 5) {
            adJob[i].classList.toggle("deadline-is-far");
            console.log("There are still plenty of time");
        } else if (difference <= 5 && difference > 0) {
            adJob[i].classList.toggle("deadline-is-close");
            console.log("We are getting closer to the deadline");
        } else if (difference === 0) {
            adJob[i].classList.toggle("deadline-is-today");
//            console.log("Deadline is today");
        } else if (difference < 0) {
            adJob[i].classList.toggle("deadline-is-over");
//            targetedAd.innerText = targetedAd.innerText  + "Closed";
//            console.log("Deadline is Over");
        }
    }
}

calculateDays();




//Dashboard
const navSideSlide = () => {
  const dashboardBtn = document.querySelector("#dashboard-btn");
  const nav = document.querySelector(".sidebar-main");
  const navLinks = document.querySelectorAll(".sidebar-main a");

if( dashboardBtn && nav && navLinks.length > 0){
  dashboardBtn.addEventListener("click", () => {
    nav.classList.toggle("nav-active-drw");

    navLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = "";
      } else {
        link.style.animation = `navLinkFade 0.5s ease forwards ${
          index / 7 + 0.5
        }s `;
      }
    });
    dashboardBtn.classList.toggle("toggle");
  });
  //
};
}
navSideSlide();




//Password Checker
let password = document.getElementById("password");
let power = document.getElementById("power-point");
confirm_password = document.getElementById("confirm_password");

if (password && power) {
    password.oninput = function () {
        let point = 0;
        let value = password.value;
        let widthPower =
            ["1%", "25%", "50%", "75%", "100%"];
        let colorPower =
            ["#D73F40", "#DC6551", "#F2B84F", "#BDE952", "#3ba62f"];

        if (value.length >= 6) {
            let arrayTest =
                [/[0-9]/, /[a-z]/, /[A-Z]/, /[^0-9a-zA-Z]/];
            arrayTest.forEach((item) => {
                if (item.test(value)) {
                    point += 1;
                }
            });
        }
        power.style.width = widthPower[point];
        power.style.backgroundColor = colorPower[point];
    };
}


//function validatePassword(){
//  if(password.value != confirm_password.value) {
//    confirm_password.setCustomValidity("Passwords Don't Match");
//  } else {
//    confirm_password.setCustomValidity('');
//  }
//}
//
//password.onchange = validatePassword;
//confirm_password.onkeyup = validatePassword;

//
//const categoryFilter = document.querySelectorAll("#category-filter");
//
//for(i=0;i<categoryFilter.length;i++){
//
//categoryFilter[i].addEventListener("change", () => {
//
//    categoryValue = event.target.value;
//
//    var xhr = new XMLHttpRequest();
//    xhr.open('GET', '/job_ads_filtered?value=' + categoryValue,true);
//    xhr.send(categoryValue);
//
//    window.location.reload();
////    return false;
//
//    });
//
//}


//otherNavNone = document.classList




/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
//function myFunction() {
//  document.getElementById("myDropdown").classList.toggle("show");
//}

// Close the dropdown menu if the user clicks outside of it
//window.onclick = function(event) {
//  if (!event.target.matches('.dropbtn')) {
//    var dropdowns = document.getElementsByClassName("dropdown-content");
//    var i;
//    for (i = 0; i < dropdowns.length; i++) {
//      var openDropdown = dropdowns[i];
//      if (openDropdown.classList.contains('show')) {
//        openDropdown.classList.remove('show');
//      }
//    }
//  }
//}




/*
//Old
// Create Divs
var progressCountIncr = document.createElement("div");

// Assign Classes to divs
progressCountIncr.classList.add("progress-no-c");

// Append to parents div
progressCircle.appendChild(progressCountIncr);
*/
