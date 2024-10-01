import sys
import click
import asyncio
from app.database import AsyncSessionFactory
from app.utils.auth import get_hashed_password
from app.models.users import User  # Import your User model

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



@click.command()
@click.option('--username', prompt='Enter username', help='Superuser username')
@click.option('--email', prompt='Enter email', help='Superuser email')
@click.option('--password', prompt=True, hide_input=True, help='Superuser password')
def create_super_user(username, email, password):
    # Run the asynchronous task in an event loop
    asyncio.run(_create_super_user(username, email, password))

async def _create_super_user(username, email, password):
    """
    Asynchronously creates a superuser in the database if one does not already exist.
    Args:
        username (str): The username for the superuser.
        email (str): The email address for the superuser.
        password (str): The password for the superuser.
    Returns:
        None
    Raises:
        Exception: If there is an issue with database operations.
    Comments:
        - Establishes an asynchronous session with the database.
        - Checks if a superuser with the given username already exists.
        - If the superuser does not exist, creates a new superuser with the provided credentials.
        - Adds the new superuser to the database and commits the transaction.
        - Prints a success message if the superuser is created, otherwise prints that the superuser already exists.
    """
    async with AsyncSessionFactory() as db:
        # Check if the superuser already exists
        existing_superuser = await User.get_one(db, [User.username == username])

        if not existing_superuser:
            # Create a new superuser
            superuser = User(
                username=username,
                email=email,
                password=get_hashed_password(password),
                is_active=True,
                is_superuser=True
            )
            
            # Add the superuser to the database
            db.add(superuser)
            await db.commit()
            await db.refresh(superuser)

            print("Superuser created successfully.")
        else:
            print("Superuser already exists.")

if __name__ == "__main__":
    create_super_user()
