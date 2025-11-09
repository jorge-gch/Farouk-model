const input = document.getElementById('words');
const slider = document.getElementById('suggestions');
const suggestionsDiv = document.getElementById('suggestionstext');
const inputRangeLabel = document.getElementById('inputrange');


inputRangeLabel.textContent = `Numero de sugerencias: ${slider.value}`;
slider.addEventListener('input', () => {
    input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
    inputRangeLabel.textContent = `Numero de sugerencias: ${slider.value}`;
});

async function downloadPDF() {
    console.log("imprimiendo");

    try {
        const response = await fetch('/generate_PDF', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "status":"ok",
            })
        });

        const data = await response.json();
        console.log("Respuesta:", data);
        const link = document.createElement('a');
        const url = "/static/images/pdf_graph.pdf";
        link.href = url;
        link.download = "PDF-GRAFO.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Error:', error);
    }
}

input.addEventListener('keyup', async () => {
    const text = input.value.trim();

    // avoid null messages
    if (!text) {
        suggestionsDiv.innerHTML = '';
        return;
    }

    try {
        const response = await fetch('/update_text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text , "suggestions": slider.value})
        });

        const data = await response.json();
        console.log('prediction:', data);
        suggestionsDiv.innerHTML = '';
        var count = 0;
        if (data.data && Array.isArray(data.data)) {
            data.data.forEach(suggestion => {
                if (count < Number(slider.value)){
                    count = count+1;
                    const button = document.createElement('button');
                    button.textContent = suggestion;
                    button.className = 'flex px-4 py-2 bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 transition-colors duration-200 font-medium';
                    button.addEventListener('click', () => {
                        input.value += " "+suggestion[0].trim();
                        input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
                        input.focus();
                    });
                    suggestionsDiv.appendChild(button);
                }else{
                    return;
                }
            });
            const image = document.getElementById('image');
            const date=new Date().getTime();
            image.src = '/static/images/candidates_graph.png?t='+date;

        }
    } catch (error) {
        console.error('Error:', error);
    }
});
