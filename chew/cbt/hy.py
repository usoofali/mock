from bs4 import BeautifulSoup

def extract_questions_and_options(filename):
    # Read the HTML file
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the HTML content
    soup = BeautifulSoup(content, 'lxml')
    
    # Find all wizard steps
    questions = []
    steps = soup.find_all('div', class_='wizard-step')
    
    for step in steps:
        # Extract the question
        question_element = step.find('h6', class_='sub-title')
        question_text = question_element.get_text(strip=True) if question_element else 'No Question Found'
        
        # Extract options
        options = []
        option_divs = step.find_all('div', class_='form-check radio radio-primary checbox-option')
        
        for option_div in option_divs:
            label = option_div.find('label', class_='form-check-label')
            option_text = label.get_text(strip=True) if label else 'No Option Found'
            options.append(option_text)
        
        # Append the question and its options to the list
        questions.append({
            'question': question_text,
            'options': options
        })
    
    return questions

if __name__ == "__main__":
    filename = 'exam.html'
    questions_and_options = extract_questions_and_options(filename)
    
    # Print the extracted questions and options
    for q in questions_and_options:
        print(q['question'])
        for option in q['options']:
            print(f' - {option}')
