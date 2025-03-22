import { useState } from "react";

function App() {
  const [fileContent, setFileContent] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "text/plain") {
      setFileName(file.name); // Capture the file name
      const reader = new FileReader();
      reader.onload = (e) => {
        setFileContent(e.target?.result as string);
      };
      reader.readAsText(file);
    } else {
      alert("Please upload a valid text file.");
    }
  };

  const handleSendToServer = async () => {
    if (!fileContent || !fileName) {
      alert("No file content or filename to send!");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: fileContent, file_name: fileName }),
      });

      if (response.ok) {
        const result = await response.json();
        alert(`File data sent successfully! Message: ${result.message}`);
      } else {
        const error = await response.json();
        alert(`Failed to send data. Error: ${error.error}`);
      }
    } catch (error) {
      console.error("Error sending file:", error);
      alert("Error sending file.");
    }
  };

  return (
    <div>
      <h1>Upload Text File</h1>
      <input type="file" accept=".txt" onChange={handleFileUpload} />
      {fileName && <p>File Name: {fileName}</p>}
      <button onClick={handleSendToServer} disabled={!fileContent}>
        Send to Server
      </button>
    </div>
  );
}

export default App;
