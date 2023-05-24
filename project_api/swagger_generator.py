from drf_yasg.generators import OpenAPISchemaGenerator


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)
        swagger.tags = [
            {"name": "posts", "description": "Viewing and adding posts"},
            {"name": "post", "description": "View and edit your posts"},
            {"name": "tags", "description": "Viewing and adding tags"},
            {"name": "user-posts", "description": "View user posts"},
            {"name": "users", "description": "View list of users"},
            {"name": "user", "description": "View user data, change your data"},
        ]

        return swagger
