import json

def load_knowledge_base(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def ask_questions(questions):
    answers = {}

    for question_id, question in questions.items():
        print(f"\n{question_id}. {question['text']}")
        for number, answer in enumerate(question["answers"], start=1):
            print(f"  {number}. {answer}")

        while True:
            choice = input("Wybierz numer odpowiedzi: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(question["answers"]):
                answers[question_id] = question["answers"][int(choice) - 1]
                break
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

    return answers

def rule_matches(rule, answers):
    for question_id, expected_answer in rule["if"].items():
        if answers.get(question_id) != expected_answer:
            return False
    return True

def main():
    knowledge_base = load_knowledge_base("baza.json")
    answers = ask_questions(knowledge_base["questions"])

    print("\n--- Wyniki diagnozy ---")
    matches = []

    for rule in knowledge_base["rules"]:
        if rule_matches(rule, answers):
            matches.append(rule)

    if not matches:
        print("Nie znaleziono pasującej reguły. Potrzebna jest dalsza analiza.")
        return

    for rule in matches:
        print(f"\nReguła {rule['id']}")
        print(f"Diagnoza: {rule['then']['diagnosis']}")
        print(f"Zalecane działanie: {rule['then']['action']}")

    print(f"\nLiczba pasujących reguł: {len(matches)}")

if __name__ == "__main__":
    main()
