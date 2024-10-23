document.addEventListener("DOMContentLoaded", function () {
    const blogForm = document.getElementById('blog-form');
    const blogList = document.getElementById('blog-list');

    function fetchBlogs() {
        fetch('/blogs')
            .then(response => response.json())
            .then(blogs => {
                blogList.innerHTML = '';
                blogs.forEach(blog => {
                    const blogPost = document.createElement('div');
                    blogPost.className = 'blog-post';
                    blogPost.innerHTML = `
                        <h3>${blog.title}</h3>
                        <p>${blog.content}</p>
                        <button onclick="deleteBlog(${blog.id})">Delete</button>
                    `;
                    blogList.appendChild(blogPost);
                });
            });
    }

    blogForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;

        fetch('/blogs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, content })
        })
        .then(response => response.json())
        .then(data => {
            fetchBlogs(); // Refresh the blog list
            blogForm.reset(); // Clear the form
        });
    });

    window.deleteBlog = function (id) {
        fetch(`/blogs/${id}`, {
            method: 'DELETE'
        })
        .then(() => {
            fetchBlogs(); // Refresh the blog list after deletion
        });
    };

    fetchBlogs(); // Initial fetch to load blogs
});
