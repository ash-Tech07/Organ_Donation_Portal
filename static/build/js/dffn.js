$(document).ready(function () {
    Dropzone.options.dffnFormInput = {
        paramName: 'file',
        maxFilesize: 1024,
        dictDefaultMessage: 'Drop the image here or click to upload',
        filesizeBase: 1024, 
        acceptedFiles: 'image/*',
        clickable: true,
        uploadMultiple: false,
        addRemoveLinks: true,
        init: function () {
            this.on('success', function (file, response) {
                $('#prediction').text(response).hide().show('normal');
            });
            this.on('error', function (file, response) {
                $('#prediction').text("Server Error!").hide().show('normal');
            });
            dffnFormInput.on("complete", function(file) {
                dffnFormInput.removeFile(file);
            });
        }
    };

});