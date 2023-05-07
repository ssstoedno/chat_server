//prevent returning when logged out
function preventBack(){
  const queryParams = new URLSearchParams(window.location.search);
  const active = queryParams.get('active');
  if (active!='true'){
    window.history.forward();
  }
}
setTimeout("preventBack()", 0);
window.onunload=function(){null};

const urlParams = new URLSearchParams(window.location.search);
const no_charParam=urlParams.get('no_char')
if (no_charParam === 'true') {
  function noCharBanner() {
      const nocharBanner= document.querySelector('#banner');
      nocharBanner.classList.add('badge','bg-danger')
      nocharBanner.textContent = 'At least one character !';
      nocharBanner.appendChild(nocharBanner);
    }


    noCharBanner();
}

const sameParam=urlParams.get('same')
if (sameParam === 'true') {
  function sameBanner() {
      const sameBanner= document.querySelector('#banner');
      sameBanner.classList.add('badge','bg-danger')
      sameBanner.textContent = 'Different password !';
      sameBanner.appendChild(sameBanner);
    }


    sameBanner();
}


const successParam=urlParams.get('success')
if (successParam === 'true') {
  function successBanner() {
      const successBanner= document.querySelector('#banner');
      successBanner.classList.add('badge','bg-success')
      successBanner.textContent = 'Success';
      successBanner.appendChild(successBanner);
    }


    successBanner();
}