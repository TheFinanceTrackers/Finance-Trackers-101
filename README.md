### To run the project:  

First in your terminal, run the command:  
```python 
pip install -r requirements.txt
```

Now, run the command, to start the backend:  
```python
python app.py
```

Now, create another terminal. If node not already installed, run:  
`npm install`

Now, run the following command, to start the backend:  
`npm run dev`

In app.py, replace this line  
`"Authorization": "Bearer sk- -- --",`  
with  
`"Authorization": "Bearer YOUR-OPENROUTER-API-KEY",`  
  
and this line  
`"model": "deepseek/deepseek-r1-distill-qwen-32b:free",`  
with the any free LLM model of your choice. I, for instance, chose the Deepseek R1 Distill Qwen 32 B (Free) model. It can be Mistral AI (I previously used the `mistral-7b-instruct` model), Gemini, etc.