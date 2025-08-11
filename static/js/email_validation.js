let counter = 60
const resendButton = document.getElementById('resend-button')
resendButton.value = `Resend Email in (${counter})s`
resendButton.disabled = counter > 0

const timer = setInterval(() => {
  counter--
  resendButton.value = `Resend Email in (${counter})s`
  resendButton.disabled = counter > 0
  if (counter <= 0) {
    resendButton.value = 'Resend Email'
    clearInterval(timer)
  }
}, 1000)