 let num = 1;

    function addInput(){
        num++;
        let newInput = '<div class="newIngredients"><div class="addingr"><label for="quantity"></label>\n' +
        '<input type="text" class="form-control" style="width: 80px" name="quantity" ' +
        'id="quantity1'+num+'" placeholder="Määrä"><small id="quantity" class="form-text text-muted">Esim. 1, 0.5, 2..</small></div> ' +
        '<div class="addingr"><label for="measuring_unit"></label>'+
        '<input type="text" class="form-control" style="width: 100px" name="measuring_unit" id="measuring_unit1'+num+'" ' +
         'placeholder="Yksikkö"><small id="quantity" class="form-text text-muted">Esim. dl, tl, rkl...</small></div>' +
        '<div class="addingr"><label for="ingredient"></label>'+
        '<input type="text" class="form-control" name="ingredient" id="ingredient1'+num+'" ' +
         'placeholder="Ainesosa"><small id="quantity" class="form-text text-muted">Sanomattakin selvää - ainesosan nimi tähän</small></div></div><br>' ;
        const more = document.getElementById('more');
        more.insertAdjacentHTML("beforebegin" ,newInput);

        }