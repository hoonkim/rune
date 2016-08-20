import pika


def SendFunctionCall ( username, project, function, params ): 
	print ("start send function call")
	print (username)
	print (project)
	print (function)
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='wisp')
	channel.basic_publish(exchange='',
                      routing_key='wisp',
                      body='{ "user" :"'+ username+'", "project" :"'+ project+'", "function" :"'+function+'", "params" : [ "seoul", "kr", "nano" ] }')
	connection.close()

SendFunctionCall('kim', 'rune', 'getTime', '[ "seoul", "kr", "nano"]')




