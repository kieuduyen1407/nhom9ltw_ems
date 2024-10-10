const formCheck = document.querySelector('form')
const checkIO = formCheck.querySelector('[btn-check]')
const requiredLatitude = 16.0473935
const requiredLongitude = 108.2368985
const tolerance = 0.01

if (checkIO) {
  checkIO.addEventListener('click', () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const {latitude, longitude} = position.coords
        if (Math.abs(latitude - requiredLatitude) <= tolerance && Math.abs(longitude - requiredLongitude) <= tolerance) {
          const inputHidden = formCheck.querySelector('[hidden]')
          const buttonValue = checkIO.value 
          inputHidden.value = buttonValue
          formCheck.submit()
        } else {
          const inputHidden = formCheck.querySelector('[hidden]')
          const buttonValue = checkIO.value 
          inputHidden.value = buttonValue
          formCheck.submit()
        }
      }, (err) => {
        alert('Vui lòng cho phép vị trí để kiểm tra')
      })
    }
  })
}
