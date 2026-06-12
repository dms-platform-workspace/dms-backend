# apps/public_api/containers.py

# apps/public_api/containers.py

from database.connection import create_db_engine, create_session_factory
from dependency_injector import containers, providers


class AppContainer(containers.DeclarativeContainer):
    """
    Global application container.
    Responsible for managing configurations, shared resources (like the database),
    and wiring feature containers together.
    """

    # 1. Configuration object to hold all environment variables/settings
    config = providers.Configuration()

    # 2. Database engine (Singleton so it is created only once during the app's lifecycle)
    db_engine = providers.Singleton(
        create_db_engine,
        database_url=config.db.url,
        echo=config.db.echo,
    )

    # 3. Database session factory (This will be passed to feature containers later)
    session_factory = providers.Singleton(
        create_session_factory,
        engine=db_engine,
    )
