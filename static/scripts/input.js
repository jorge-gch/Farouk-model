const input = document.getElementById('words');
const suggestionsDiv = document.getElementById('suggestions');

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
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        console.log('prediction:', data);
        suggestionsDiv.innerHTML = '';
        if (data.data && Array.isArray(data.data)) {
            data.data.forEach(suggestion => {
                const button = document.createElement('button');
                button.textContent = suggestion;
                button.className = 'px-4 py-2 bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 transition-colors duration-200 font-medium';
                button.addEventListener('click', () => {
                    input.value = suggestion;
                    input.focus();
                });
                suggestionsDiv.appendChild(button);
            });
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
