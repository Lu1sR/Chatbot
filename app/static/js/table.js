document.addEventListener('DOMContentLoaded', async () => {

    $('[data-toggle="tooltip"]').tooltip();

    let btnRetrain = document.getElementById('btnRetrain');
    let properties = [];

    let modal = $('#modal');
    let modalMsg = $('#modal-body-msg');

    btnRetrain.onclick = () => callRetrain();

    function callRetrain() {
        btnRetrain.disabled = true;
        $.ajax({
            url: `/create_model`,
            type: 'GET',
            success: () => {
                btnRetrain.disabled = false;
                modalMsg.text('Chatbot re entrnado exitosamente');
                modal.modal('show');
            },
            error: (error) => {
                console.log(error);
                btnRetrain.disabled = false;
                modalMsg.text('Error al re entrenar el chatbot');
                modal.modal('show');
            }
        });
    }

    function removeItem(index, id) {
        $.ajax({
            url: `/property/${id}`,
            type: 'DELETE',
            success: (result) => {
                properties.splice(index, 1);
                buildPropertiesTable();
            },
            error: (error) => {
                console.log(error);
            }
        });
    }

    async function loadData() {
        try {
            let response = await fetch('/properties');
            properties = await response.json();
        } catch (error) {
            console.log(error);
        }
    }

    function buildPropertiesTable() {
        let tbody = document.getElementById('tbody');
        tbody.innerHTML = '';

        if (properties.length > 0) {
            properties.forEach((element, index) => {
                let tr = document.createElement('tr');
                tr.classList.add('tr-shadow');

                let tdType = document.createElement('td');
                let tdContract = document.createElement('td');
                let tdLocation = document.createElement('td');
                let tdDescription = document.createElement('td');
                let tdPrince = document.createElement('td');

                let tdActions = document.createElement('td');
                let div = document.createElement('div');
                div.classList.add('table-data-feature');

                // let buttonEdit = document.createElement('button');
                // buttonEdit.classList.add('item');
                // buttonEdit.title = 'Editar';

                let buttonDelete = document.createElement('button');
                buttonDelete.classList.add('item');
                buttonDelete.title = 'Eliminar';

                buttonDelete.onclick = () => removeItem(index, element.id);

                // let iEdit = document.createElement('i');
                // iEdit.classList.add('zmdi');
                // iEdit.classList.add('zmdi-edit');

                let iDelete = document.createElement('i');
                iDelete.classList.add('zmdi');
                iDelete.classList.add('zmdi-delete');

                // buttonEdit.appendChild(iEdit);
                buttonDelete.appendChild(iDelete);

                // div.appendChild(buttonEdit);
                div.appendChild(buttonDelete);

                tdActions.appendChild(div);

                tdType.textContent = element.type;
                tdContract.textContent = element.contract;
                tdLocation.textContent = element.location;
                tdDescription.textContent = element.description;
                tdPrince.textContent = `$ ${element.price}`;

                tr.appendChild(tdType);
                tr.appendChild(tdContract);
                tr.appendChild(tdLocation);
                tr.appendChild(tdDescription);
                tr.appendChild(tdPrince);
                tr.appendChild(tdActions);

                tbody.appendChild(tr);

                let trSpace = document.createElement('tr');
                trSpace.classList.add('spacer');

                tbody.appendChild(trSpace);
            });
        } else {
            let tableContainer = document.getElementById('table-container');
            tableContainer.innerHTML = '';
            let header = document.createElement('h1');
            header.textContent = 'No hay infomacion en la BD';
            tableContainer.appendChild(header);
        }
    }

    await loadData();
    buildPropertiesTable();

});