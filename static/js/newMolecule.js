document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();  

    let formData = new FormData();  
    const molFile = document.getElementById("molFile").files[0];
    const smiles = document.getElementById("smilesInput").value;

    if (molFile) {
        formData.append("molFile", molFile);
    }

    if (smiles) {
        formData.append("smiles", smiles);
    }

    fetch("/add", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("predictionResult").innerHTML = data;
    })
    .catch(error => console.error("Error:", error));
});
