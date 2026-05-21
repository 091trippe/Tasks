const API_URL = "http://localhost:5000/tasks";

async function loadTasks() {

    const response = await fetch(API_URL);

    const tasks = await response.json();

    const taskList = document.getElementById("taskList");

    taskList.innerHTML = "";

    tasks.forEach(task => {

        const li = document.createElement("li");

        li.innerHTML = `
            <span class="${task.done ? 'done' : ''}">
                ${task.title}
            </span>

            <div class="actions">

                <button
                    class="complete-btn"
                    onclick="toggleTask(${task.id}, ${!task.done})">

                    ${task.done ? '↩' : '✔'}

                </button>

                <button
                    class="delete-btn"
                    onclick="deleteTask(${task.id})">

                    ✖

                </button>

            </div>
        `;

        taskList.appendChild(li);
    });
}

async function addTask() {

    const input = document.getElementById("taskInput");

    if (!input.value.trim()) {
        return;
    }

    await fetch(API_URL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: input.value
        })
    });

    input.value = "";

    loadTasks();
}

async function toggleTask(id, done) {

    await fetch(`${API_URL}/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            done: done
        })
    });

    loadTasks();
}

async function deleteTask(id) {

    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}

loadTasks();
