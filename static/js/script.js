// Additional JS for enhanced functionality
document.addEventListener('DOMContentLoaded', function() {
  const carousel = document.querySelector('#heroCarousel');
  
  // Pause carousel when hovering over controls
  const controls = document.querySelectorAll('.carousel-control-prev, .carousel-control-next');
  controls.forEach(control => {
    control.addEventListener('mouseenter', () => {
      const carouselInstance = bootstrap.Carousel.getInstance(carousel);
      carouselInstance.pause();
    });
    control.addEventListener('mouseleave', () => {
      const carouselInstance = bootstrap.Carousel.getInstance(carousel);
      carouselInstance.cycle();
    });
  });
  
  // Add parallax effect to background images
  carousel.addEventListener('mousemove', (e) => {
    const items = document.querySelectorAll('.carousel-item.active .carousel-background');
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    items.forEach(item => {
      item.style.transform = `scale(1.05) translate(${x * 20}px, ${y * 20}px)`;
    });
  });
});




document.querySelectorAll('.solution-box').forEach(function(box) {
    box.addEventListener('touchstart', function() {
      this.classList.add('touched');
    });
    box.addEventListener('touchend', function() {
      setTimeout(() => this.classList.remove('touched'), 1000);
    });
  });




// Initialize Swiper with autoplay
document.addEventListener('DOMContentLoaded', function() {
    new Swiper('.myInvestSwiper', {
      slidesPerView: 1,
      spaceBetween: 20,
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
          spaceBetween: 15
        },
        992: {
          slidesPerView: 3,
          spaceBetween: 20
        }
      }
    });
  });











document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', function() {
        const parent = this.parentElement;
        parent.classList.toggle('active');
    });
});







  document.addEventListener("DOMContentLoaded", function(){
    if (window.innerWidth > 992) {
      document.querySelectorAll('.navbar .dropdown').forEach(function(everydropdown){
        everydropdown.addEventListener('mouseover', function(e){
          let el_link = this.querySelector('a[data-bs-toggle]');
          if(el_link != null){
            let nextEl = el_link.nextElementSibling;
            el_link.classList.add('show');
            nextEl.classList.add('show');
          }
        });
        everydropdown.addEventListener('mouseleave', function(e){
          let el_link = this.querySelector('a[data-bs-toggle]');
          if(el_link != null){
            let nextEl = el_link.nextElementSibling;
            el_link.classList.remove('show');
            nextEl.classList.remove('show');
          }
        })
      });
    }
  });