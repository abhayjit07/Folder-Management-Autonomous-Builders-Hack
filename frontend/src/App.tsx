"use client"

import type React from "react"

import { useState } from "react"
import { Upload, FileText, Send, Check, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Textarea } from "@/components/ui/textarea"

export default function FileUploadPage() {
  const [fileContent, setFileContent] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string | null>(null)
  const [fileSize, setFileSize] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle")
  const [statusMessage, setStatusMessage] = useState("")
  const [isDragging, setIsDragging] = useState(false)

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + " bytes"
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB"
    else return (bytes / 1048576).toFixed(1) + " MB"
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    processFile(file)
  }

  const processFile = (file?: File) => {
    if (file && file.type === "text/plain") {
      setIsUploading(true)
      setStatus("idle")
      setFileName(file.name)
      setFileSize(formatFileSize(file.size))

      const reader = new FileReader()
      reader.onload = (e) => {
        setFileContent(e.target?.result as string)
        setIsUploading(false)
        setStatus("success")
        setStatusMessage("File uploaded successfully!")
      }
      reader.onerror = () => {
        setIsUploading(false)
        setStatus("error")
        setStatusMessage("Error reading file.")
      }
      reader.readAsText(file)
    } else if (file) {
      setStatus("error")
      setStatusMessage("Please upload a valid text file (.txt).")
    }
  }

  const handleSendToServer = async () => {
    if (!fileContent) {
      setStatus("error")
      setStatusMessage("No file content to send!")
      return
    }

    setIsSending(true)
    setStatus("idle")

    try {
      const response = await fetch("http://localhost:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: fileContent, file_name: fileName }),
      })

      if (response.ok) {
        setStatus("success")
        setStatusMessage("File data sent successfully!")
      } else {
        setStatus("error")
        setStatusMessage("Failed to send data to server.")
      }
    } catch (error) {
      console.error("Error sending file:", error)
      setStatus("error")
      setStatusMessage("Error connecting to server.")
    } finally {
      setIsSending(false)
    }
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    processFile(file)
  }

  return (
    <div className="container mx-auto py-10 px-4">
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl flex items-center gap-2">
            <FileText className="h-6 w-6" />
            Text File Upload
          </CardTitle>
          <CardDescription>Upload a text file to preview its content and send it to the server</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25 hover:border-primary/50"
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center justify-center gap-2">
              <Upload className="h-10 w-10 text-muted-foreground" />
              <p className="text-lg font-medium">Drag and drop your text file here</p>
              <p className="text-sm text-muted-foreground">or click to browse files</p>
              <input
                type="file"
                accept=".txt"
                onChange={handleFileUpload}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
            </div>
          </div>

          {isUploading && (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Uploading file...</p>
              <Progress value={66} className="h-2" />
            </div>
          )}

          {fileName && fileSize && (
            <div className="flex items-center gap-2 text-sm p-2 bg-muted rounded">
              <FileText className="h-4 w-4" />
              <span className="font-medium">{fileName}</span>
              <span className="text-muted-foreground">({fileSize})</span>
            </div>
          )}

          {status !== "idle" && (
            <Alert
              variant={status === "error" ? "destructive" : "default"}
              className={status === "success" ? "border-green-500 text-green-500" : ""}
            >
              {status === "success" ? <Check className="h-4 w-4" /> : <AlertCircle className="h-4 w-4" />}
              <AlertDescription>{statusMessage}</AlertDescription>
            </Alert>
          )}

          {fileContent && (
            <div className="space-y-2">
              <h3 className="text-sm font-medium">File Preview:</h3>
              <Textarea value={fileContent} readOnly className="min-h-[150px] font-mono text-sm" />
            </div>
          )}
        </CardContent>
        <CardFooter>
          <Button onClick={handleSendToServer} disabled={!fileContent || isSending} className="w-full">
            {isSending ? (
              <>
                <span className="animate-pulse">Sending...</span>
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" /> Send to Server
              </>
            )}
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}

