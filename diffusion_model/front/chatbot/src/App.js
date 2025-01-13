import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Make sure to use the updated CSS

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setResult(null); // Reset the result when a new file is uploaded
        setError(null);  // Reset errors
    };

    const handleSubmit = async () => {
        if (!file) {
            alert('Please upload a file first.');
            return;
        }

        try {
            // Read the file content as JSON
            const fileContent = await file.text();
            const parsedContent = JSON.parse(fileContent); // Parse the JSON content of the file

            // Send the parsed JSON content to the backend
            const response = await axios.post('http://127.0.0.1:5000/predict', {
                features: parsedContent.features, // Ensure the JSON file has a 'features' key
            });

            // Set the result from the response
            setResult(response.data);
        } catch (err) {
            setError('Error while processing the file or predicting.');
        }
    };

    return (
        <div className="chatbot-container">
            <h2 className="chatbot-header">Chatbot Attack Detection</h2>

            <div className="chat-conversation">
                {/* User prompt */}
                <div className="chat-message user">
                    <img src="/user.png" alt="User" />
                    <p>Hello, can you analyze this file?</p>
                </div>

                {/* Bot reply */}
                <div className="chat-message bot">
                    <img src="chatbot.png" alt="Bot" />
                    <p>Sure! Please upload your file to get started.</p>
                </div>

                {/* If a file is uploaded, simulate the bot processing */}
                {file && (
                    <div className="chat-message bot">
                        <img src="chatbot.png" alt="Bot" />
                        <p>Processing your file... Click "Analyze" to continue.</p>
                    </div>
                )}
            </div>

            {/* File upload and analyze button */}
            <div className="file-upload-container">
                <label htmlFor="file-upload" className="label-upload">
                    Upload File
                </label>
                <input
                    id="file-upload"
                    type="file"
                    accept=".json"
                    onChange={handleFileChange}
                />
                <button className="analyze-button" onClick={handleSubmit}>
                    Analyze
                </button>
            </div>

            {/* Display results */}
            {result && (
                <div
                    className={`result-container ${
                        result.predicted_class === 1 ? 'malicious' : 'normal'
                    }`}
                >
                    <h3>Prediction:</h3>
                    <p>
                        <strong>Status:</strong>{' '}
                        {result.predicted_class === 1 ? 'Malicious' : 'Normal'}
                    </p>
                    <p>
                        <strong>Predicted Value:</strong> {result.predicted_value}
                    </p>
                </div>
            )}

            {/* Display error message */}
            {error && <p className="error-message">{error}</p>}
        </div>
    );
};

export default FileUpload;
