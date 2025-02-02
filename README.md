# AI YouTube Summarizer

This is a simple PyQt6-based desktop application that allows you to summarize the content of a YouTube video using AI. It fetches the transcript of a YouTube video and sends it to a local model (e.g., Llama2) for summarization. The result can then be saved as a text file.

## Features

- Input a YouTube video URL
- Summarize the video's transcript
- Download the summary as a ```.txt``` file
- Simple and easy-to-use graphical interface built with PyQt6
- Supports multiple languages for transcript extraction (e.g., English, Arabic)

## Requirements

- Python 3.x
- PyQt6
- youtube-transcript-api
- requests

Install the required dependencies using `pip`:

```bash
pip install PyQt6 youtube-transcript-api requests
```

## How to Run
### 1-Clone the repository:

```bash
git clone https://github.com/yourusername/ai-youtube-summarizer.git
cd ai-youtube-summarizer
```

### 2-Run the application:

```bash
python main.py
```

### Enter the YouTube video URL in the input box and click "Summarize" to get the transcript summary.
### You can also download the summary as a ```.txt``` file by clicking "Download Summary"


## Supported Languages
#### This tool supports transcript extraction for YouTube videos in multiple languages, such as English, Arabic, and more. You can customize the languages in the code if needed.

## UI DEMO

![Image](https://github.com/user-attachments/assets/ed942f6e-2007-470f-acc9-c18755febc94)
