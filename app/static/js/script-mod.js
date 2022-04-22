    let one_ingr = {};
    let updated_ingredients = [];
    let num = 1;

    window.onload=function() {
    let listener = document.getElementById('addIngredient');
    if(listener) {
        listener.addEventListener('click',updateIngredients);
        listener.addEventListener('click',addInput);
    }

    let saveIngr = document.getElementById('saveIngredients');
    if (saveIngr) {
        saveIngr.addEventListener('click',updateIngredients);
    }

    let submitModified = document.getElementById('mod_submit');
    if (submitModified) {
        submitModified.addEventListener('click', saveUpdatedRecipe);
    }

    function updateIngredients() {
        /* Tästä puuttuu mahdollisuus lisätä monta ainesosaa, koska yksi lisätty aina ylikirjoittaa
        * sen entisen. Homma työn alla. */
        let mod_quantity = document.querySelector('[id*="mod_quantity"]').value;
        let mod_measuring_unit = document.querySelector('[id*="mod_measuring_unit"]').value;
        let mod_ingredient = document.querySelector('[id*="mod_ingredient"]').value;

        one_ingr = {
                    'quantity': mod_quantity,
                    'measuring_unit': mod_measuring_unit,
                    'ingredient': mod_ingredient
        };


        updated_ingredients.push(one_ingr);
        console.log(one_ingr);
        console.log(updated_ingredients);

        const ingrs = JSON.stringify(updated_ingredients)

        axios.put('/', ingrs);

        }

    function removeIngredient () {
       /* Nappia painamalla pitää voida poistaa ainesosa.
       * Poistetaan siis kentät. Jos on ehditty tallentaa se jo ainesosiin niin se pitää myös
       * poistaa niistä. */
    }

    function addInput(){
        num++;
        let newInput = '<label for="mod_quantity"></label>\n' +
        '<input type="text" class="form-control" name="quantity" ' +
        'id="mod_quantity1'+num+'" placeholder="Määrä" required>' +
        '<label for="mod_measuring_unit"></label>'+
        '<input type="text" class="form-control" name="measuring_unit" id="mod_measuring_unit1'+num+'" placeholder="Yksikkö"required>' +
        '<label for="mod_ingredient"></label>'+
        '<input type="text" class="form-control" name="ingredient" id="mod_ingredient1'+num+'" placeholder="Ainesosa" required><br>';
        document.getElementById('moreIngredients').innerHTML += newInput;
    }


    function saveUpdatedRecipe() {
        let form = document.getElementById("recipe_form")

        let data = new FormData(form);

        axios({
            method: "patch",
            url: "/",
            data: data,
            header: {
                "Content-Type": "application/json"
            }
        })
            .then(function (response) {
                console.log("Response, data = " + response.data)

                if (response.status === 200) {
                    form.reset()
                    window.location = "/";
                }
            })
            .catch(function (response) {
                console.log(response);
            })
    }
}

/* let form = document.getElementById("recipe_form")

    form.addEventListener("submit", function(e) {
        e.preventDefault();

        let data = new FormData(form);

        axios.put('/', data)
        .then(function(response) {
            console.log("Response, data = " + response.data)

            if (response.status === 200) {
                form.reset()
                window.location = "/";
            }
        })
        .catch(function (response) {
            console.log(response);
        })
    })

    function confirm_alert() {
        return confirm("Resepti päivitetty!")
    }*/