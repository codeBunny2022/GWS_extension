import { getAuthToken, revokeAuthToken } from './oauth.js';
import { buildPrompt } from './utils.js';

document.getElementById('submit').addEventListener('click', async () => {
    const task = document.getElementById('task').value;
    const responseElement = document.getElementById('response');

    const token = await getAuthToken();

    // Dummy values for required fields, replace with actual data as needed
    const data = {
        task: task,
        already_done: '',
        workspace_content: '',
        prompt_history: '',
        current_service_url: 'http://example.com',
        service_history: '',
        token: token
    };

    const prompt = buildPrompt(data.task, data.already_done, data.workspace_content, data.prompt_history, data.current_service_url, data.service_history);

    try {
        const response = await fetch('YOUR_FLASK_SERVER_URL', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ...data, prompt }),
        });
        const result = await response.json();
        responseElement.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        responseElement.textContent = 'Error: ' + error.message;
    }
});

document.getElementById('signout').addEventListener('click', async () => {
    await revokeAuthToken();
    alert('Signed out');
});