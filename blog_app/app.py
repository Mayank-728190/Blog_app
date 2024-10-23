from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Initialize the JSON file if it does not exist
def initialize_blog_file():
    if not os.path.exists("blogs.json"):
        with open("blogs.json", "w") as file:
            json.dump([], file)

# Load blog data from the JSON file
def load_blog_data():
    if not os.path.exists("blogs.json"):
        return []
    
    with open("blogs.json", "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# Save blog data to the JSON file
def save_blog_data(blogs):
    with open("blogs.json", "w") as file:
        json.dump(blogs, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blogs', methods=['POST'])
def create_blog():
    new_blog = request.json
    blogs = load_blog_data()
    new_blog['id'] = len(blogs) + 1  # Simple ID assignment
    blogs.append(new_blog)
    save_blog_data(blogs)
    return jsonify(new_blog), 201

@app.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = load_blog_data()
    return jsonify(blogs)

@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blogs = load_blog_data()
    blog = next((b for b in blogs if b['id'] == blog_id), None)
    return jsonify(blog) if blog else ('', 404)

@app.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blogs = load_blog_data()
    blog = next((b for b in blogs if b['id'] == blog_id), None)
    if blog:
        updated_blog = request.json
        blog.update(updated_blog)
        save_blog_data(blogs)
        return jsonify(blog)
    return ('', 404)

@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blogs = load_blog_data()
    blog = next((b for b in blogs if b['id'] == blog_id), None)
    if blog:
        blogs.remove(blog)
        save_blog_data(blogs)
        return ('', 204)
    return ('', 404)

# Initialize the blog file when starting the app
if __name__ == "__main__":
    initialize_blog_file()
    app.run(debug=True)
