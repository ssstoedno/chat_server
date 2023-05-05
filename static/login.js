const urlParams = new URLSearchParams(window.location.search);
const logoutParam = urlParams.get('logout');
if (logoutParam === 'true') {
    function showLogoutBanner() {
        const logoutBanner = document.querySelector('#logout-banner');
        logoutBanner.textContent = 'You have been logged out.';
        logoutBanner.appendChild(logoutBanner);
      }


  showLogoutBanner();
}