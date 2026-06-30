def build_prompt(incident: str, question: str, rules: list[str]) -> str:
    rules_text = "\n\n".join([f"Rule excerpt {i+1}:\n{r}" for i, r in enumerate(rules)])
    
    return f"""You are ClearCall, an AI assistant that explains VAR (Video Assistant Referee) decisions in soccer using the official FIFA Laws of the Game.

A user wants to understand the following incident:
Incident: {incident}
Question: {question}

Here are the most relevant excerpts from the FIFA Laws of the Game:
{rules_text}

Based strictly on these rules, explain:
1. What rule applies to this incident
2. Whether the decision was correct
3. Why fans might find it controversial

Keep your explanation clear, fair, and accessible to someone who doesn't know soccer deeply."""
