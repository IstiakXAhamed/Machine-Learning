#Few shot prompting - a technique where the model is given a few examples to learn from before performing the task
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

genai_key = os.getenv("GENAI_API_KEY")
if not genai_key:
    raise RuntimeError("GENAI_API_KEY is not set in the environment")

client = OpenAI(
    api_key=genai_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = """
    You are an expert AI Assistant in resolving user queries using Chain of thought . 
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps with detailed reasoning.
    Once you think enough PLAN has been done, finally you can give OUTPUT.
    
    Rules:
    - Strictly follow the given json format
    - Only run one step at a time.
    - Show detailed thinking in PLAN steps, breaking down complex problems into smaller parts
    - The sequence of steps in START (Where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user)
    
    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string"}
     
    Example 1:
    START: Hey Can you solve 2+3*5/10
    PLAN: {"step": "PLAN", "content": "I need to solve the mathematical expression 2+3*5/10. First, I'll identify the operations: addition (+), multiplication (*), and division (/)"}
    PLAN: {"step": "PLAN", "content": "According to PEMDAS/BODMAS rules, multiplication and division come before addition"}
    PLAN: {"step": "PLAN", "content": "Looking at 3*5/10, I'll work left to right for multiplication and division. First: 3*5 = 15"}
    PLAN: {"step": "PLAN", "content": "Next, perform division on the result: 15/10 = 1.5"}
    PLAN: {"step": "PLAN", "content": "Now I have simplified the expression to: 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Finally, perform the addition: 2 + 1.5 = 3.5"}
    OUTPUT: {"step": "OUTPUT", "content": "The answer is 3.5"}
    
    Example 2:
    START: What is the capital of France and its population?
    PLAN: {"step": "PLAN", "content": "This question has two parts: (1) identifying the capital of France, and (2) stating its population"}
    PLAN: {"step": "PLAN", "content": "For part 1: France is a European country, and its capital city is Paris"}
    PLAN: {"step": "PLAN", "content": "For part 2: I need to provide population data. Paris has different population counts depending on the area"}
    PLAN: {"step": "PLAN", "content": "The city proper (Paris itself) has approximately 2.2 million residents"}
    PLAN: {"step": "PLAN", "content": "The metropolitan area is much larger, with over 12 million people, but the question asks for the capital's population"}
    PLAN: {"step": "PLAN", "content": "I'll provide the city proper population as the primary answer, as that's the most direct interpretation"}
    OUTPUT: {"step": "OUTPUT", "content": "The capital of France is Paris, with a population of approximately 2.2 million people in the city proper."}
    
    Example 3:
    START: How many days until Christmas if today is October 15?
    PLAN: {"step": "PLAN", "content": "I need to calculate the number of days from October 15 to December 25 (Christmas)"}
    PLAN: {"step": "PLAN", "content": "I'll break this into three parts: remaining days in October, all days in November, and days in December up to the 25th"}
    PLAN: {"step": "PLAN", "content": "October has 31 days total. From October 15 to October 31: 31 - 15 = 16 days remaining"}
    PLAN: {"step": "PLAN", "content": "November is a full month between October and December. November has 30 days"}
    PLAN: {"step": "PLAN", "content": "In December, I need to count from December 1st to December 25th inclusive: that's 25 days"}
    PLAN: {"step": "PLAN", "content": "Now I'll sum up all the parts: 16 (remaining October) + 30 (November) + 25 (December) = 71 days"}
    PLAN: {"step": "PLAN", "content": "Let me verify: Oct 15→31 (16 days) + Nov (30 days) + Dec 1→25 (25 days) = 71 days total"}
    OUTPUT: {"step": "OUTPUT", "content": "There are 71 days until Christmas from October 15."}
    
    Example 4:
    START: If I buy 3 shirts at $25 each and get a 20% discount, how much do I pay?
    PLAN: {"step": "PLAN", "content": "This is a multi-step calculation involving multiplication and percentage discount"}
    PLAN: {"step": "PLAN", "content": "Step 1: Calculate the total price before discount. I have 3 shirts at $25 each"}
    PLAN: {"step": "PLAN", "content": "Total before discount: 3 × $25 = $75"}
    PLAN: {"step": "PLAN", "content": "Step 2: Calculate the discount amount. A 20% discount means I save 20% of $75"}
    PLAN: {"step": "PLAN", "content": "Discount calculation: 20% of $75 = 0.20 × $75 = $15"}
    PLAN: {"step": "PLAN", "content": "Step 3: Subtract the discount from the original total"}
    PLAN: {"step": "PLAN", "content": "Final price: $75 - $15 = $60"}
    PLAN: {"step": "PLAN", "content": "Alternatively, 20% off means paying 80% of the original price: 0.80 × $75 = $60. This confirms my answer"}
    OUTPUT: {"step": "OUTPUT", "content": "You would pay $60 after the 20% discount (saving $15 on the original $75)."}
"""
print("\n\n\n")

message_history = [
    {"role": "system", "content" : SYSTEM_PROMPT},
]

user_query = input("type your query : ")

message_history.append({"role": "user", "content" : user_query})

while True:
    response = client.chat.completions.create(
        model = "gemini-2.5-flash",
        response_format = {"type": "json_object"},
        messages= message_history
        
    )
    
    raw_result = (response.choices[0].message.content)
    message_history.append({"role": "assistant","content": raw_result})
    parsed_result = json.loads(raw_result)
    
    if parsed_result.get("step")=="START":
        print("Started : ",parsed_result.get("content"))
        continue
    if parsed_result.get("step")=="PLAN":
        print("Thinking : ",parsed_result.get("content"))
        continue
    if parsed_result.get("step")=="OUTPUT":
        print("OUTPUT : ",parsed_result.get("content"))
        break

print("\n\n\n")