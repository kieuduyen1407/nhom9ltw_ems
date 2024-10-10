const btnLeave = document.querySelectorAll('[btn-leave]')
if (btnLeave.length >0) {
  btnLeave.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmLeave = confirm('Xác nhận cho thằng này nghỉ?')
      if (confirmLeave) {
        const formLeave = document.querySelector('[form-leave]')
        const inputLeave = formLeave.querySelector('[hidden]')
        inputLeave.value = btn.value
        formLeave.submit()
      }
    })
  })
}