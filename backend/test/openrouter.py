api_key="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"
import requests
import json
import os
filePath=os.path.dirname(os.path.abspath(__file__))
def getDeepSeekResponse(prompt):
   
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer {0}".format(api_key),
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1-distill-qwen-7b",
        "messages": [
        {
            "role": "user",
            "content": prompt
        }
        ],
        
    })
    )
    
    #print(response.json())
    # Check if the request was successful
    result=None
    if response.status_code == 200:
        #print("Response:", response.json())
        result=response.json()
        content= result["choices"][0]["message"]["content"]
        result=content
        #print(result["choices"][0]["message"]["content"])

    else:
        result="Error: {0} - {1}".format(response.status_code, response.text)
        print("Error:", response.status_code, response.text)
    # Example usage
    return result
def getHouseInfo(houseNum):
    file=filePath+"/images/house1/info.txt"
    with open(file, "r") as text_file:
        unknown = text_file.readlines()
        return unknown

    
def askHouseInfo(housenum,question):
    houseInfo=getHouseInfo(housenum)
    prompt = "Based on the following house information, {0} \n\nHouse Information:\"{1}\"\n".format(question,houseInfo)
    
    #print("House Info:", prompt)
    response = getDeepSeekResponse(prompt)
    
    print("Response:", response)
    #print("Content:", response["choices"][0]["message"]["content"])
    return response
if __name__ == "__main__":
    houseInfo=getHouseInfo(1)
    prompt = "Based on the following house information, what is the size of the biggest room? \n\nHouse Information:\"{0}\"\n".format(houseInfo)
    
    #print("House Info:", prompt)
    response = getDeepSeekResponse(prompt)
    

    print("Response:", response)
    #print("Content:", response["choices"][0]["message"]["content"])