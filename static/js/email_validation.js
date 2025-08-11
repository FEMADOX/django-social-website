let counter = 60
const resendButton = document.getElementById('resend-button')

const timer = setInterval(() => {
  counter--
  resendButton.innerText = `Resend Email in (${counter})s`
  resendButton.disabled = counter > 0
  if (counter <= 0) {
    resendButton.innerText = 'Resend Email'
    clearInterval(timer)
  }
}, 1000)