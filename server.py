from flask import Flask,render_template, url_for, request , redirect
from xml.etree import ElementTree as ET

app = Flask(__name__)

data_file = 'data.xml'

@app.route('/')
@app.route('/home')
def home():
   return render_template("index.html")

@app.route('/aloe-vera')
def aloe_vera():
   return render_template('aloe-vera.html')

@app.route('/bacularis')
def bacularis():
   return render_template('bacularis.html')

@app.route('/fern')
def fern():
   return render_template('fern.html')

@app.route('/boncel')
def boncel():
   return render_template('bonsel.html')

@app.route('/cactus')
def cactus():
   return render_template('cactus.html')

@app.route('/omata')
def omata():
   return render_template('omata.html')

@app.route('/history')
def history():
    try:
        # Parse the existing XML file
        tree = ET.parse('data.xml')
        root = tree.getroot()

        # Extract data from XML and store it in a list of dictionaries
        entries = []
        for entry in root.findall('entry'):
            data = {
                'name': entry.find('name').text,
                'number': entry.find('number').text,
                'email': entry.find('email').text,
                'plant': entry.find('plant').text,
                'price': entry.find('price').text,
                'address': entry.find('address').text
            }
            entries.append(data)

        return render_template('table.html', entries=entries)
    except (FileNotFoundError, ET.ParseError):
        # If the file doesn't exist or is empty, return an empty list of entries
        return render_template('table.html', entries=[])


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        number = request.form.get('number')
        email = request.form.get('email')
        plant = request.form.get('plant')
        price = request.form.get('price')
        address = request.form.get('address')

        # Load the existing XML file or create a new one if it doesn't exist
        try:
            tree = ET.parse('data.xml')
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            # If the file doesn't exist or is empty, create a new root element
            root = ET.Element('data')
            tree = ET.ElementTree(root)

        # Create a new entry for the submitted data
        entry = ET.Element('entry')
        ET.SubElement(entry, 'name').text = name + "\n"
        ET.SubElement(entry, 'number').text = number
        ET.SubElement(entry, 'email').text = email
        ET.SubElement(entry, 'plant').text = plant
        ET.SubElement(entry, 'price').text = price
        ET.SubElement(entry, 'address').text = address

        # Append the new entry to the root
        root.append(entry)

        # Save the updated XML file
        tree.write('data.xml')


        return render_template('index.html')


@app.route('/delete_entry/<int:entry_index>', methods=['POST'])
def delete_entry(entry_index):
    if request.method == 'POST':
        try:
            # Parse the existing XML file
            tree = ET.parse('data.xml')
            root = tree.getroot()

            # Find the entry to be deleted
            entry_to_delete = root.find('entry[{}]'.format(entry_index + 1))

            # If the entry exists, remove it from the root
            if entry_to_delete is not None:
                root.remove(entry_to_delete)

                # Save the updated XML file
                tree.write('data.xml')

        except (FileNotFoundError, ET.ParseError):
            # Handle file not found or parsing error (if necessary)
            pass

    # Redirect back to the history page
    return redirect(url_for('history'))



def parse_xml():
    tree = ET.parse(data_file)
    root = tree.getroot()
    data = []

    for entry in root.findall('entry'):
        name = entry.find('name').text
        number = entry.find('number').text
        email = entry.find('email').text
        plant = entry.find('plant').text
        price = entry.find('price').text
        address = entry.find('address').text

        data.append({
            'name': name,
            'number': number,
            'email': email,
            'plant': plant,
            'price': price,
            'address': address
        })

    return data

@app.route('/search', methods=['POST'])
def search_data():
    search_term = request.form['search_term'].lower()
    data = parse_xml()

    filtered_data = [item for item in data if
                     search_term in item['name'].lower() or
                     search_term in item['plant'].lower()]

    return render_template('table.html', entries=filtered_data)

if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0" ,port=5000)