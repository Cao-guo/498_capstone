import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

function App() {
  // I use this state to store the uploaded file name
  const [fileName, setFileName] = useState('');

  // This state controls which page is currently visible (home, upload, or todo)
  const [activePage, setActivePage] = useState('home');

  // This holds the list of to-do tasks for the task manager section
  const [tasks, setTasks] = useState([]);

  // This function handles file uploads (simulated for this project)
  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      alert(`File "${file.name}" uploaded (simulated).`);
    }
  };

  // This function adds a new task to the task list
  const handleAddTask = (e) => {
    e.preventDefault();
    const taskInput = document.getElementById('task-input');
    const newTask = taskInput.value.trim();
    if (newTask) {
      setTasks([...tasks, newTask]);
      taskInput.value = '';
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Smart Retail Analytics</h1>
        <nav>
          <button onClick={() => setActivePage('home')}>Home</button>
          <button onClick={() => setActivePage('upload')}>Upload</button>
          <button onClick={() => setActivePage('todo')}>Tasks</button>
        </nav>
      </header>

      <main>
        {/* Home Page */}
        {activePage === 'home' && (
          <section>
            <h2>Welcome to Smart Retail Analytics</h2>
            <p>This is a React-based application to help small retailers make data-driven decisions.</p>
            <ul>
              <li>📊 Upload your CSV sales data</li>
              <li>📈 Analyze sales trends</li>
              <li>🧠 Make smarter business decisions</li>
            </ul>
          </section>
        )}

        {/* Upload Page */}
        {activePage === 'upload' && (
          <section>
            <h2>Upload Sales Data (Simulation)</h2>
            <input type="file" accept=".csv" onChange={handleUpload} />
            {fileName && <p>Uploaded file: {fileName}</p>}
          </section>
        )}

        {/* Task List Page */}
        {activePage === 'todo' && (
          <section>
            <h2>Task List</h2>
            <form onSubmit={handleAddTask}>
              <input id="task-input" type="text" placeholder="Enter a task" />
              <button type="submit">Add</button>
            </form>
            <ul>
              {tasks.map((task, index) => (
                <li key={index}>✅ {task}</li>
              ))}
            </ul>
          </section>
        )}
      </main>

      <footer>
        <p>&copy; 2025 Smart Retail Analytics - Built with React</p>
      </footer>
    </div>
  );
}

export default App;
