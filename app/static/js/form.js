document.addEventListener("DOMContentLoaded", () => {
    let form = document.getElementById('form');
    let btnSubmit = document.getElementById('submit');

    form.onsubmit = async (event) => {
        event.preventDefault();
        try {
            btnSubmit.disabled = true;
            let payload = {};
            let formdata = new FormData(form);

            for (let tuple of formdata.entries()) payload[tuple[0]] = tuple[1];

            $.ajax({
                url: '/property',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                success: data => {
                    console.log(data);
                    btnSubmit.disabled = false;
                    window.location.href = '/list';
                },
                error: error => {
                    console.log(error);
                    btnSubmit.disabled = false;
                },
                data: JSON.stringify(payload)
            });

        } catch (error) {
            console.log(error);
        }
    }

});