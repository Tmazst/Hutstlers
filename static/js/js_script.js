


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
//        console.log(deadline);

        // Calculate the days between today's date and the deadline
        var difference = (deadline.getTime() - today) / (1000 * 60 * 60 * 24); // Convert the time difference to days
//        console.log("There are still plenty of time: ",difference);

        if (difference > 5) {
            adJob[i].classList.toggle("deadline-is-far");
//            console.log("There are still plenty of time");

        } else if (difference <= 5 && difference > 0) {
            adJob[i].classList.toggle("deadline-is-close");
//            console.log("We are getting closer to the deadline");

        } else if (difference === 0) {
            adJob[i].classList.toggle("deadline-is-today");
//            console.log("Deadline is today");

        } else if (difference < 0) {
            adJob[i].classList.toggle("deadline-is-over");

        }
    }
}

calculateDays();


function checkDate(){

    var applyBtn = document.querySelector(".jb-viewed-card-body a");
    var appDeadline = document.querySelector("#deadline");

    var date = new Date();
    var today = date.getTime(); // Get today's date in milliseconds to compare with deadlines

    var deadline = new Date(appDeadline.innerText);

    console.log("Clicked!!",deadline.getTime());

    // Calculate the days between today's date and the deadline
    var differenceDate = (deadline.getTime() - today) / (1000 * 60 * 60 * 24);

    if (differenceDate < 0) {
            applyBtn.style.visibility="hidden";
            console.log("Clicked!!",difference);
    }
}

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

