# Despegar 

## Contexto: 

Estás desarrollando un sistema para una agencia de viajes en línea que ofrece a los clientes la posibilidad de reservar vuelos, hoteles y paquetes turísticos. El sistema debe gestionar información sobre clientes, reservas, vuelos, hoteles, paquetes turísticos, pagos, ciudades y países. Cada reserva puede incluir varias personas. El objetivo es diseñar un modelo de base de datos que permita almacenar, consultar y analizar estos datos de manera eficiente. 

## Descripción del Sistema: 

La agencia de viajes en línea proporciona servicios de reservas para vuelos, hoteles y paquetes turísticos. Los clientes pueden realizar reservas que se asocian a sus perfiles y pueden incluir múltiples personas. El sistema debe permitir gestionar toda esta información de manera integral. 

## Clientes: 

El sistema debe gestionar la información básica de los clientes, como nombre, dirección, número de teléfono y correo electrónico. Además, debe registrar las reservas realizadas por cada cliente. 

## Reservas: 

Cada reserva representa una transacción en la que un cliente selecciona uno o más servicios ofrecidos por la agencia. Debe almacenarse el número de reserva, la fecha en que se realizó y el estado de la reserva. 

## Personas en Reserva: 

Dentro de cada reserva, puede haber múltiples personas asociadas. El sistema debe permitir el registro de detalles sobre cada persona en la reserva, como nombre y número de pasaporte. 

## Servicios: 

  - Vuelos: La agencia ofrece vuelos que los clientes pueden reservar. El sistema debe registrar información sobre cada vuelo, como el número de vuelo, origen, destino, fechas y horas, aerolínea y precio. 

  - Hoteles: Los clientes pueden reservar estancias en hoteles. El sistema debe gestionar información sobre los hoteles, como nombre, dirección, número de estrellas, tipo de habitaciones, precio y disponibilidad. 

  - Paquetes Turísticos: Los paquetes turísticos combinan vuelos y estancias en hoteles en una oferta integrada. El sistema debe manejar información sobre cada paquete, incluyendo nombre, descripción, las ciudades y países incluidos y el precio total. 

## Pagos: 

El sistema debe registrar información sobre los pagos realizados por los clientes, incluyendo el método de pago, monto, fecha del pago y estado del pago. 

## Ubicaciones: 

  - Paises: El sistema debe gestionar información sobre países, incluyendo nombre, código del país y continente. 

  - Ciudades: Cada servicio ofrecido está asociado a una ciudad dentro de un país. El sistema debe registrar datos sobre cada ciudad, como nombre y código postal. 

 
