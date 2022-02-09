document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input')
    document.addEventListener('keydown', (event) => {
        const regex = new RegExp("^[a-zA-Z]$");
        const key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        const inputsArray = Array.from(inputs)
        if (regex.test(key)) {
            const input = inputsArray.find(input => input.name.includes('char') && input.value === '')
            if (!input) return
            input.focus()
            input.value = key
        } else if (event.key === "Backspace") {
            const input = Object.assign([], inputsArray).reverse().find(input => input.name.includes('char') && input.value !== '')
            input.focus()
            input.value = ""
        }
    })
})