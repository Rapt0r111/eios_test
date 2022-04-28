 document.addEventListener('click', (event)=>{
        if (event.target.className == 'delete-form') {
            console.log(event.target.closest('.ingredient-form').style.display = 'none')
        }
        if (event.target.id == 'add-more') {
            add_new_form(event)
        }

    })
    function delete_row(el){
        console.log(el.closest('.ingredient-form').style.display = 'none')
    }
    function add_new_form(event) {
        console.log(event)
        if (event) {
            event.preventDefault()
        }
        const totalNewForms = document.getElementById('id_files_set-TOTAL_FORMS')
        const currentIngredientForms = document.getElementsByClassName('ingredient-form')
        const currentFormCount = currentIngredientForms.length // + 1
        const formCopyTarget = document.getElementById('ingredient-form-list')
        const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
        copyEmptyFormEl.setAttribute('class', 'ingredient-form')
        copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
        const regex = new RegExp('__prefix__', 'g')
        copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
        totalNewForms.setAttribute('value', currentFormCount + 1)
        formCopyTarget.append(copyEmptyFormEl)
    }