import requests
import json
from PyQt6.QtCore import Qt
from youtube_transcript_api import YouTubeTranscriptApi
from PyQt6.QtWidgets import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.admit.clicked.connect(self.search_click)
        self.download_summarize.clicked.connect(self.download_trans)

    def settings(self):
        self.setWindowTitle('AI Youtube Summarizer')
        self.resize(950, 800)

    def initUI(self):

        self.title = QLabel('AI Youtube Summarizer')
        self.title.setObjectName("title")
        self.title.setStyleSheet("font-size: 34px; font-weight: bold; color:#4CAF50")  # Larger title font

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Please type a URL of a YouTube video")
        self.input_box.setStyleSheet("padding: 10px; font-size: 16px;")  # Style input box

        self.output = QTextEdit()
        self.output.setObjectName("output")
        self.output.setPlaceholderText("Summary")
        self.output.setReadOnly(True)  # Make the QTextEdit non-editable
        self.output.setStyleSheet("padding: 10px; font-size: 16px;")  # Style output box

        self.admit = QPushButton("Summarize")
        self.download_summarize = QPushButton("Download Summary")
        self.admit.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;")  # Style button
        self.download_summarize.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; font-size: 16px;")  # Style button

        self.master = QVBoxLayout()
        self.master.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.master.addWidget(self.input_box)
        self.master.addWidget(self.output)

        # Create a horizontal layout for the buttons
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.admit)
        self.buttons_layout.addWidget(self.download_summarize)

        self.master.addLayout(self.buttons_layout)  # Add the buttons layout to the main layout

        self.master.setSpacing(20)
        self.master.setContentsMargins(50, 50, 50, 50)  # Add margins to the main layout
        self.setLayout(self.master)

    def search_click(self):
        URL = self.input_box.text()
        if URL:
            self.input_box.clear()
            # self.results = "test"
            self.results = self.summarize_vid(URL)
        else:
            self.results = "Please type a URL."

        self.output.setText(self.results)

    def download_trans(self):
        summary_text = self.output.toPlainText()
        if summary_text:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Summary", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(summary_text)
                    self.output.setText(f"Summary saved to {file_path}")
                except Exception as e:
                    self.output.setText(f"Failed to save summary: {str(e)}")
        else:
            self.output.setText("No summary to save!")

    def summarize_vid(self, URL):
        try:
            HOST = "Your_local_host_here (ollama one)"

            video_id = URL.split("v=")[1].split("&")[0]

            # Fetch the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])

            transcription = " ".join([entry['text'] for entry in transcript])

            payload = {
                "model": "llama2",  # Replace with the model name you're using
                "messages": [{"role": "user", "content": f"Summarize this text and give key points of it: {transcription}"}]
            }

            response = requests.post(HOST, json=payload, stream=True)

            if response.status_code == 200:
                summary = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            json_data = json.loads(line)
                            if "message" in json_data and "content" in json_data["message"]:
                                summary += json_data["message"]["content"].replace("\n", "").replace("  ", " ") + " "
                        except json.JSONDecodeError:
                            return f"Failed to parse line: {line}"
                return summary.strip()
            else:
                return f"Error: {response.status_code}\n{response.text}"

        except Exception as e:
            return str(e)


if __name__ == '__main__':
    app = QApplication([])
    main = Window()
    main.show()
    app.exec()
