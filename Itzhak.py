from flask import Flask, render_template, request, send_file
from music21 import stream, note, meter, key, metadata, converter, instrument
import os
import subprocess
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# RSA Functions
def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1  # Ensure it's odd and has the correct length
    return p

def is_prime(n, k=128):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_number(length):
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    x0, x1, y0, y1 = 0, 1, 1, 0
    original_phi = phi
    while e > 0:
        q, r = phi // e, phi % e
        phi, e = e, r
        x0, x1 = x1 - q * x0, x0
        y0, y1 = y1 - q * y0, y0
    if phi != 1:
        return None
    return y1 + original_phi if y1 < 0 else y1

def generate_keys(bit_length):
    p = generate_prime_number(bit_length)
    q = generate_prime_number(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)  # Public and private key

def encrypt(public_key, plaintext):
    e, n = public_key
    message_int = int.from_bytes(plaintext.encode('utf-8'), 'big')
    ciphertext = pow(message_int, e, n)
    return str(ciphertext)  # Return as string for storage

def decrypt(private_key, ciphertext):
    d, n = private_key
    print(d)
    print(n)
    decrypted_int = pow(int(ciphertext), int(d), int(n))
    byte_length = (decrypted_int.bit_length() + 7) // 8
    decrypted_bytes = decrypted_int.to_bytes(byte_length, 'big')
    return decrypted_bytes.decode('utf-8')

# Music Generation Functions
def create_music_sheet(message, output_path, instrument_name='Piano'):
    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = "Shiky8 Music Sheet"
    part = stream.Part()
    part.append(meter.TimeSignature('4/4'))
    part.append(key.KeySignature(0))
    
    inst = instrument.fromString(instrument_name)
    part.insert(0, inst)

    for char in message:
        if char.isalpha():
            pitch = 60 + (ord(char.upper()) - ord('A'))
        elif char == ' ':
            pitch = 72
        elif char.isdigit():
            pitch = 48 + (ord(char) - ord('0'))
        else:
            pitch = 81

        duration = 1
        note_obj = note.Note(pitch, quarterLength=duration)
        part.append(note_obj)

    score.append(part)
    musicxml_path = "temp_music_sheet.xml"
    score.write('musicxml', fp=musicxml_path)
    subprocess.run(['musescore', musicxml_path, '-o', output_path])
    return musicxml_path

def extract_message_from_notes(notes):
    message = ''
    for n in notes:
        if n.isNote:
            if 60 <= n.pitch.midi <= 85:
                char = chr((n.pitch.midi - 60) + ord('A'))
                message += char
            elif n.pitch.midi == 72:
                message += ' '
            elif 48 <= n.pitch.midi <= 57:
                char = chr((n.pitch.midi - 48) + ord('0'))
                message += char
            elif n.pitch.midi == 81:
                message += '?'  # Placeholder for special characters
    return message.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        instrument_choice = request.form['instrument']
        output_path = "music_sheet.png"
        
        bit_length = 128  # Adjust this based on your needs
        public_key, private_key = generate_keys(bit_length)
        ciphertext = encrypt(public_key, message)
        create_music_sheet(ciphertext, output_path, instrument_choice)
        
        return render_template('download.html', output_path=output_path, public_key=public_key, private_key=private_key)

    return render_template('index.html')


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    extracted_message = ''
    decrypted_message = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('extract.html', extracted_message='No file part')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('extract.html', extracted_message='No selected file')

        # Save the uploaded file
        musicxml_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(musicxml_path)

        # Get the private key from the form
        private_key = str(request.form['private_key'])

        score = converter.parse(musicxml_path)
        notes = score.flatten().notes
        extracted_message = extract_message_from_notes(notes)

        # Decrypt the extracted message using the provided private key
        try:
            # Validate the private key format
            d, n = map(int, private_key.split(','))  # Assuming the private key is in 'd,n' format
            
            # Ensure that the extracted message is in a valid format for decryption
            if extracted_message:  # Make sure there's something to decrypt
                decrypted_message = decrypt((d, n), extracted_message)  # Use your decryption method
                extracted_message += f" (Decrypted Message: {decrypted_message})"
            else:
                extracted_message += " (No message extracted for decryption.)"

        except ValueError as ve:
            extracted_message += f" (Error during key parsing: {str(ve)})"
        except Exception as e:
            extracted_message += f" (Error during decryption: {str(e)})"

    return render_template('extract.html', extracted_message=extracted_message)



if __name__ == '__main__':
    app.run(debug=True)
