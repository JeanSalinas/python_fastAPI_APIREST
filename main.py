# API Rest: interfaz de programación de aplicaciones para compartir recursos
from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable donde tendrá todas las caracteristicas de una API REST
app = FastAPI()

#Definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre:str
    descripcion:Optional[str] = None
    nivel: str
    duracion: int

#simularemos una base de datos

cursos_db = []
# CRUD: read (lectura) 
# GET ALL: leeremos todos los cursos que haya en la base de datos

@app.get('/cursos/', response_model=List[Curso])

def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir,crear) 
# POST: agregamos un nuevo recurso a nuestra base de datos

@app.post('/cursos/', response_model=Curso)

def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) #Usamos uuid para genera un id único e irrepetible
    cursos_db.append(curso)
    return curso

#CRUD read (Lectura)
# Get individual, leeremos el curso que coincida con el id que pidamos

@app.get('/cursos/{curso_id}',response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for  curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail='Curso no encontrado')
    return curso

# CRUD UPDATE (Actualizar / modificar)
# PUT : odificaremos un recurso que coincida con el id que pidamos

@app.put('/cursos/{curso_id}',response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for  curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail='Curso no encontrado')
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) #Buscamos el indice exacto donde esta el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

#CRUD DELETE (Borrar)
# Delete: Eliminaremos un recurso que coincida con el ID que mandemos

@app.delete('/cursos/{curso_id}',response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for  curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail='Curso no encontrado')
    cursos_db.remove(curso)
    return curso