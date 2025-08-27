from llama import app as llama_app, generate

with llama_app.run():
    result=generate.remote("Life is a mystery, everyone must stand alone, I hear")
    
print(result)   