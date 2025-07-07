document.addEventListener('DOMContentLoaded', function() {
  const percentageEl = document.getElementById('percentage');
  const progressBar = document.getElementById('progress-bar');
  const imageOverlay = document.getElementById('image-overlay');
  
  let percentage = 0;
  
  // Simulate loading process
  const loadingInterval = setInterval(() => {
    percentage += 1;
    
    // Update percentage text
    percentageEl.textContent = `${percentage}%`;
    
    // Update progress bar width
    progressBar.style.width = `${percentage}%`;
    
    // Update image overlay (reveal image from bottom)
    imageOverlay.style.height = `${100 - percentage}%`;
    
    if (percentage >= 100) {
      clearInterval(loadingInterval);

      // Fade out preloader
      setTimeout(() => {
        document.querySelector('.preloader').style.opacity = '0';
        document.querySelector('.preloader').style.pointerEvents = 'none';
      }, 300);

      // Remove from DOM completely
      setTimeout(() => {
        document.querySelector('.preloader').style.display = 'none';
      }, 1000);
    }
  }, 40);
});





document.querySelectorAll('.solution-box').forEach(function(box) {
    box.addEventListener('touchstart', function() {
      this.classList.add('touched');
    });
    box.addEventListener('touchend', function() {
      setTimeout(() => this.classList.remove('touched'), 1000);
    });
  });



// Initialize Swiper for the investment carousel
// Ensure Swiper JS is loaded before this script
// File: assets/js/script.js
// --- a/file:///c%3A/Users/Administrator/Desktop/damascus_full_static_site/assets/js/script.js
// +++ b/file:///c%3A/Users/Administrator/Desktop/damascus_full_static_site/assets/js/script.js
// @@ -1,0 +1,22 @@
//  assets/js/script.js
//  This file contains JavaScript code for the Damascus Projects & Services website.  
  var swiper = new Swiper(".myInvestSwiper", {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    autoplay: {
      delay: 3000, // 3 seconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev"
    },
    breakpoints: {
      768: {
        slidesPerView: 2
      }
    }
  });
