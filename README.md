# Itzhak

A Flask-based web application that allows users to convert messages into music sheets, encrypting the message using RSA encryption and representing it as musical notes on a sheet. The application also provides functionality to extract and decrypt messages from uploaded MusicXML files.

## Features

- **Message to Music Sheet**: Convert text messages into music sheets, represented as musical notes that vary by selected instrument.
- **RSA Encryption**: Secure messages with RSA encryption before converting them to music sheets.
- **Downloadable Files**: Download generated music sheets in both XML and PNG formats.
- **Message Extraction**: Extract and decrypt messages from uploaded music sheets.
- **Flexible Instrument Choices**: Choose different instruments to style the generated music sheet.

## Setup Instructions

### Prerequisites

- **Python 3.8+** 
- **pip** (Python package manager)
- **MuseScore** (for converting MusicXML files to PNG images)
  - Download and install MuseScore from [MuseScore.org](https://musescore.org/).

### Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/shiky8/Itzhak.git
    cd Itzhak
    ```

2. **Install Dependencies**
    ```bash
    python3 -m pip install -r requirements.txt
    ```

3. **Set Up MuseScore**
   - Ensure MuseScore is available in your system's PATH or specify the full path in the `subprocess.run()` function in `create_music_sheet`.
   ```bash
    sudo apt install musescore
    ```

4. **Run the Application**
    ```bash
    python Itzhak.py
    ```
    The app will be available at `http://127.0.0.1:5000`.

## Usage

### Generate a Music Sheet

1. Go to the homepage at `http://127.0.0.1:5000/`.
2. Enter your message and select an instrument.
3. Click **Generate Music Sheet**. 
4. The app will display options to download the generated music sheet in XML and PNG formats, as well as the generated **Public Key** and **Private Key** for RSA encryption.

### Extract and Decrypt Message

1. Go to the **Extract Message** page by clicking the link on the homepage.
2. Upload the MusicXML file containing the encrypted message.
3. Enter the **Private Key** (format: `d,n`).
4. Click **Extract Message** to view the decrypted message.

## File Structure

- **app.py**: The main Flask application file with all the routes and functions.
- **templates/**: HTML templates for the app’s pages (`index.html`, `download.html`, `extract.html`).
- **static/**: (Optional) Contains any static files such as CSS, JavaScript, or images.
- **uploads/**: Directory to store uploaded files temporarily.

## How it Works

### Encryption and Decryption

- **RSA Encryption**: The message is encrypted using RSA before being converted into musical notes. A public-private key pair is generated for each message.
- **Decryption**: When a user uploads a music sheet and enters their private key, the app decrypts the extracted message back into readable text.

### Music Generation

- **Notes Generation**: The message characters are encoded as MIDI pitch values, representing notes on a 4/4 music sheet. Each letter, digit, and symbol corresponds to a unique note.
- **Conversion to PNG**: Using MuseScore, the generated MusicXML file is converted to a PNG image for download.

## Example

1. **Generate a Music Sheet**: 
    - Message: "Hello World"
    - Instrument: "Piano"
    - Output: MusicXML and PNG files with encoded notes.
  
2. **Extract Message**:
    - Upload the MusicXML file.
    - Enter the private key.
    - Decrypted Message: "Hello World" (or similar, based on the original input).
## Demo

## Requirements

- **Python Packages**:
  - `Flask`: Web framework.
  - `music21`: Library for generating and parsing MusicXML files.
  - `random`: For generating prime numbers in RSA encryption.

## Troubleshooting

- **MuseScore Errors**: If MuseScore isn’t found, ensure it’s correctly installed and available in the PATH.
- **RSA Key Parsing Errors**: Ensure the private key is entered in `d,n` format.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute, report issues, or suggest features!

