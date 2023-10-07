def generate_certificate(name, level):
    # Load the HTML template and replace the placeholder with the provided name and level
    with open('certificate_template.html', 'r') as template_file:
        certificate_html = template_file.read()
    
    certificate_html = certificate_html.replace('%NAME%', name)
    certificate_html = certificate_html.replace('%LEVEL%', str(level))

    # Generate the output filename
    output_filename = f'circus_melody_{name.replace(" ", "_")}_level_{level}.html'

    # Save the modified HTML content to the new HTML file
    with open(output_filename, 'w') as output_file:
        output_file.write(certificate_html)

generate_certificate('John Doe', 1)
