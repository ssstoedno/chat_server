const urlParams = new URLSearchParams(window.location.search);
param = urlParams.get('logout');
if (param === 'true') {
    function showLogoutBanner() {
        const logoutBanner = document.querySelector('#banner');
        logoutBanner.textContent = 'You have been logged out.';
        logoutBanner.appendChild(logoutBanner);
      }


  showLogoutBanner();
}

param=urlParams.get('wrong_pass')
if (param === 'true') {
  function showWrongPassBanner() {
      const wrongpassBanner= document.querySelector('#banner');
      wrongpassBanner.textContent = 'Wrong password !';
      wrongpassBanner.appendChild(wrongpassBanner);
    }


showWrongPassBanner();
}

param=urlParams.get('already_logged')
if (param === 'true') {
  function showAlreadyLoggedBanner() {
      const alreadyloggedBanner= document.querySelector('#banner');
      alreadyloggedBanner.textContent = 'Already Logged !';
      alreadyloggedBanner.appendChild(alreadyloggedBanner);
    }


    showAlreadyLoggedBanner();
}

param=urlParams.get('no_char')
if (param === 'true') {
  function noCharBanner() {
      const nocharBanner= document.querySelector('#banner');
      nocharBanner.textContent = 'At least one character for password and username !';
      nocharBanner.appendChild(nocharBanner);
    }


    noCharBanner();
}