# memory.py

conversation_history = []

def add_to_memory(question, answer):
    conversation_history.append({
        "question": question,
        "answer": answer
    })

def get_context():
    context = ""
    for item in conversation_history[-3:]:  # last 3 messages
        context += f"Q: {item['question']}\nA: {item['answer']}\n\n"
    return context
