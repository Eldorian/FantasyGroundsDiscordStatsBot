import azure.functions as func
from main import client

def main(req: func.HttpRequest) -> func.HttpResponse:
    client.run()
    return func.HttpResponse("Function executed successfully.")