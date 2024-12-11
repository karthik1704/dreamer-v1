from pathlib import Path
from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecuritySchemeType
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from .settings import UPLOAD_DIR
from .dependencies.auth import oauth2_bearer, oauth2_bearer_student
from .routers import users, auth, batches, notes,  students, live_classes
from .routers.videos import students as student_videos, admin as admin_videos
app = FastAPI(title="Seyon Acadamy V1", version="0.1.0")


origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://www.crm.seyonacademy.com",
    "https://crm.seyonacademy.com",
    "https://seyonacademy.com",
    "https://www.seyonacademy.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Serve the `uploads/` directory at 
# the `/static` path
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")





app.include_router(auth.router)
app.include_router(users.router)
app.include_router(batches.router)
app.include_router(notes.router)
app.include_router(admin_videos.router)
app.include_router(student_videos.router)
app.include_router(students.router)
app.include_router(live_classes.router)




# Store the original OpenAPI function to avoid infinite recursion
original_openapi = app.openapi

# Custom OpenAPI configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the default OpenAPI schema first
    openapi_schema = original_openapi()

    # Add custom security schemes for users and admins
    openapi_schema["components"]["securitySchemes"] = {
        "AdminAuth": {
            "type": SecuritySchemeType.oauth2.value,
            "flows": {
                "password": {
                    "tokenUrl": "auth/",
                    "scopes": {},
                }
            },
        },
        "StudentAuth": {
            "type": SecuritySchemeType.oauth2.value,
            "flows": {
                "password": {
                    "tokenUrl": "auth/student",
                    "scopes": {},
                }
            },
        },
    }

    # Adjust security for individual routes
    for path, methods in openapi_schema["paths"].items():
        for method in methods:
            if not "/student" in path:
                openapi_schema["paths"][path][method]["security"] = [{"AdminAuth": []}]
            elif "/student" in path:
                openapi_schema["paths"][path][method]["security"] = [{"StudentAuth": []}]

    # Save the customized schema to avoid regenerating it
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign the custom OpenAPI function
app.openapi = custom_openapi