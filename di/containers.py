# src/di/containers.py
from dependency_injector import containers, providers
from repositories.postgres_task_repository import PostgresTaskRepository
from services.task_service import TaskService
import asyncpg

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # DB conncection pool is now handled in database.pool

    # db_pool = providers.Resource(
    #     asyncpg.create_pool,
    #     dsn=config.database.dsn,
    #     min_size=5,
    #     max_size=10,
    #     timeout=30
    # )
    
    # Repository
    # No need to pass pool to provider now
    task_repository = providers.Factory(
        PostgresTaskRepository
        # pool=db_pool
    )
    
    # Service
    task_service = providers.Factory(
        TaskService,
        task_repository=task_repository
    )