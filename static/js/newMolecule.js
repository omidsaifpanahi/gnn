document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();  

    event.preventDefault();  

    let formData = new FormData();
    const inputType = $("input[name=input_type]:checked").val();
    const name = $("#name").val();

    formData.append("input_type", inputType);
    formData.append("name", name);

    if (inputType === 'smiles') {
        const smiles = $("#smilesInput").val();
        formData.append("smiles", smiles);
    } else {
        const molFile = $('#molFile')[0].files[0];
        formData.append("mol_file", molFile);
    }


    $.ajax({
        url: "/molecule/add",
        cache: false,
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        dataType: "json",
        success: function (result) {        
            if(result['success'])
            {
                result['data'] = JSON.parse(result['data'])
                $('#result').removeClass('d-none')
                $('#result-prediction').html(result['data']['prediction'])
                $('#result-image').attr("src",result['data']['image']);              
            }
            else
            {
                Swal.fire(data['message'], '', 'info')        
            }
        },
        error: function(xhr, resp, text='error') {
            if( typeof xhr['responseJSON'] !== 'undefined' )
            {
                if( typeof xhr['responseJSON']['message'] !== 'undefined' )
                {
                    text = xhr['responseJSON']['message'];
                }
            }

            Swal.fire({
                width: '50%',
                icon: 'error',
                title: text,
                showCloseButton: true
            });
        }
    });
});
