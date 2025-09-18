# src/di/containers.py
from dependency_injector import containers, providers
from repositories.postgres_task_repository import PostgresTaskRepository
from services.task_service import TaskService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # DB conncection pool is now handled in database.pool
    
    # Repository
    # No need to pass pool to provider now
    task_repository = providers.Factory(
        PostgresTaskRepository
    )
    
    # Service
    task_service = providers.Factory(
        TaskService,
        task_repository=task_repository
    )