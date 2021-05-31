# ECOVALUE

## Cómo ejecutar:

## Prerequisitos
- Una máquina preferiblemente linux con [docker](https://docs.docker.com/get-docker/) instalado.

###  Instalación en instancias EC2 de AWS
Si usted tiene acceso a una cuenta con recursos EC2: puede instalar las dependencias en su instancia con estos comandos:

~~~bash
sudo amazon-linux-extras install docker
sudo yum install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
~~~


## Verificar que docker está instalado y corriendo

En su consola ejecute:
~~~bash
sudo systemctl status docker
~~~
Debe mostrar una serie de mensajes en los que se encuentra:

~~~bash
...
     Active: active (running)
...
~~~

## Crear la imagen de ejecución
Crear una imagen con todos los paquetes necesarios para que la app corra bien. Esto tomará el archivo [Dockerfile](https://github.com/fsosap/expert-system/blob/main/Dockerfile) e instalará todas las dependencias:

~~~bash
docker build -t app-expert .
~~~

**Nota:** No omitir el punto al final del comando

## Ejecutar el contenedor de Docker en segundo plano 

~~~bash
docker run -p 80:80 app-expert .
~~~

**Nota:** Si tiene problemas en este paso con permisos es posible que su máquina no le deje ejecutar aplicaciones en el puerto 80 ya que es protegido. En ese caso, cambie el puerto 80 por otro como 8080 en la máquina:

~~~bash
docker run -p 8080:80 app-expert .
~~~

## Probar la ejecución
Para probar la ejecución del servicio podemos usar [Postman](https://www.postman.com/downloads/) o *curl* si, como el equipo de ECOVALUE, es más amante de la consola:

~~~bash
curl -X POST http://<tu IP o dominio>/recommend \
   -H 'Content-Type: application/json' \
   -d ' {
    "free_cash_flow_to_total_debt": 5.985886,  
    "accounts_ayable_turnover": 0.545793, 
    "operating_margin": -84.875316, 
    "sales_per_employee": 566922.568600, 
    "asset_turnover": 0.255633, 
    "total_debt_to_total_assets": 0.000000, 
    "current_ratio": 8.953141, 
    "revenue_growth_year_over_year": 488.260427, 
    "return_on_assets": -23.377976
}'
~~~

Note que debe reemplazar la IP por la que tiene su máquina, por ejemplo 127.0.0.1 que es la IP local.
