const input = document.getElementById('words');

input.addEventListener('keyup', async () => {
    const text = input.value;

    await fetch('/update_text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
});
