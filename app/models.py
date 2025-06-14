from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, DateTime, Table, ForeignKey, Column, Integer, Text, Boolean, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship

Base = declarative_base()

# --- Modelos principales ---
class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(250))
    email: Mapped[str] = mapped_column(String(250), unique=True)
    foto_perfil: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Empresa(Base):
    __tablename__ = "empresas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(250))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    empleos: Mapped[List["Empleo"]] = relationship(back_populates="empresa")


class Empleo(Base):
    __tablename__ = "empleos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    fecha_publicacion: Mapped[datetime] = mapped_column(default=datetime.now)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(100))
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    empresa: Mapped["Empresa"] = relationship(back_populates="empleos")
    habilidades: Mapped[str] = mapped_column(Text)

# #
# class Publicacion(Base):
#     __tablename__ = "publicaciones"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     contenido: Mapped[str] = mapped_column(Text)
#     fecha: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
#
#     autor: Mapped["Usuario"] = relationship(back_populates="publicaciones")
#     comentarios: Mapped[List["Comentario"]] = relationship(back_populates="publicacion")
#     me_gustas: Mapped[List["MeGusta"]] = relationship(back_populates="publicacion")
#
#
# class Comentario(Base):
#     __tablename__ = "comentarios"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     contenido: Mapped[str] = mapped_column(Text)
#     fecha: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     publicacion_id: Mapped[int] = mapped_column(ForeignKey("publicaciones.id"))
#
#     publicacion: Mapped["Publicacion"] = relationship(back_populates="comentarios")
#
#
# class MeGusta(Base):
#     __tablename__ = "me_gustas"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
#     publicacion_id: Mapped[int] = mapped_column(ForeignKey("publicaciones.id"))
#
#     publicacion: Mapped["Publicacion"] = relationship(back_populates="me_gustas")
#
#
# class Grupo(Base):
#     __tablename__ = "grupos"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     nombre: Mapped[str] = mapped_column(String(100))
#     tema: Mapped[str] = mapped_column(String(200))
#
#     miembros: Mapped[List["Usuario"]] = relationship(secondary=miembros_grupo)
#     publicaciones: Mapped[List["PublicacionGrupo"]] = relationship(back_populates="grupo")
#
#
# class PublicacionGrupo(Base):
#     __tablename__ = "publicaciones_grupo"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     contenido: Mapped[str] = mapped_column(Text)
#     fecha: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id"))
#     autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
#
#     grupo: Mapped["Grupo"] = relationship(back_populates="publicaciones")
#
#
# class Mensaje(Base):
#     __tablename__ = "mensajes"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     contenido: Mapped[str] = mapped_column(Text)
#     timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     remitente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
#     destinatario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
#
#     remitente: Mapped["Usuario"] = relationship(
#         foreign_keys=[remitente_id], back_populates="mensajes_enviados"
#     )
#     destinatario: Mapped["Usuario"] = relationship(
#         foreign_keys=[destinatario_id], back_populates="mensajes_recibidos"
#     )
#
#
# class Notificacion(Base):
#     __tablename__ = "notificaciones"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     contenido: Mapped[str] = mapped_column(String(200))
#     vista: Mapped[bool] = mapped_column(default=False)
#     timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
#
#     usuario: Mapped["Usuario"] = relationship(back_populates="notificaciones")