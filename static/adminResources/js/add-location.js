function addSelectField() {
  const container = document.getElementById('container');
  const newSelectField = document.createElement('div');
  newSelectField.classList.add('select-field');
  newSelectField.innerHTML = `
    <select name="dynamicDropdown[]">
      <option value="option1">Option 1</option>
      <option value="option2">Option 2</option>
      <option value="option3">Option 3</option>
    </select>
    <button type="button" onclick="removeSelectField(this)">Remove</button>
  `;
  container.appendChild(newSelectField);
}

function removeSelectField(button) {
  const container = document.getElementById('container');
  container.removeChild(button.parentNode);
}