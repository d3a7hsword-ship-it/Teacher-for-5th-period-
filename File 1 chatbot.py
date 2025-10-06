import datetime
import random

# In-memory knowledge base
knowledge_base = {
    "greetings": {
        "hello": "Hello! How are you today?",
        "hi": "Hi there! Ready to learn something new?",
        "who are you": "I am your AI teacher, here to explain things clearly."
    },
    "definitions": {
        "science": {
            "gravity": {
                "main": "Gravity is the force that pulls objects toward each other.",
                "synonyms": ["gravitational force", "pull of gravity"],
                "examples": [
                    "Gravity keeps us on the ground.",
                    "Gravity causes objects to fall when dropped."
                ],
                "follow_up": "Gravity was first described by Isaac Newton in the 17th century."
            },
            "water": {
                "main": "Water is a liquid made of hydrogen and oxygen (H2O). Essential for life.",
                "examples": [
                    "Water fills oceans and lakes.",
                    "Water is vital for plants and animals."
                ]
            }
        },
        "math": {
            "addition": {
                "main": "Addition combines numbers. Example: 2 + 3 = 5.",
                "examples": [
                    "Adding 5 + 7 gives 12.",
                    "Addition is the first operation learned in math."
                ]
            },
            "multiplication": {
                "main": "Multiplication is repeated addition. Example: 3 × 4 = 12.",
                "examples": [
                    "5 × 2 = 10, which is 2+2+2+2+2.",
                    "Multiplication helps solve problems quickly."
                ],
                "follow_up": "Multiplication is fundamental for higher math."
            }
        },
        "technology": {
            "computer": {
                "main": "A computer processes information and runs programs.",
                "examples": [
                    "Laptops, desktops, and servers are all computers.",
                    "Computers can perform millions of calculations per second."
                ]
            },
            "phone": {
                "main": "A phone is a device used for communication.",
                "examples": [
                    "Smartphones allow calls, messages, and apps.",
                    "Phones are used worldwide to connect people."
                ]
            }
        }
    },
    "fun": {
        "joke": [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Why did the math book look sad? Because it had too many problems."
        ],
        "trivia": [
            "The Eiffel Tower can be 15 cm taller in summer due to metal expansion.",
            "Honey never spoils; archaeologists have found edible honey in ancient tombs."
        ]
    },
    "quizzes": {
        "science": {
            "gravity": "True or False: Gravity pulls objects toward each other?"
        },
        "math": {
            "addition": "What is 2 + 3?"
        }
    }
}

# Session memory
memory = {
    "name": None,
    "learned": {},  # New facts taught by user
    "last_topic": None
}

# Function to get current date/time
def get_datetime_response(user_input):
    now = datetime.datetime.now()
    if "day" in user_input:
        return f"Today is {now.strftime('%A')}."
    if "date" in user_input:
        return f"Today is {now.strftime('%A, %B %d, %Y')}."
    if "time" in user_input:
        return f"The current time is {now.strftime('%I:%M %p')}."
    return None

# Main response function
def get_response(user_input):
    user_input = user_input.lower()

    # Greetings
    for key, response in knowledge_base["greetings"].items():
        if key in user_input:
            return response

    # Definitions
    for subject, topics in knowledge_base["definitions"].items():
        for key, value in topics.items():
            # Check key or synonyms
            synonyms = value.get("synonyms", [])
            if key in user_input or any(s in user_input for s in synonyms):
                # Remember last topic
                memory["last_topic"] = key
                # Random example if available
                examples = value.get("examples")
                if examples:
                    return random.choice(examples)
                return value["main"]

    # Fun
    for key, items in knowledge_base.get("fun", {}).items():
        if key in user_input:
            return random.choice(items)

    # Quizzes
    if "quiz" in user_input:
        subject = random.choice(list(knowledge_base["quizzes"].keys()))
        topic, question = random.choice(list(knowledge_base["quizzes"][subject].items()))
        memory["last_topic"] = topic
        return f"Quiz time! {question}"

    # Follow-up explanations
    if "tell me more" in user_input and memory.get("last_topic"):
        topic = memory["last_topic"]
        for subject, topics in knowledge_base["definitions"].items():
            if topic in topics and "follow_up" in topics[topic]:
                return topics[topic]["follow_up"]

    # Date/time
    dt_response = get_datetime_response(user_input)
    if dt_response:
        return dt_response

    # Memory commands
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        memory["name"] = name
        return f"Nice to meet you, {name}!"
    if "what is my name" in user_input:
        if memory["name"]:
            return f"Your name is {memory['name']}."
        else:
            return "I don't know your name yet."

    # Learned responses
    if user_input in memory["learned"]:
        return memory["learned"][user_input]

    # Mini learning
    print("I don't know the answer. Teach me!")
    answer = input("You: ")
    memory["learned"][user_input] = answer
    return "Got it! I'll remember that."

# Chat loop
print("AI Teacher: Hello! Ask me anything, or type 'bye' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("AI Teacher: Goodbye!")
        break
    response = get_response(user_input)
    print("AI Teacher:", response)
