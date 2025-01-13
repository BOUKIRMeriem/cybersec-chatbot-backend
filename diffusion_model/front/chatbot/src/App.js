import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

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
            // Create a FormData object to send the file
            const formData = new FormData();
            formData.append('file', file);

            // Send the FormData to the backend
            const response = await axios.post('http://127.0.0.1:5000/predict', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', // Set correct content type
                },
            });

            // Set the result from the response
            setResult(response.data);
        } catch (err) {
            setError('Error while uploading the file or predicting.');
        }
    };

    return (
        <div className="chatbot-container">
            <h2 className="chatbot-header">Chatbot Attack Detection</h2>

            <div className="chat-conversation">
                <div className="chat-message user">
                    <img src="/user.png" alt="User" />
                    <p>Hello, can you analyze this file?</p>
                </div>
                <div className="chat-message bot">
                    <img src="chatbot.png" alt="Bot" />
                    <p>Sure! Please upload your file to get started.</p>
                </div>
            </div>

            <div className="file-upload-container">
                <input type="file" accept=".json" onChange={handleFileChange} />
                <button className="analyze-button" onClick={handleSubmit}>Analyze</button>
            </div>

            {result && (
                <div className="result-container">
                    <h3>Prediction:</h3>
                    <p><strong>Predicted Value:</strong> {result.predicted_value}</p>
                    <p><strong>Predicted Class:</strong> {result.predicted_class === 1 ? 'Attack' : 'Normal'}</p>
                </div>
            )}

            {error && <p className="error-message">{error}</p>}
        </div>
    );
};

export default FileUpload;
