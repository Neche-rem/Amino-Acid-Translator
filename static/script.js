async function translateSeq() {
    const fileInput = document.getElementById("file").files[0];

    let response;

    if (fileInput) {
        let formData = new FormData();
        formData.append("file", fileInput);

        response = await fetch("/translate", {
            method: "POST",
            body: formData
        });

    } else {
        const sequence = document.getElementById("sequence").value;

        response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ sequence })
        });
    }

    const data = await response.json();

    document.getElementById("result").innerText =
        "Amino Acid Chain: " + data.protein;
}
