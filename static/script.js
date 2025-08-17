// Highlight active nav link on scroll
const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll("header ul li a");

window.addEventListener("scroll", () => {
    let current = "";
    sections.forEach((section) => {
        const sectionTop = section.offsetTop - 80;
        if (pageYOffset >= sectionTop) {
            current = section.getAttribute("id");
        }
    });
    navLinks.forEach((link) => {
        link.classList.remove("active");
        if (link.getAttribute("href") === `#${current}`) {
            link.classList.add("active");
        }
    });
});

// Menu icon toggle for navbar
const menuIcon = document.getElementById('menu-icon');
const navbar = document.querySelector('.navbar');

menuIcon.addEventListener('click', () => {
    menuIcon.classList.toggle('active');
    navbar.classList.toggle('active');
    
    // Toggle body scroll when menu is open
    if (navbar.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = 'auto';
    }
});

// Close menu when clicking on a link (mobile)
document.querySelectorAll('.navbar a').forEach(link => {
    link.addEventListener('click', () => {
        navbar.classList.remove('active');
        menuIcon.classList.remove('active');
        document.body.style.overflow = 'auto';
    });
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    if (!navbar.contains(e.target) && !menuIcon.contains(e.target)) {
        navbar.classList.remove('active');
        menuIcon.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        navbar.classList.remove('active');
        menuIcon.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

// ======================
// Gallery Modal Logic (Images Only)
// ======================
let currentGallery = [];
let currentIndex = 0;

document.querySelectorAll('.gallery-icon').forEach(icon => {
    icon.addEventListener('click', function () {
        const fileList = this.getAttribute('data-gallery-files');
        if (fileList) {
            currentGallery = fileList.split(',').map(item => item.trim());
            currentIndex = 0;
            showModal();
        }
    });
});

function showModal() {
    document.getElementById('galleryModal').style.display = 'flex';
    showSlide(currentIndex);
}

function closeModal() {
    document.getElementById('galleryModal').style.display = 'none';
}

function showSlide(index) {
    const currentFile = currentGallery[index];
    const modalImage = document.getElementById('modalImage');
    const indicators = document.getElementById('galleryIndicators');

    // Show image only
    modalImage.src = currentFile;
    modalImage.style.display = 'block';

    // Create indicators
    indicators.innerHTML = '';
    currentGallery.forEach((_, i) => {
        const dot = document.createElement('div');
        dot.className = 'indicator' + (i === index ? ' active' : '');
        dot.onclick = () => {
            currentIndex = i;
            showSlide(currentIndex);
        };
        indicators.appendChild(dot);
    });
}

// Gallery modal arrow event listeners
document.querySelector('#galleryModal .close').onclick = closeModal;
document.getElementById('prevSlide').onclick = function () {
    currentIndex = (currentIndex - 1 + currentGallery.length) % currentGallery.length;
    showSlide(currentIndex);
};
document.getElementById('nextSlide').onclick = function () {
    currentIndex = (currentIndex + 1) % currentGallery.length;
    showSlide(currentIndex);
};

// ======================
// Video Modal Logic (Videos Only)
// ======================
let currentVideoGallery = [];
let currentVideoIndex = 0;

document.querySelectorAll('.video-icon').forEach(icon => {
    icon.addEventListener('click', function () {
        const fileList = this.getAttribute('data-videos-files');
        if (fileList) {
            currentVideoGallery = fileList.split(',').map(item => item.trim());
            currentVideoIndex = 0;
            showVideoModal();
        }
    });
});

function showVideoModal() {
    document.getElementById('videoModal').style.display = 'flex';
    showVideoSlide(currentVideoIndex);
}

function closeVideoModal() {
    document.getElementById('videoModal').style.display = 'none';
}

function showVideoSlide(index) {
    const currentFile = currentVideoGallery[index];
    const modalVideo = document.getElementById('modalVideo');
    const indicators = document.getElementById('videoIndicators');

    // Show video only
    modalVideo.src = currentFile;
    modalVideo.style.display = 'block';
    modalVideo.load();

    // Create indicators
    indicators.innerHTML = '';
    currentVideoGallery.forEach((_, i) => {
        const dot = document.createElement('div');
        dot.className = 'indicator' + (i === index ? ' active' : '');
        dot.onclick = () => {
            currentVideoIndex = i;
            showVideoSlide(currentVideoIndex);
        };
        indicators.appendChild(dot);
    });
}

// Video modal arrow event listeners
document.querySelector('#videoModal .close').onclick = closeVideoModal;
document.getElementById('prevVideoSlide').onclick = function () {
    currentVideoIndex = (currentVideoIndex - 1 + currentVideoGallery.length) % currentVideoGallery.length;
    showVideoSlide(currentVideoIndex);
};
document.getElementById('nextVideoSlide').onclick = function () {
    currentVideoIndex = (currentVideoIndex + 1) % currentVideoGallery.length;
    showVideoSlide(currentVideoIndex);
};

// ======================
// Modal click outside to close
// ======================
window.onclick = function (event) {
    const galleryModal = document.getElementById('galleryModal');
    if (event.target == galleryModal) {
        closeModal();
    }
    const videoModal = document.getElementById('videoModal');
    if (event.target == videoModal) {
        closeVideoModal();
    }
    const infoModal = document.getElementById('infoModal');
    if (event.target == infoModal) {
        infoModal.style.display = 'none';
    }
    // Login modal close
    const loginModal = document.getElementById('loginModal');
    if (event.target == loginModal) {
        loginModal.style.display = 'none';
    }
};

// ======================
// Info modal logic (supports HTML)
// ======================
const infoIcons = document.querySelectorAll('.info-icon');
const infoModal = document.getElementById('infoModal');
const infoModalContent = document.getElementById('infoModalContent');
const closeInfo = document.querySelector('.close-info');

infoIcons.forEach(icon => {
    icon.addEventListener('click', function () {
        const rawHTML = this.getAttribute('data-info');
        infoModalContent.innerHTML = decodeHTMLEntities(rawHTML);
        infoModal.style.display = 'flex';
    });
});

closeInfo.onclick = function () {
    infoModal.style.display = 'none';
};

function decodeHTMLEntities(text) {
    const div = document.createElement("div");
    div.innerHTML = text;
    return div.textContent;
}

// ======================
// Section Scroll Reveal Animation
// ======================

document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll("section");
  
    const options = {
      root: null,
      threshold: 0.1,
    };
  
    const revealSection = (entries, observer) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      });
    };
  
    const observer = new IntersectionObserver(revealSection, options);
  
    sections.forEach(section => {
      section.classList.add("hidden");
      observer.observe(section);
    });
  });


/*  // Animate home content and image container//
const home = document.querySelector('.home');
const homeContainer = document.querySelector('.home-container');

if (home && homeContainer) {
  const homeObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        home.classList.add('home-visible');
        homeContainer.classList.add('home-visible');
        homeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  homeObserver.observe(home);
}*/
document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll("section");

  const options = {
    root: null,
    threshold: 0.1,
  };

  const revealSection = (entries, observer) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("visible");

      // Special handling for home-container
      if (entry.target.id === "home") {
        const homeContainer = document.querySelector(".home-container");
        if (homeContainer) {
          homeContainer.classList.add("visible");
        }
      }

      observer.unobserve(entry.target);
    });
  };

  const observer = new IntersectionObserver(revealSection, options);

  sections.forEach(section => {
    section.classList.add("hidden");
    observer.observe(section);
  });
});

document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".home").classList.add("visible");
});

document.querySelectorAll('.bxs-file-pdf').forEach(btn => {
  btn.addEventListener('click', () => {
    const fileDropdown = btn.closest('.project-text')?.querySelector('.file-dropdown');
    const fileModal = document.getElementById('fileModal');
    const fileModalContent = document.getElementById('fileModalContent');

    if (fileDropdown && fileModal && fileModalContent) {
      fileModalContent.innerHTML = '<h3>Download Files</h3>' + fileDropdown.innerHTML;
      fileModal.style.display = 'block';
    }
  });
});

