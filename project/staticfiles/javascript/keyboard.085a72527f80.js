document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input')
    document.addEventListener('keydown', (event) => {
        const regex = new RegExp("^[a-zA-Z]$")
        const key = event.key
        const inputsArray = Array.from(inputs)
        if (regex.test(key)) {
            const input = inputsArray.find(input => input.name.includes('attempts_') && input.value === '')
            if (!input) return
            input.focus()
            input.value = key
        } else if (key === "Backspace") {
            const input = Object.assign([], inputsArray).reverse().find(input => input.name.includes('attempts_') && input.value !== '')
            input.focus()
            input.value = ""
        } else if (key === "Enter") {
            return
        } else {
            event.preventDefault()
        }
    })
})