import time
fileToOpen = "template_index.html"

while True:
    with open(fileToOpen) as fl:
        SWITCHSTATELEDCACHETTE = "ON"
        DHT11TEMPCACHETTEHUMIDE = "21"
        DHT11HUMCACHETTEHUMIDE = "80"
        DHT11TEMPCACHETTECHAUDE = "28"
        DHT11HUMCACHETTECHAUDE = "33"
        DHT11TEMPSALON = "22"
        DHT11HUMSALON = "31"
        content = fl.read()
        content = content.replace("SWITCHSTATELEDCACHETTE", SWITCHSTATELEDCACHETTE)
        content = content.replace("DHT11TEMPCACHETTEHUMIDE", DHT11TEMPCACHETTEHUMIDE)
        content = content.replace("DHT11HUMCACHETTEHUMIDE", DHT11HUMCACHETTEHUMIDE)
        content = content.replace("DHT11TEMPCACHETTECHAUDE", DHT11TEMPCACHETTECHAUDE)
        content = content.replace("DHT11HUMCACHETTECHAUDE", DHT11HUMCACHETTECHAUDE)
        content = content.replace("DHT11TEMPSALON", DHT11TEMPSALON)
        content = content.replace("DHT11HUMSALON", DHT11HUMSALON)
        print(content)

    html = open("index.html", mode="w")
    html.write(content)
    time.sleep(1)