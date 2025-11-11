const input = document.getElementById('words');
const slider = document.getElementById('suggestions');
const suggestionsDiv = document.getElementById('suggestionstext');
const inputRangeLabel = document.getElementById('inputrange');
var predictions = {data: []};


inputRangeLabel.textContent = `Numero de sugerencias: ${slider.value}`;
slider.addEventListener('input', () => {
    input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
    inputRangeLabel.textContent = `Numero de sugerencias: ${slider.value}`;
});

async function downloadPDF() {
    console.log("imprimiendo");

    try {
        const text = input.value;
        const response = await fetch('/generate_PDF', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "suggestions": slider.value,
                "text": text,
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

// autocomplete with tab
input.addEventListener('keydown', function (event) {
    if (event.key === 'Tab') {
        const firstButton = suggestionsDiv.querySelector('button');
        if (firstButton) {
            event.preventDefault();
            firstButton.click();
        }
    }
});

function fillSuggestions(data) {
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
                        if (input.value.endsWith(" ")) {
                            input.value += suggestion[0].trim()+" ";
                        }else{
                            const palabras = input.value.split(" ");
                            palabras[palabras.length - 1] = suggestion[0].trim();
                            input.value = palabras.join(" ");
                            input.value += " ";
                        }
                        
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
}

input.addEventListener('keyup', async () => {
    const text = input.value;
    const espacioFinal = text.endsWith(" ");
    console.log('Input text:', text);
    // avoid null messages
    if (!text) {
        suggestionsDiv.innerHTML = '';
        return;
    }
    if (espacioFinal){

        
        try {
            const response = await fetch('/update_text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text , "suggestions": slider.value})
            });

            const data = await response.json();
            console.log('prediction:', data);
            predictions=data;
            suggestionsDiv.innerHTML = '';
            
            fillSuggestions(data)
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        // 🟣 Caso: el usuario está escribiendo la última palabra (sin espacio al final)
        suggestionsDiv.innerHTML = '';

        // Extraer la última palabra incompleta
        const palabras = text.split(" ");
        const ultima = palabras[palabras.length - 1].toLowerCase();

        // Evitar filtrar si no hay datos previos
        if (!predictions || !predictions.data) return;

        
        // Filtrar las sugerencias que empiecen con esas letras usando forEach
        let coincidencias = [];
        console.log(predictions.data);
        predictions.data.forEach(s => {
            if (s[0].toLowerCase().startsWith(ultima)) {
                coincidencias.push(s);
            }
        });

        // Mostrar solo algunas sugerencias (ej. hasta el valor del slider)
        const dataFiltrada = { data: coincidencias.slice(0, Number(slider.value)) };
        fillSuggestions(dataFiltrada);

            }
});
