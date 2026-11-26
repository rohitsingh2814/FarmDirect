document.addEventListener("DOMContentLoaded", function () {
  const reveals = document.querySelectorAll(".fd-reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08 }
    );
    reveals.forEach((el, idx) => {
      el.style.transitionDelay = `${Math.min((idx % 6) * 65, 320)}ms`;
      observer.observe(el);
    });
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }
});
