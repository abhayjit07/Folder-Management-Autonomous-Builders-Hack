import { useState } from "react";

function App() {
  const [fileContent, setFileContent] = useState<string | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "text/plain") {
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
    if (!fileContent) {
      alert("No file content to send!");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: fileContent }),
      });

      if (response.ok) {
        alert("File data sent successfully!");
      } else {
        alert("Failed to send data.");
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
      <button onClick={handleSendToServer} disabled={!fileContent}>
        Send to Server
      </button>
    </div>
  );
}

export default App;
