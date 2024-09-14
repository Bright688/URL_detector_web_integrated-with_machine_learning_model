<!DOCTYPE html>
<html lang="en">

<h1>Flask Website with Machine Learning Model for URL Classification</h1>

<p>This project is a web-based application built using Flask that allows users to classify URLs as legitimate or phishing using a machine learning model.</p>

<div class="section">
    <h2>Project Overview</h2>
    <p>The Flask application provides a user interface where users can enter a URL to classify whether it is legitimate or phishing. The classification is performed using a pre-trained machine learning model, and results are displayed dynamically on the page.</p>
</div>

<div class="section">
    <h2>Features</h2>
    <ul>
        <li>URL input form for classification.</li>
        <li>Loading spinner shown while processing the URL.</li>
        <li>Machine learning model to classify URLs based on extracted features.</li>
        <li>Dynamic display of classification results on the same page.</li>
    </ul>
</div>

<div class="section">
    <h2>Installation</h2>
    <p>To set up the project, follow these steps:</p>
    <ol>
        <li>Clone the repository or download the source code.</li>
        <li>Navigate to the project directory:</li>
        <pre><code>cd flask-url-classifier</code></pre>
        <li>Create a virtual environment (optional but recommended):</li>
        <pre><code>python3 -m venv venv</code></pre>
        <li>Activate the virtual environment:</li>
        <ul>
            <li>On Windows:</li>
            <pre><code>venv\Scripts\activate</code></pre>
            <li>On macOS/Linux:</li>
            <pre><code>source venv/bin/activate</code></pre>
        </ul>
        <li>Install the required dependencies:</li>
        <pre><code>pip install -r requirements.txt</code></pre>
        <li>Download the pre-trained machine learning model and scaler files (`model.pkl` and `scaler.pkl`) and place them in the project directory.</li>
        <li>Run the Flask app:</li>
        <pre><code>python app.py</code></pre>
        <li>Open your browser and go to <code>http://127.0.0.1:5000/</code> to access the application.</li>
    </ol>
</div>

<div class="section">
    <h2>Usage</h2>
    <p>Once the application is running, follow these steps to classify a URL:</p>
    <ol>
        <li>Enter a URL in the input field on the homepage.</li>
        <li>Click the "Classify" button to submit the URL.</li>
        <li>The system will process the URL, and a loading spinner will be displayed during this time.</li>
        <li>Once the classification is complete, the result ("Legitimate" or "Phishing") will be displayed below the form.</li>
    </ol>
</div>

<div class="section">
    <h2>Project Structure</h2>
    <p>The project is organized as follows:</p>
    <ul>
        <li><code>app.py</code>: The main Flask application file that handles routes and URL classification.</li>
        <li><code>templates/</code>: Directory containing HTML templates.</li>
        <li><code>static/</code>: Directory for static assets (CSS, JavaScript).</li>
        <li><code>model.pkl</code>: Pre-trained machine learning model for URL classification.</li>
        <li><code>scaler.pkl</code>: Scaler used to normalize the feature data for the model.</li>
        <li><code>requirements.txt</code>: List of required Python packages.</li>
    </ul>
</div>

<div class="section">
    <h2>How the Machine Learning Model Works</h2>
    <p>The machine learning model used in this project is trained to classify URLs based on features such as:</p>
    <ul>
        <li>Length of the URL.</li>
        <li>Presence of an IP address in the URL.</li>
        <li>Use of URL shortening services.</li>
        <li>Number of special characters.</li>
        <li>Domain age and SSL certificate presence.</li>
        <li>HTML content length, number of links, and forms.</li>
    </ul>
    <p>These features are extracted from the URL and passed to the pre-trained model for classification.</p>
</div>

<div class="section">
    <h2>License</h2>
    <p>This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as needed.</p>
</div>

</body>
</html>
