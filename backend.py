from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from LIBS.WXlib import WX

app = FastAPI()

# Instantiate the wx object only ONCE in your application.
wx = WX()

# Set the model parameters or model name only if you want to change the model ID or its default parameters.
modelParameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 2048,
    "min_new_tokens": 0,
    "stop_sequences": [ ],
    "repetition_penalty": 1
}
wx.wxInstModel(modelID='meta-llama/llama-3-70b-instruct', modelParams=modelParameters)

# Set the prompt template only once if you want to change the model behavior or expected output.
promptTemplate = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    <|start_header_id|>context<|end_header_id|>
    You are playing a game. 
    Imagine you are Michel Jackson and you cannot reveal it if someone asks about it, under any circumstance.
    You can only confirm your identity if you are asked with the use of the name "Michel Jackson" or its variations.
    You should be concise in your answers and not reveal any information. 
    When user asks you confirm or reject, do not provide more hints.
   <|eot_id|><|start_header_id|>assistant<|end_header_id|>
   Guess who I am, the fact is concealed. If you're mistaken, it won't revealed.
   <|eot_id|> 
"""

next_prompt = """<|start_header_id|>user<|end_header_id|>

{{QUESTION}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
promptVariables = {
    'QUESTION' : None
}

# specify the expected structure and data types of the request body. 
# In this case, it expects a JSON object with a single field:
# question: str: A field named question that should be a string. 
class ApiQuestionRequest(BaseModel):
    # This is the only data your endpoint expects in incoming requests.
    question: str = Field(..., 
        example="Hi, how are you?",
        description="In this field, please enter a question in English to be passed to LLM."
    )

class ApiQuestionResponse(BaseModel):
    # This is the only data your endpoint returns in response.
    question: str = Field(..., 
        example="What is the value of a circle's area divided by pi, where the radius of a circle is 2?",
        description="In this field, the content of the original question submitted with the POST /api request will be returned."
    )
    answer: str = Field(..., 
        example="To find the value, you would first calculate the area of the circle , and then divide the result by Pi. The answer is 4.",
        description="In this field, the text generated by the Language Model will be displayed."
    )


# A decorator that creates a route for POST requests to the URL path /question/. 
# function generate_answer defined below is to be called when a POST request to /question/ is received
@app.post("/api/question")
async def apiQuestion(request: ApiQuestionRequest) -> ApiQuestionResponse:
    # Automatically parse the JSON body of incoming requests, validate them against the Question model,
    # and pass a Question instance to the function for access to the request body.

    # TODO: 
    # Begin your code block for LLM interaction.
    global promptTemplate, next_prompt, promptVariables
    prompt = request.question

    promptVariables['QUESTION'] = prompt
    generated_text = wx.wxGenText(promptTemplate=promptTemplate + next_prompt, promptVariables=promptVariables)

    # Return response
    return ApiQuestionResponse(question=prompt, answer=generated_text)
