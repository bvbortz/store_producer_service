import json
import logging
import threading
import time
from flask import Flask
from flask import request

from api.enum import EnvironmentVariables
from api.gateway.rabbitmq import RabbitMQ


def publish_handler(rabbitMQ_instance, prompt, name):
    try:
        rabbitMQ_instance.publish(message=json.dumps({"prompt": prompt, "name": name}))
    except:
        time.sleep(10)
        rabbitMQ_instance.start_server()
        publish_handler(rabbitMQ_instance, prompt, name)
def main():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )
    print("started script server")
    rabbitMQ_instance = RabbitMQ(
        queue=EnvironmentVariables.RABBITMQ_QUEUE.get_env(),
        host=EnvironmentVariables.RABBITMQ_HOST.get_env(),
        routing_key=EnvironmentVariables.RABBITMQ_ROUTING_KEY.get_env(),
        username=EnvironmentVariables.RABBITMQ_USERNAME.get_env(),
        password=EnvironmentVariables.RABBITMQ_PASSSWORD.get_env(),
        exchange=EnvironmentVariables.RABBITMQ_EXCHANGE.get_env()
    )
    app = Flask(__name__)
    
    @app.route('/script/', methods=['POST', 'GET'])
    async def script():
        print("entered route")
        if request.method == 'POST':
            data = request.json
            prompt = data['prompt']
            name = data['name']
            func = lambda : publish_handler(rabbitMQ_instance, prompt, name)
            t = threading.Thread(target=func)
            t.start()
            return "Down"
        else:
            return 'UP'
    app.run(host="producer", port=EnvironmentVariables.PORT.get_env())
