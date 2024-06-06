import os
import base64
from io import BytesIO
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def extract_num_reads(html_file):
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    num_reads = 0

    # Find all tables in the HTML file
    tables = soup.find_all('table')

    # Iterate over each table
    for table in tables:
        # Find all rows in the table
        rows = table.find_all('tr')

        # Iterate over each row
        for row in rows:
            # Find all cells in the row
            cells = row.find_all('td')

            # Check if the row contains "Total Sequences" metric
            if len(cells) == 2 and cells[0].text.strip() == "Total Sequences":
                num_reads = int(cells[1].text.strip())
                return num_reads

    return num_reads

def create_bar_chart(data):
    # Create bar chart
    files = [item[0] for item in data]
    read_counts = [item[1] for item in data]

    fig, ax = plt.subplots()
    ax.barh(files, read_counts, color='skyblue')
    ax.set_xlabel('Number of Reads')
    ax.set_ylabel('HTML File')
    ax.set_title('Read Counts from HTML Files')
    
    # Save the plot to a BytesIO object and encode it in base64
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return image_base64

if __name__ == "__main__":
    # Define the target number of reads
    target_reads = 100000

    # Get a list of files in the current directory
    files_in_directory = os.listdir()

    # Filter out HTML files
    html_files = [file for file in files_in_directory if file.endswith('.html')]

    data = []
    for html_file in html_files:
        num_reads = extract_num_reads(html_file)
        passed = num_reads >= target_reads
        missing_reads = max(0, target_reads - num_reads)
        data.append((html_file, num_reads, passed, missing_reads))

    # Create the bar chart
    chart_base64 = create_bar_chart(data)

    # Write the results to an HTML file
    with open("read_counts.html", "w") as output_file:
        output_file.write("<html><head><title>Read Counts</title></head><body>")
        output_file.write("<h1>Read Counts from HTML Files</h1>")
        output_file.write('<img src="data:image/png;base64,{}" alt="Bar Chart">'.format(chart_base64))
        output_file.write("<table border='1'>")
        output_file.write("<tr><th>HTML File</th><th>Number of Reads</th><th>Passed</th><th>Missing Reads</th></tr>")
        
        for html_file, num_reads, passed, missing_reads in data:
            output_file.write(f"<tr><td>{html_file}</td><td>{num_reads}</td><td>{passed}</td><td>{missing_reads}</td></tr>")
        
        output_file.write("</table>")
        output_file.write("</body></html>")

