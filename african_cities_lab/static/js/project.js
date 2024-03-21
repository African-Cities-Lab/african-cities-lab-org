import '../sass/project.scss';
import "../css/project.css"

/* Project specific Javascript goes here. */
// TODO: Create a sticky navbar using jquery

(function ($) {
    "use strict";

    // CHANGE TO STICKY NAV

    if($('#moocs_page').length) {

      $(window).scroll(function() {
        var startPx = $(window).scrollTop();

        if(startPx >= 485) {
          $("#main-nav").addClass("sticky-nav");
          $("#moocs_register_link_onmenu").removeClass("d-none");

          var moocs_register_link = $('#moocs_register_link').attr('href');

          $('#moocs_register_link_onmenu').attr('href', moocs_register_link);

        } else {
          $("#main-nav").removeClass("sticky-nav");

          $("#moocs_register_link_onmenu").addClass("d-none");
          $('#moocs_register_link_onmenu').attr('href', '');
        }
      });

    } else {

      $(window).scroll(function() {
        var startPx = $(window).scrollTop();
        startPx >= 95 ? $("#main-nav").addClass("sticky-nav") :  $("#main-nav").removeClass("sticky-nav");
      });
    }

    // HelloBar
    setup_hellobar();
    function setup_hellobar() {
        setTimeout( function() {
            if($(".hellobar").hasClass("d-none")) {
                $(".hellobar").removeClass("d-none");
                return $(".hellobar").addClass("d-block")
            } else {
                return $(".hellobar").addClass("d-block")
            }
        },450);
        return $("#close_hellobar").on("click",function(){
            $(".hellobar").removeClass("d-block");
             $(".hellobar").addClass("d-none");
          return!1
        })
      }

    //Partners logo swipper
    var swiper = new Swiper(".partners-swiper", {
        slidesPerView: 2,
        spaceBetween: 10,
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        freeMode: true,
        pagination: {
            clickable: true,
        },
        breakpoints: {
            640: {
              slidesPerView: 2,
              spaceBetween: 20,
            },
            768: {
              slidesPerView: 3,
              spaceBetween: 40,
            },
            1024: {
              slidesPerView: 4,
              spaceBetween: 60,
            },
        },
    });

    //Home silder
    var swiper = new Swiper(".home-swiper", {
      spaceBetween: 30,
      effect: "fade",
      autoplay: {
        delay: 7000,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    //COUNTER
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });
})(jQuery);
