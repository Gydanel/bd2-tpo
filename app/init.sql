SET FOREIGN_KEY_CHECKS=0; -- to disable them

REPLACE INTO usuarios (id, nombre, email, foto_perfil, telefono, fecha_registro, country)
VALUES
  (1, 'Ana López', 'ana.lopez@email.com', 'ana.jpg', '123456789', NOW(), 'Spain'),
  (2, 'Carlos Pérez', 'carlos.perez@email.com', NULL, NULL, NOW(), 'Mexico'),
  (3, 'Lucía Gómez', 'lucia.gomez@email.com', 'lucia.jpg', '987654321', NOW(), 'Argentina'),
  (4, 'Miguel Torres', 'miguel.torres@email.com', NULL, '555123456', NOW(), 'Chile'),
  (5, 'Sofía Ruiz', 'sofia.ruiz@email.com', 'sofia.jpg', NULL, NOW(), 'Colombia'),
  (6, 'David Fernández', 'david.fernandez@email.com', NULL, '666777888', NOW(), 'Peru'),
  (7, 'Elena Martínez', 'elena.martinez@email.com', 'elena.jpg', '111222333', NOW(), 'Uruguay'),
  (8, 'Javier Sánchez', 'javier.sanchez@email.com', NULL, NULL, NOW(), 'Ecuador'),
  (9, 'María Castro', 'maria.castro@email.com', 'maria.jpg', '444555666', NOW(), 'Venezuela'),
  (10, 'Pedro Ramos', 'pedro.ramos@email.com', NULL, '777888999', NOW(), 'Spain');

REPLACE INTO empresas (id, nombre, descripcion, ubicacion)
VALUES
  (1, 'Tech Solutions', 'Empresa de tecnologia e innovación', 'Madrid'),
  (2, 'Salud Global', 'Servicios médicos internacionales', 'Barcelona'),
  (3, 'Finanzas Hoy', 'Consultoría financiera', 'Valencia'),
  (4, 'Educación Plus', 'Plataforma educativa', 'Sevilla'),
  (5, 'AgroFuturo', 'Tecnología agrícola', 'Zaragoza'),
  (6, 'EcoVida', 'Soluciones ecológicas', 'Bilbao'),
  (7, 'ConstruyeYa', 'Construcción y reformas', 'Granada'),
  (8, 'Viajes Mundo', 'Agencia de viajes', 'Alicante'),
  (9, 'Legal Asesores', 'Servicios legales', 'Valladolid'),
  (10, 'Arte Digital', 'Diseño y arte digital', 'Málaga');

REPLACE INTO empleos (id, titulo, descripcion, fecha_publicacion, ubicacion, empresa_id, habilidades, categoria)
VALUES
  (1, 'Desarrollador Backend', 'Desarrollo de APIs y microservicios', NOW(), 'Remoto', 1, 'Python,SQL,Docker', 'Tecnología'),
  (2, 'Analista de Datos', 'Análisis y visualización de datos', NOW(), 'Madrid', 2, 'Excel,PowerBI,SQL', 'Datos'),
  (3, 'Contable', 'Gestión de cuentas y balances', NOW(), 'Valencia', 3, 'Python,Excel', 'Finanzas'),
  (4, 'Profesor Online', 'Clases virtuales de matemáticas', NOW(), 'Remoto', 4, 'Python,Zoom', 'Marketing'),
  (5, 'Ingeniero Agrónomo', 'Optimización de cultivos', NOW(), 'Zaragoza', 5, 'Agronomía,Drones', 'Marketing'),
  (6, 'Consultor Ambiental', 'Evaluación de impacto ambiental', NOW(), 'Bilbao', 6, 'Medio Ambiente,Drones', 'Medio Ambiente'),
  (7, 'Jefe de Obra', 'Supervisión de proyectos de construcción', NOW(), 'Granada', 7, 'Gestión de Proyectos,Drones', 'Construcción'),
  (8, 'Agente de Viajes', 'Atención al cliente y reservas', NOW(), 'Alicante', 8, 'Atención al Cliente,Drones', 'Turismo'),
  (9, 'Abogado Junior', 'Asistencia legal y redacción de documentos', NOW(), 'Valladolid', 9, 'Derecho,Redacción', 'Legal'),
  (10, 'Diseñador Gráfico', 'Creación de contenido digital', NOW(), 'Málaga', 10, 'Photoshop,Illustrator', 'Diseño');

REPLACE INTO aplicaciones_empleo (id, usuario_id, empleo_id, fecha_aplicacion, estado) VALUES
  (1, 1, 1, NOW(), 'pendiente'),
  (2, 2, 3, NOW(), 'aceptado'),
  (3, 3, 2, NOW(), 'rechazado'),
  (4, 4, 4, NOW(), 'pendiente'),
  (5, 5, 5, NOW(), 'pendiente'),
  (6, 6, 6, NOW(), 'aceptado'),
  (7, 7, 7, NOW(), 'pendiente'),
  (8, 8, 8, NOW(), 'rechazado'),
  (9, 9, 9, NOW(), 'pendiente'),
  (10, 10, 10, NOW(), 'aceptado');

SET FOREIGN_KEY_CHECKS=1; -- to re-enable them
