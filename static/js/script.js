
function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


document.addEventListener("DOMContentLoaded", function() {
  const btn = document.getElementById("dark-mode-btn");

    btn.addEventListener("click", function() {
      const currentTheme = getCookie("theme");
      if (currentTheme === "dark") {
        document.documentElement.setAttribute("data-bs-theme", "light");
        setCookie("theme", "light", 365);
      } else {
        document.documentElement.setAttribute("data-bs-theme", "dark");
        setCookie("theme", "dark", 365);
      }
    });


  const theme = getCookie("theme");
  if (theme === "dark") {
      document.documentElement.setAttribute("data-bs-theme", "dark");
    } else {
      document.documentElement.setAttribute("data-bs-theme", "light");
    }

});
