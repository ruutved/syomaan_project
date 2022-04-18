    let one_ingredient = {};
    let ingredients = [];
    let num = 1;

    window.onload=function() {
    let listener = document.getElementById('add');
    if(listener) {
        listener.addEventListener('click',saveInput);
        listener.addEventListener('click',addInput);
    }

    let submitter = document.getElementById('save');
    if (submitter) {
        submitter.addEventListener('click',saveInput);
    }}

    function saveInput() {
        if (num === 1) {
            let quantity = document.getElementById('quantity1').value;
            let measuring_unit = document.getElementById('measuring_unit1').value;
            let ingredient = document.getElementById('ingredient1').value;

            one_ingredient = {
                    'quantity': quantity,
                    'measuring_unit': measuring_unit,
                    'ingredient': ingredient
            };
        }
        else {
            console.log('quantity'+num);
            let a_quantity = document.getElementById('quantity1'+num).value;
            let a_measuring_unit = document.getElementById('measuring_unit1'+num).value;
            let a_ingredient = document.getElementById('ingredient1'+num).value;

            one_ingredient = {
                    'quantity': a_quantity,
                    'measuring_unit': a_measuring_unit,
                    'ingredient': a_ingredient
            };
        }


    ingredients.push(one_ingredient);
    console.log(one_ingredient);
    console.log(ingredients);

    const ingrs = JSON.stringify(ingredients)

    axios.put('/add_recipe', ingrs)

    document.getElementById("inputInstructions").focus();

    }


    /* Tallenna viimeinen ainesosa painamalla Submit-nappia niin, ettei
    * ole tarpeen painaa Lisää ainesosa -nappia. Eli saveInput pitää olla myös
    * submit-napissa. Sen lisäksi remove-nappi tähän, ja selvitä miten
    * viedä ingredients-lista pythonin puolelle. */

    function addInput(){
        num++;
        let newInput = '<label for="quantity"></label>\n' +
        '<input type="text" class="form-control" name="quantity" ' +
        'id="quantity1'+num+'" placeholder="Määrä" required>' +
        '<label for="measuring_unit"></label>'+
        '<input type="text" class="form-control" name="measuring_unit" id="measuring_unit1'+num+'" placeholder="Yksikkö"required>' +
        '<label for="ingredient"></label>'+
        '<input type="text" class="form-control" name="ingredient" id="ingredient1'+num+'" placeholder="Ainesosa" required><br>';
        document.getElementById('moreIngredients').innerHTML += newInput;
    }