function buildPrompt(task, already_done, workspace_content, prompt_history, current_service_url, service_history) {
    const base_prompt = `
## Visited Services History:
${service_history}
----- End of Service History -----
## TASK HISTORY:
${prompt_history}
----- End of TASK History -----
## ACTIONS HISTORY:
${already_done}
----- End of Actions History -----
## TEXTUAL CONTENT OF CURRENT WORKSPACE:
${workspace_content}
----- End of Workspace Content -----
## Current Service URL: ${current_service_url}
## YOUR CURRENT OBJECTIVE: ${task}
    `;
    return base_prompt;
}

function extractFunctionDetails(s) {
    const pattern = /(\w+)\((.*)\)/;
    const match = s.match(pattern);
    if (match) {
        const function_name = match[1];
        const argument_string = match[2];
        const args = argument_string ? argument_string.split(',').map(arg => cleanArguments(arg)) : [];
        return [function_name, args];
    }
    return [null, null];
}

function cleanArguments(argument) {
    return argument.replace(/['"]/g, '').replace(/\\n/g, '\n').trim();
}

export { buildPrompt, extractFunctionDetails, cleanArguments };