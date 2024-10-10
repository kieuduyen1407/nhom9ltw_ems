const formChange = document.querySelector('[form-change]')
if (formChange) {
  const btnChange = document.querySelector('[btn-change]')
  const inputPosition = formChange.querySelector('input[name="position"]')
  const inputDepartment = formChange.querySelector('input[name="department"]')
  const selectPosition = document.querySelector('#select-position')
  const selectDepartment = document.querySelector('#select-department')
  let valuePosition = selectPosition.value;  
  let valueDepartment = selectDepartment.value;
  selectPosition.addEventListener('change', () => {
    valuePosition = selectPosition.value
  })
  selectDepartment.addEventListener('change', () => {
    valueDepartment = selectDepartment.value
  })
  btnChange.addEventListener('click', () => {
    if (valuePosition===inputPosition.value && valueDepartment===inputDepartment.value) {
      alert('Chưa có chỉnh sửa gì')
    } else {
      const confirmChange = confirm('Xác nhận chỉnh sửa?')
      if (confirmChange) {
        inputPosition.value = valuePosition
        inputDepartment.value = valueDepartment
        formChange.submit()
      }
    }
  })
}