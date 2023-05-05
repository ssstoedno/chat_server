const urlParams = new URLSearchParams(window.location.search);
const logoutParam = urlParams.get('logout');
if (logoutParam === 'true') {
    function showLogoutBanner() {
        const logoutBanner = document.querySelector('#banner');
        logoutBanner.textContent = 'You have been logged out.';
        logoutBanner.appendChild(logoutBanner);
      }


  showLogoutBanner();
}

const wrong_passParam=urlParams.get('wrong_pass')
if (wrong_passParam === 'true') {
  function showWrongPassBanner() {
      const wrongpassBanner= document.querySelector('#banner');
      wrongpassBanner.textContent = 'Wrong password !';
      wrongpassBanner.appendChild(wrongpassBanner);
    }


showWrongPassBanner();
}

const already_loggedParam=urlParams.get('already_logged')
if (already_loggedParam === 'true') {
  function showAlreadyLoggedBanner() {
      const alreadyloggedBanner= document.querySelector('#banner');
      alreadyloggedBanner.textContent = 'Already Logged !';
      alreadyloggedBanner.appendChild(alreadyloggedBanner);
    }


    showAlreadyLoggedBanner();
}

const no_charParam=urlParams.get('no_char')
if (no_charParam === 'true') {
  function noCharBanner() {
      const nocharBanner= document.querySelector('#banner');
      nocharBanner.textContent = 'At least one character for password and username !';
      nocharBanner.appendChild(nocharBanner);
    }


    noCharBanner();
}