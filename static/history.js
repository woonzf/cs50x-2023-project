document.addEventListener('DOMContentLoaded', function() {

    /* Month selection and filter button enabled if year is selected */
    let year = document.getElementById('year');
    year.addEventListener('click', function() {
        if (year.value != "") {
            document.getElementById('month').disabled = false;
            document.getElementById('filter').disabled = false;
        }
    });
});
