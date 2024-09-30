import fitz  # PyMuPDF
import os

def extract_section_5_summary(pdf_path):
    # Check if the file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No such file: '{pdf_path}'")
    
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    # Extract text from the entire document
    text = ""
    for page_num in range(document.page_count):
        page = document[page_num]
        text += page.get_text("text")
    
    # Find SECTION 5
    section_5_start = text.find("SECTION 5 — ACCIDENT DETAILS - DESCRIPTION")
    if section_5_start == -1:
        return "SECTION 5 not found in the document."
    
    section_5_end = text.find("SECTION 6", section_5_start)
    if section_5_end == -1:
        section_5_end = len(text)
    
    section_5_text = text[section_5_start:section_5_end].strip()
    
    # Extract detailed accident description
    description_start = section_5_text.find("On")
    description_end = section_5_text.find("ITEMS MARKED BELOW FOLLOWED BY AN ASTERISK (*) SHOULD BE EXPLAINED IN THE NARRATIVE", description_start)
    if description_start != -1 and description_end != -1:
        description = section_5_text[description_start:description_end].strip()
    else:
        description = section_5_text[description_start:].strip()
    
    # Clean up the description to form a single paragraph
    description = ' '.join(description.split())
    
    return description

def extract_directory_and_filename(path):
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    return directory, filename

def write_summary_to_file(pdf_path, summary):

    summary_path = "/Users/mcharkhabi/public-github/cs244b/Data/CA_DMV_AV_COLLISION_SUMMARIES/" 
    directory, filename = extract_directory_and_filename(pdf_path)
    # print(f"directory:{directory}, filename:{filename}")

    # Create the summary file name
    summary_file_path = summary_path + filename.replace(".pdf", "_summary.txt")
    # print(f"type:{type(summary_file_path)} and value:{summary_file_path}")
    
    # Write the summary to the file
    with open(summary_file_path, 'w') as summary_file:
        summary_file.write(summary)
    
    print(f"Summary written to {summary_file_path}")

def process_all_pdfs_in_dir(dir_path):
    for filename in os.listdir(dir_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(dir_path, filename)
            summary = extract_section_5_summary(pdf_path)
            print(f"pdf_path:{pdf_path}, summary:{summary}")
            write_summary_to_file(pdf_path, summary)

def get_prompt_template():
    PROMPT_TEMPLATE = "You are a triage assistant at an autonomous vehicle company. I will describe and driving scenario, and I ask that you answer the following questions: \
    1. Does a rules-of-the-road regulation apply to this case? Answer TRUE or FALSE only. \
    2. What rules of the road regulations apply in the local state? Answer with a list of vehicle codes such as ['VEHICLE CODE 1', 'VEHICLE CODE 2'] only. List no more than 3 vehicle codes. \
    3. Describe your professional rules-of-the-road assessment and complete the following template: [NO, LOW, UNDUE] legal risk. [NO, AN] undesired driving behavior."

def main():

    # file_name = "waymo_06032024-pdf.pdf"
    # pdf_path = "/Users/mcharkhabi/public-github/cs244b/Data/CA_DMV_AV_COLLISION_REPORTS/" + file_name
    
    # Extract summary from SECTION 5
    # summary = extract_section_5_summary(pdf_path)
    
    dir_path = "/Users/mcharkhabi/public-github/cs244b/Data/CA_DMV_AV_COLLISION_REPORTS/"
    process_all_pdfs_in_dir(dir_path)

    # Write the summary to a file
    # write_summary_to_file(pdf_path, summary)

if __name__ == "__main__":
    main()
