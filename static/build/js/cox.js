$(document).ready(function () {

    // Intercept the form submission
    $('#cox_input_form').submit(function (e) {
        // Prevent the default form submission
        e.preventDefault();

        // Get form data
        var coxInputParameters = {
            HLA_A1: $('#HLA_A1').val(),
            HLA_A2: $('#HLA_A2').val(),
            HLA_B1: $('#HLA_B1').val(),
            HLA_B2: $('#HLA_B2').val(),
            HLA_DR1: $('#HLA_DR1').val(),
            HLA_DR2: $('#HLA_DR2').val(),
            age_at_list_registration: $('#age_at_list_registration').val(),
            age_cat: $('#age_cat').val(),
            blood_gp: $('#blood_gp').val(),
            cPRA: $('#cPRA').val(),
            cPRA_cat: $('#cPRA_cat').val(),
            dialysis_duration: $('#dialysis_duration').val(),
            duration: $('#duration').val(),
            gender: $('#gender').val(),
            gestation: $('#gestation').val(),
            if_transplanted: $('#if_transplanted').val(),
            log_time_on_Dialysis: $('#log_time_on_Dialysis').val(),
            number_prior_transplant: $('#number_prior_transplant').val(),
            prior_transplant: $('#prior_transplant').val(),
            underlying_disease: $('#underlying_disease').val()
        };

        // Make a POST request
        $.post('/cox', coxInputParameters, function (response, status) {
            $('#cox_prediction').text(`Probable wait-time: ${response} months`).hide().show('normal');
        });

    });

});