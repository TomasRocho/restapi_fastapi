from app.crud.turma_crud import TurmaCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class TurmaService:
    
    @staticmethod
    def create(session, turma_create):
        try:
            return TurmaCRUD.create(session, turma_create)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Turma com essa descrição já existe")
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Professor ou disciplina associada não encontrada")
            raise
    
    @staticmethod
    def update(session, turma_id, turma_update):
        try:
            turma = TurmaCRUD.update(session, turma_id, turma_update)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Turma com essa descrição já existe")
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Professor ou disciplina associada não encontrada")
            raise
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma
    
    @staticmethod
    def delete(session, turma_id):
        if not TurmaCRUD.get_by_id(session, turma_id):
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        TurmaCRUD.delete(session, turma_id)
        return {"detail": "Turma deletada com sucesso"}
    
    @staticmethod
    def get_by_id(session, turma_id):
        turma = TurmaCRUD.get_by_id(session, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma
    
    @staticmethod
    def get_all(session):
        return TurmaCRUD.get_all(session)
    
    @staticmethod
    def get_by_parametros(session, descricao=None, periodo=None,nome_professor=None, nome_disciplina=None):
        return TurmaCRUD.get_by_parametros(session, descricao, periodo,nome_professor,nome_disciplina)