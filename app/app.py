from fastapi import FastAPI, HTTPException

from app.schemas import PostCreate

app = FastAPI()
text_posts = {
    1: {
        "title": "Getting Started with Python",
        "content": "Python is an easy-to-learn and powerful programming language.",
    },
    2: {
        "title": "Why Use FastAPI?",
        "content": "FastAPI provides high performance, automatic docs, and intuitive type hints.",
    },
    3: {
        "title": "Understanding REST APIs",
        "content": "RESTful services use standard HTTP methods like GET, POST, PUT, and DELETE.",
    },
    4: {
        "title": "Path vs Query Parameters",
        "content": "Path params identify specific resources, while query params filter collections.",
    },
    5: {
        "title": "Introduction to Databases",
        "content": "Relational databases use SQL to store and query structured data efficiently.",
    },
    6: {
        "title": "Docker Basics",
        "content": "Containers package your application along with all its dependencies for easy deployment.",
    },
    7: {
        "title": "Async Programming Concepts",
        "content": "Asynchronous I/O prevents server blocking during database and network calls.",
    },
    8: {
        "title": "Git Workflow Tips",
        "content": "Commit often, write descriptive commit messages, and use feature branches.",
    },
    9: {
        "title": "Authentication vs Authorization",
        "content": "Authentication verifies who you are, while authorization determines what you can do.",
    },
    10: {
        "title": "Deploying to Production",
        "content": "Use reverse proxies, process managers, and proper logging when deploying live.",
    },
}


@app.get("/")
def app_start():
    return {"message": "app running"}


@app.get("/hello-world")
def hello_world():
    return {"message": "hello world"}


@app.get("/get-posts")
def get_posts(limit: int | None = None):
    if limit:
        return dict(list(text_posts.items())[:limit])
    return text_posts


@app.get("/get-post/{id}", responses={404: {"description": "Post Not Found"}})
def get_post_by_id(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return text_posts.get(id)


@app.post("/create-post")
def create_post(post: PostCreate) -> PostCreate:
    new_post = {
        "title": post.title,
        "content": post.content,
    }
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
